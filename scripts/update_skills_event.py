"""Receive only: validate remote snapshots, preflight both catalogs, install approved skills."""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

REPOS = ('skills-redoma', 'skills-equipe')


def run(*args, cwd=None, binary=False):
    result = subprocess.run(list(args), cwd=cwd, capture_output=True,
                            env={**os.environ, 'GIT_TERMINAL_PROMPT':'0','GCM_INTERACTIVE':'never'},
                            timeout=120)
    if result.returncode:
        raise ValueError('Command failed: ' + args[0] + ' ' + args[1] + '; inspect repository access or local conflicts.')
    return result.stdout if binary else result.stdout.decode('utf-8', errors='replace').strip()


@contextmanager
def lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd=os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def extract_snapshot(archive, destination):
    with zipfile.ZipFile(archive) as source:
        total=0
        for entry in source.infolist():
            output=(destination/entry.filename).resolve()
            if not output.is_relative_to(destination.resolve()):
                raise ValueError('Archive path outside snapshot.')
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('Snapshot symbolic links are unsupported.')
            total+=entry.file_size
            if total>512*1024*1024: raise ValueError('Snapshot exceeds size limit.')
        source.extractall(destination)


def load_installer(snapshot, label):
    # The runtime is a pinned local copy installed by the human, never new code from a push.
    runtime=Path(__file__).resolve().parent
    if str(runtime) not in sys.path: sys.path.insert(0,str(runtime))
    spec=importlib.util.spec_from_file_location('event_install_'+label,runtime/'install.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.ROOT=snapshot
    return module


def tree_files(folder):
    result={}
    for path in folder.rglob('*'):
        if path.is_symlink(): raise ValueError('Skill source contains a symbolic link.')
        if path.is_file() and path.name!='.skills-equipe-install.json':
            result[path.relative_to(folder).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def prepare_retirements(entries, destination, backup):
    """Retire an unchanged installed prior mark, preserve anything edited or unmanaged."""
    family=lambda name: re.sub(r'-mk\d+$','',name)
    desired={e['name'] for e in entries}
    families={family(name) for name in desired}
    actions=[]
    if not destination.exists(): return actions
    for path in destination.iterdir():
        if not path.is_dir() or path.name in desired or family(path.name) not in families: continue
        receipt_path=path/'.skills-equipe-install.json'
        if path.is_symlink() or not receipt_path.is_file():
            raise ValueError('Old mark is unmanaged: '+path.name)
        receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
        if tree_files(path)!=receipt.get('files'):
            raise ValueError('Old mark has local edits: '+path.name)
        actions.append((path,backup/path.name))
    return actions


def synchronize(config):
    home=Path(config['home']).expanduser().resolve()
    state_dir=home/'.codex/hub/skills-events'
    destination=home/'.agents/skills'
    state_file=state_dir/'installed-heads.json'
    previous=json.loads(state_file.read_text()) if state_file.exists() else {}
    with lock(state_dir/'update.lock'), tempfile.TemporaryDirectory(prefix='snapshots-',dir=state_dir) as temp:
        snapshots=[];heads={};all_entries=[]
        for name in REPOS:
            path=Path(config['repositories'][name]).resolve()
            expected='https://github.com/ARedomaDigital/'+name+'.git'
            if run('git','remote','get-url','origin',cwd=path)!=expected:
                raise ValueError('Repository remote does not match the configured Redoma source.')
            # Protect local work: fetch only. Clones, working trees and local commits stay intact.
            run('git','fetch','--quiet','origin','main',cwd=path)
            head=run('git','rev-parse','refs/remotes/origin/main',cwd=path)
            if not re.fullmatch('[a-f0-9]{40}',head): raise ValueError('Invalid remote revision.')
            heads[name]=head
            snapshot=Path(temp)/name;snapshot.mkdir()
            archive=Path(temp)/(name+'.zip')
            archive.write_bytes(run('git','archive','--format=zip',head,cwd=path,binary=True))
            extract_snapshot(archive,snapshot)
            module=load_installer(snapshot,name)
            entries=json.loads((snapshot/'catalog.json').read_text(encoding='utf-8'))['skills']
            module.preflight(entries,destination,True)
            snapshots.append((module,entries));all_entries.extend(entries)
        names=[e['name'] for e in all_entries]
        if len(names)!=len(set(names)): raise ValueError('Duplicated names across the catalogs.')
        if previous==heads: return {'ok':True,'changed':False,'heads':heads}
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        retirements=prepare_retirements(all_entries,destination,state_dir/'backups'/stamp)
        for source,target in retirements:
            target.parent.mkdir(parents=True,exist_ok=True);source.rename(target)
        try:
            for module,entries in snapshots: module.install_group(entries,destination,True)
        except Exception:
            for source,target in retirements:
                if not source.exists() and target.exists(): target.rename(source)
            raise
        # Refresh shared links through the pinned local installer runtime.
        import configure_hub
        for source,_ in retirements:
            alias=home/'.claude/skills'/source.name
            is_link=alias.is_symlink() or (hasattr(alias,'is_junction') and alias.is_junction())
            if is_link and alias.resolve()==source.resolve():
                if alias.is_symlink(): alias.unlink()
                else: alias.rmdir()
        link_state=configure_hub.after_install(destination,home)
        if link_state.get('conflicts'): raise ValueError('Shared skill links need local reconciliation.')
        state_file.write_text(json.dumps(heads,indent=2),encoding='utf-8')
        return {'ok':True,'changed':True,'heads':heads,'retired_marks':[p.name for p,_ in retirements]}


def main():
    config=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
    state_dir=Path(config['home'])/'.codex/hub/skills-events';state_dir.mkdir(parents=True,exist_ok=True)
    try:
        result=synchronize(config)
    except FileExistsError:
        result={'ok':False,'busy':True,'conflicts':False,'error':'Another updater holds the lock; retry on reconnect.'}
    except Exception as error:
        result={'ok':False,'conflicts':True,'error':str(error),'next_action':'Preserve local edits and reconcile; no reset or force push.'}
    result['at']=datetime.now(timezone.utc).isoformat()
    (state_dir/'status.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    with (state_dir/'events.jsonl').open('a',encoding='utf-8') as stream: stream.write(json.dumps(result)+'\n')
    print(json.dumps(result))
    return 0 if result['ok'] else 1


if __name__=='__main__': raise SystemExit(main())
