"""Validate approved catalog content in one repository, including in CI."""
import hashlib
import json
from pathlib import Path
import release_approval

def main():
    root=Path(__file__).resolve().parents[1]
    entries=json.loads((root/'catalog.json').read_text(encoding='utf-8'))['skills']
    result=release_approval.require(entries,root/'skill-approvals.json')
    expected=set()
    for entry in entries:
        expected.add(entry['path']+'/SKILL.md')
        for relative,wanted in entry['files'].items():
            path=(root/entry['path']/relative).resolve()
            if not path.is_relative_to((root/'skills').resolve()):
                raise ValueError('Approved catalog path escaped skills folder.')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=wanted:
                raise ValueError('Approved skill files changed: '+entry['name'])
    actual={p.relative_to(root).as_posix() for p in (root/'skills').rglob('SKILL.md')}
    if actual!=expected: raise ValueError('Uncatalogued skill blocks release.')
    print(json.dumps({'ok':True,**result}))
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,ValueError) as error:
        print(json.dumps({'ok':False,'stage':'human-approval','error':str(error)}))
        raise SystemExit(1)
