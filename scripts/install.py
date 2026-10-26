"""Install a skill and its catalog dependencies without running skill code."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release_approval
import configure_hub

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = '.skills-equipe-install.json'


def hashes(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob('*')) if p.is_file() and p.name != RECEIPT}


def resolve_group(identifier, catalog, aliases, include_dependencies=True):
    entries = {e['id']: e for e in catalog['skills']}
    identifier = aliases.get(identifier, identifier)
    if identifier not in entries:
        raise ValueError('Escolha um identificador com --list.')
    visited, result = set(), []

    def visit(name, direct=False):
        name = aliases.get(name, name)
        if name in visited:
            return
        visited.add(name)
        if name not in entries:
            raise ValueError('Dependência ausente no catálogo: ' + name)
        entry = entries[name]
        if entry.get('builtin') and not direct:
            return
        if include_dependencies:
            for dependency in entry.get('dependencies', []):
                visit(dependency)
        result.append(entry)

    visit(identifier, True)
    return result


def preflight(entries, destination, update):
    release_approval.require(entries, ROOT / 'skill-approvals.json')
    destination = destination.expanduser().resolve()
    actions = []
    for entry in entries:
        if not entry['valid_metadata']:
            raise ValueError('Metadados incompletos: ' + entry['id'])
        source = (ROOT / entry['path']).resolve()
        if not source.is_relative_to((ROOT / 'skills').resolve()):
            raise ValueError('Caminho de origem inválido.')
        if hashes(source) != entry['files']:
            raise ValueError('A cópia do repositório foi alterada: ' + entry['id'])
        name = entry['name']
        if not name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in name.lower()):
            raise ValueError('Nome da skill exige revisão: ' + entry['id'])
        target = (destination / name).resolve()
        if not target.is_relative_to(destination) or target == destination:
            raise ValueError('Caminho de destino inválido.')
        if target.exists():
            actual = hashes(target)
            if actual == entry['files']:
                continue
            receipt_path = target / RECEIPT
            if not update or not receipt_path.exists():
                raise ValueError('O destino já existe e difere da biblioteca: ' + name + '. Nada foi sobrescrito.')
            receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
            if actual != receipt['files']:
                raise ValueError('Há alterações locais em ' + name + '. Preserve-as antes de atualizar.')
            for relative in receipt['files']:
                if not (target / relative).resolve().is_relative_to(target):
                    raise ValueError('Registro de instalação inválido.')
        else:
            receipt = None
        for relative in entry['files']:
            if not (target / relative).resolve().is_relative_to(target):
                raise ValueError('Arquivo fora do destino da skill.')
        actions.append((entry, source, target, receipt))
    return actions


def install_group(entries, destination, update=False):
    # All destinations are checked before the first file is written.
    actions = preflight(entries, destination, update)
    for entry, source, target, previous in actions:
        if previous:
            for relative in previous['files']:
                (target / relative).unlink()
        target.mkdir(parents=True, exist_ok=True)
        for relative in entry['files']:
            output = target / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, output)
        if hashes(target) != entry['files']:
            raise ValueError('Falha na verificação da instalação: ' + entry['id'])
        approval = release_approval.filtered(release_approval.read_manifest(ROOT / 'skill-approvals.json'), [entry])
        receipt = {'id': entry['id'], 'sha256': entry['sha256'], 'files': entry['files'],
                   'approval': approval['approvals'][0]}
        (target / RECEIPT).write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return [entry['id'] for entry, source, target, receipt in actions]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('id', nargs='?')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--dest', type=Path)
    parser.add_argument('--profile-home', type=Path, default=Path.home(), help='Perfil local para configurar Codex e Claude juntos.')
    parser.add_argument('--no-shared-context', action='store_true', help='Instala apenas os arquivos, sem configurar o perfil.')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--all', action='store_true', help='Instala todas as skills deste repositório.')
    parser.add_argument('--no-deps', action='store_true')
    args = parser.parse_args()
    if args.dest is None:
        args.dest = args.profile_home / '.agents' / 'skills'
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    policy_path = ROOT / 'collection-policy.json'
    policy = json.loads(policy_path.read_text(encoding='utf-8')) if policy_path.exists() else {}
    if args.list:
        for entry in catalog['skills']:
            print(entry['id'] + '\t' + entry['category'])
        return 0
    if args.all:
        if args.id:
            parser.error('Use --all ou um identificador, não ambos.')
        entries = catalog['skills']
    else:
        if not args.id:
            parser.error('Informe um identificador ou use --all.')
        entries = resolve_group(args.id, catalog, policy.get('aliases', {}), not args.no_deps)
    installed = install_group(entries, args.dest, args.update)
    result = {'installed_or_updated': installed, 'already_current': len(entries) - len(installed)}
    try:
        result['shared_context'] = ({'applied': False, 'reason': 'explicit-opt-out'} if args.no_shared_context
                                    else configure_hub.after_install(args.dest, args.profile_home))
    except (OSError, ValueError) as error:
        result['shared_context'] = {'ok': False, 'error': str(error), 'stage': 'shared-context-setup',
                                    'next_action': 'Preserve installed skills; resolve access or conflicting instruction files and run configure_hub.py.'}
        print(json.dumps(result, ensure_ascii=True))
        return 1
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
