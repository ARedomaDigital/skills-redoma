"""Install linked upstream skills directly from their official GitHub repositories."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = '.skills-redoma-install.json'


def files(folder):
    result = {}
    for path in folder.rglob('*'):
        if path.is_symlink():
            raise ValueError('A source contains a symbolic link: ' + str(path))
        if path.is_file() and path.name != RECEIPT:
            result[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('id', nargs='?')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--dest', type=Path, default=Path.home() / '.agents' / 'skills')
    args = parser.parse_args()
    rows = json.loads((ROOT / 'external-sources.json').read_text(encoding='utf-8'))['skills']
    eligible = {row['id']: row for row in rows if row['install'] == 'upstream'}
    if args.list:
        for row in rows:
            print(row['id'] + '\t' + row['source'] + '\t' + row['url'])
        return
    if args.all == bool(args.id):
        parser.error('Use --all ou um identificador.')
    selected = list(eligible.values()) if args.all else [eligible[args.id]]
    destination = args.dest.expanduser().resolve()
    with tempfile.TemporaryDirectory(prefix='redoma-skills-') as temp:
        clones = {}
        actions = []
        for row in selected:
            url = row['url']
            if url not in clones:
                repo = Path(temp) / ('repo-' + str(len(clones)))
                result = subprocess.run(['git', 'clone', '--depth', '1', '--quiet', url + '.git', str(repo)],
                    capture_output=True, text=True, env={**os.environ, 'GIT_LFS_SKIP_SMUDGE': '1'})
                if result.returncode:
                    raise ValueError('Falha ao baixar a fonte oficial: ' + url)
                clones[url] = repo
            repo = clones[url]
            source = (repo / row['path']).resolve()
            if not source.is_relative_to(repo.resolve()) or not (source / 'SKILL.md').is_file():
                raise ValueError('A skill mudou de local na origem: ' + row['id'])
            new_files = files(source)
            target = (destination / row['id']).resolve()
            if not target.is_relative_to(destination):
                raise ValueError('Destino inválido.')
            if target.exists():
                actual = files(target)
                if actual == new_files:
                    continue
                receipt_path = target / RECEIPT
                if not args.update or not receipt_path.exists():
                    raise ValueError('A skill já existe e difere da origem: ' + row['id'])
                receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
                if actual != receipt['files']:
                    raise ValueError('Há alterações locais em ' + row['id'])
            else:
                receipt = None
            actions.append((row, source, target, new_files, receipt))
        for row, source, target, new_files, receipt in actions:
            if receipt:
                for relative in receipt['files']:
                    old = (target / relative).resolve()
                    if not old.is_relative_to(target):
                        raise ValueError('Registro de instalação inválido.')
                    old.unlink()
            target.mkdir(parents=True, exist_ok=True)
            for relative in new_files:
                output = target / relative
                output.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source / relative, output)
            if files(target) != new_files:
                raise ValueError('Falha ao verificar ' + row['id'])
            (target / RECEIPT).write_text(json.dumps({'url': row['url'], 'path': row['path'],
                'commit': subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip(),
                'files': new_files}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'installed_or_updated': [row['id'] for row, *_ in actions],
                      'already_current': len(selected) - len(actions)}, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError, KeyError) as error:
        raise SystemExit(str(error))
