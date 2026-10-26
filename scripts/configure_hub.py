"""Configure shared Redoma instructions and live skill links for local coding tools."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

START = '<!-- REDOMA-SHARED-CONTEXT:START -->'
END = '<!-- REDOMA-SHARED-CONTEXT:END -->'


def managed(original, body):
    block = START + '\n' + body.rstrip() + '\n' + END
    if original.count(START) != original.count(END) or original.count(START) > 1:
        raise ValueError('Malformed Redoma block; preserve and reconcile the instruction file.')
    if START in original:
        left, rest = original.split(START, 1)
        _, right = rest.split(END, 1)
        return left + block + right
    return original + ('\n\n' if original else '') + block + '\n'


def safe(path, home):
    if not path.resolve().is_relative_to(home.resolve()):
        raise ValueError('Shared-context path points outside the selected profile: ' + str(path))
    return path


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temp = Path(stream.name)
        stream.write(data)
    try:
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


@contextmanager
def locked(folder):
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'context-setup.lock'
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def directory_link(target, source):
    target.parent.mkdir(parents=True, exist_ok=True)
    if os.name == 'nt':
        # Junctions need no Developer Mode or symlink privilege. Quote PowerShell literals.
        quote = lambda p: "'" + str(p).replace("'", "''") + "'"
        command = ('New-Item -ItemType Junction -Path ' + quote(target)
                   + ' -Target ' + quote(source) + ' -ErrorAction Stop | Out-Null')
        result = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', command],
                                capture_output=True, text=True)
        if result.returncode:
            raise OSError('Unable to create live skill link: ' + str(target))
    else:
        target.symlink_to(source, target_is_directory=True)


def plan(home):
    home = home.expanduser().resolve()
    base = home / '.codex/hub'
    shared = base / 'REDOMA.md'
    context = base / 'CURRENT_CONTEXT.md'
    roots = [home / '.agents/skills', home / '.codex/skills']
    writes, links, current, conflicts = [], [], [], []

    def write(path, body, only_missing=False, block=False):
        safe(path, home)
        if path.is_symlink():
            raise ValueError('Instruction file is a symlink; reconcile it explicitly: ' + str(path))
        before = path.read_bytes() if path.exists() else None
        if only_missing and before is not None:
            return
        content = managed(before.decode('utf-8-sig') if before else '', body) if block else body
        after = content.encode('utf-8')
        if before != after:
            writes.append((path, before, after))

    instructions = '''# Contexto compartilhado da Redoma

Codex, Claude Code e outros agentes locais devem consultar esta mesma base.
Ao iniciar trabalho, leia CURRENT_CONTEXT.md nesta pasta; ao concluir uma etapa
relevante, registre data, ferramenta, resultado, arquivos e proxima acao. Releia
antes de alterar um arquivo que outra sessao possa ter atualizado.

Consulte as skills por nome e descricao em ~/.agents/skills e ~/.codex/skills;
o Claude recebe atalhos de diretorio em ~/.claude/skills para os mesmos arquivos.
Consulte tambem ~/.claude/skills quando a tarefa precisar de uma skill exclusiva
dali. Nao copie nem sobrescreva uma versao local divergente para sincronizar.

Os arquivos globais ~/.codex/AGENTS.md e ~/.claude/CLAUDE.md podem conter regras
pessoais adicionais. Consulte apenas os trechos pertinentes da outra ferramenta;
nao siga novamente imports ou blocos compartilhados ja lidos. Instrucoes de
projeto aplicaveis continuam valendo. Evite ciclos e leitura integral repetida.

Para colaboracao em um projeto, use seu CONTEXTO.md quando existir e salve ali
decisoes, estado e proxima etapa. Nao leia bancos internos de chats, credenciais,
tokens, caches ou settings de outra ferramenta para obter contexto.

Compartilhar arquivos nao compartilha o historico interno dos chats, conexoes,
ferramentas ou permissoes. Agentes com acesso local podem usar esta base; apps
na nuvem precisam de uma integracao propria. Use cada conta pessoal autorizada.
Entre computadores, receba atualizacoes pelos repositorios oficiais; esta ponte
local nao faz upload de contexto pessoal nem habilita envios sem aprovacao.
'''
    write(shared, instructions, block=True)
    write(context, '# Contexto atual\n\nRegistre aqui o estado resumido do trabalho compartilhado.\n', only_missing=True)
    codex = '## Redoma: contexto compartilhado\n\nLeia `~/.codex/hub/REDOMA.md` e siga a base compartilhada com Claude Code.\nMapa dos caminhos locais: `~/.codex/hub/llm-roots.json`.\n'
    claude = '## Redoma: contexto compartilhado\n\n@../.codex/hub/REDOMA.md\n\nMapa dos caminhos locais: `~/.codex/hub/llm-roots.json`.\n'
    write(home / '.codex/AGENTS.md', codex, block=True)
    override = home / '.codex/AGENTS.override.md'
    if override.exists():
        write(override, codex, block=True)
    write(home / '.claude/CLAUDE.md', claude, block=True)

    names = {}
    for root in roots:
        safe(root, home)
        if not root.exists():
            continue
        for source in sorted(root.iterdir()):
            if source.name.startswith('.') or not source.is_dir() or not (source / 'SKILL.md').is_file():
                continue
            if not re.fullmatch('[a-zA-Z0-9_-]+', source.name):
                conflicts.append({'skill': source.name, 'reason': 'unsupported-name'})
                continue
            if source.name in names:
                if names[source.name].resolve() != source.resolve():
                    conflicts.append({'skill': source.name, 'reason': 'multiple-sources'})
                continue
            names[source.name] = source
            target = home / '.claude/skills' / source.name
            safe(target.parent, home)
            if os.path.lexists(target):
                if target.resolve() == source.resolve():
                    current.append(str(target))
                else:
                    conflicts.append({'skill': source.name, 'reason': 'existing-claude-skill', 'path': str(target)})
            else:
                links.append((target, source.resolve()))
    manifest = {'schema_version': 1, 'home': str(home), 'shared_instruction': str(shared),
                'context': str(context), 'skill_roots': [str(p) for p in roots],
                'entrypoints': {'codex': str(home / '.codex/AGENTS.md'), 'claude': str(home / '.claude/CLAUDE.md')},
                'skill_links': {str(t): str(s) for t, s in links}, 'conflicts': conflicts}
    # Include existing aliases so a second run produces the identical manifest.
    for alias in current:
        manifest['skill_links'][alias] = str(Path(alias).resolve())
    write(base / 'llm-roots.json', json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    return home, writes, links, current, conflicts


def configure(home=None, apply=True):
    home = Path(home or Path.home()).expanduser().resolve()
    if not apply:
        _, writes, links, current, conflicts = plan(home)
        return {'applied': False, 'changed_files': [str(p) for p, *_ in writes],
                'linked_skills': [str(t) for t, _ in links], 'conflicts': conflicts}
    base = safe(home / '.codex/hub', home)
    with locked(base):
        _, writes, links, current, conflicts = plan(home)
        backups = []
        for path, before, after in writes:
            actual = path.read_bytes() if path.exists() else None
            if actual != before:
                raise ValueError('Instruction file changed during setup; nothing was overwritten: ' + str(path))
            if before is not None:
                backup = safe(base / 'backups' / (path.name + '-' + hashlib.sha256(before).hexdigest() + '.bak'), home)
                if not backup.exists():
                    atomic(backup, before)
                backups.append(str(backup))
            atomic(path, after)
        for target, source in links:
            directory_link(target, source)
            if target.resolve() != source.resolve():
                raise ValueError('Live skill link did not resolve to its source: ' + str(target))
    return {'applied': True, 'changed_files': [str(p) for p, *_ in writes], 'backups': backups,
            'linked_skills': [str(t) for t, _ in links], 'already_linked': len(current), 'conflicts': conflicts,
            'verification': 'filesystem-only; confirm discovery in a new local tool session'}


def after_install(destination, home=None):
    home = Path(home or Path.home()).expanduser().resolve()
    destination = destination.expanduser().resolve()
    if destination not in {(home / '.agents/skills').resolve(), (home / '.codex/skills').resolve()}:
        return {'applied': False, 'reason': 'custom-destination; run configure_hub.py --home explicitly'}
    return configure(home)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--check', action='store_true', help='Show planned changes without writing.')
    args = parser.parse_args()
    print(json.dumps(configure(args.home, not args.check), ensure_ascii=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        print(json.dumps({'ok': False, 'stage': 'shared-context-setup', 'error': str(error),
                          'next_action': 'Preserve existing files; resolve access, active lock or conflicting paths.'}))
        raise SystemExit(1)
