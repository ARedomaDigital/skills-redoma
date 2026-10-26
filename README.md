# Skills gerais da Redoma

Este é o link público para compartilhar com a equipe: **https://github.com/ARedomaDigital/skills-redoma**.

As skills gerais atualmente usadas na máquina de origem vêm de projetos externos. Este repositório aponta para as fontes oficiais e oferece um instalador para as 22 skills obtidas diretamente de dois projetos no GitHub. Componentes do Codex e de plugins são instalados pelos respectivos fornecedores. Skills de clientes ficam em outro repositório, privado.

## Instalar no Windows

É preciso ter [Git](https://git-scm.com/downloads) e [Python](https://www.python.org/downloads/). Abra o PowerShell:

```powershell
git clone https://github.com/ARedomaDigital/skills-redoma.git
cd skills-redoma
.\update.cmd
```

O comando atualiza o clone e copia as skills diretamente de [Matt Pocock](https://github.com/mattpocock/skills) e [HyperFrames](https://github.com/heygen-com/hyperframes). Ele não executa código dessas skills. Instala na pasta `~/.agents/skills` e registra os arquivos instalados para permitir atualizações seguras.

## Atualizar quando quiser

Na pasta clonada, execute:

```powershell
.\update.cmd
```

O último comando instala as skills gerais originais da Redoma que forem adicionadas no futuro. Se uma skill tiver edição local, a atualização para e pede revisão, sem sobrescrevê-la.

## Escolher skills e conferir as fontes

- [Catálogo de skills próprias](CATALOGO.md)
- [Lista de fontes oficiais](external-sources.json)
- `python scripts/install_external.py --list` mostra todas as fontes, inclusive componentes que exigem instalação pelo fornecedor.
- `python scripts/install.py --list` mostra as skills originais disponíveis neste repositório.

Para as skills do Codex e dos plugins, consulte [OpenAI Skills](https://github.com/openai/skills) e a [documentação de plugins do Codex](https://developers.openai.com/codex/plugins). Cada integrante conecta suas próprias contas e serviços.

O repositório público começa com histórico independente. Nunca inclua nele arquivos, contexto ou instruções de clientes.

## Comece por aqui

- [Boas-vindas e configuração do computador](skills/ia-e-skills/redoma-welcoming-mk5/SKILL.md)
- [Tutorial: baixar, enviar e resolver dúvidas](skills/ia-e-skills/redoma-tutorial/SKILL.md)
- [Prompt pronto para o primeiro acesso](skills/ia-e-skills/redoma-welcoming-mk5/references/primeiro-acesso.md)
- [Biblioteca interna da equipe, com acesso privado](https://github.com/ARedomaDigital/skills-equipe)

Cada integrante precisa de acesso aos dois repositórios. O privado exige convite; enviar alterações exige escrita. Os três computadores compartilham os destinos, mas cada um tem configuração, recibos e credenciais próprios.

## Codex e Claude com a mesma base local

A instalacao de skills agora configura automaticamente o contexto compartilhado,
independentemente de qual assistente local executou o comando. Use normalmente
`python scripts/install.py --all --update`; o instalador de fontes externas
`python scripts/install_external.py --all --update` faz a mesma configuracao.

- `~/.codex/hub/REDOMA.md`: orientacoes comuns aos agentes locais.
- `~/.codex/hub/CURRENT_CONTEXT.md`: estado resumido para continuar o trabalho.
- `~/.codex/AGENTS.md` e `~/.claude/CLAUDE.md`: entradas para essa base.
- `~/.agents/skills`: arquivos instalados compartilhados. No Claude, atalhos de
  diretorio em `~/.claude/skills` apontam para os mesmos arquivos, inclusive as
  skills legadas de `~/.codex/skills` quando existirem.
- `~/.codex/hub/llm-roots.json`: caminhos e conflitos encontrados neste perfil.

Regras pessoais e contexto existente sao mantidos; arquivos de instrucoes
alterados recebem backup local. Skills divergentes no Claude nao sao trocadas:
consulte `shared_context.conflicts` no resultado. Uma segunda execucao nao
duplica os apontadores. O instalador nao altera settings, contas ou permissoes.

Para configurar quem ja tem as skills, execute `python scripts/configure_hub.py`.
Use `--check` para simular; `--home CAMINHO` para um perfil isolado. Destinos
personalizados de skills nao alteram o perfil global automaticamente. Para
instalacao so de arquivos, use `--no-shared-context`. Reinicie a sessao local e
confira a descoberta das skills; o instalador verifica os caminhos no disco.

A ponte compartilha arquivos locais, nao o historico interno dos chats nem as
conexoes dos aplicativos. Claude Code local e Codex local tem entradas prontas;
outras ferramentas precisam ler a mesma base pelo mecanismo que suportarem.
Apps na nuvem nao passam a ler este computador. As atualizacoes entre PCs
continuam pelo GitHub: cada colaborador precisa receber a versao do instalador.
Nao ha copia do contexto pessoal para o repositorio nem servico em segundo plano.

## Avisos e atualizacao por evento no Windows

O servico Redoma recebe webhooks assinados de pushes em main nos dois repositorios.
Cada Windows cadastrado mantem uma conexao WebSocket de saida; nao consulta o GitHub
por intervalo. Ao reconectar, recebe o estado mais recente, inclusive depois de
ficar desligado. O servico registra uma confirmacao por computador.

Primeiro cadastro: mantenha os dois clones em pastas irmas, conecte sua propria
conta GitHub com acesso ao privado e peca ao administrador um convite de uso unico
(valido por 15 minutos). Execute no clone:

```powershell
python scripts/install.py --all --update --enable-events
```

A etapa de convite ocorre somente uma vez. O instalador apresenta o estado do
receptor nas proximas execucoes. Alternativa para cadastrar somente o receptor:

```powershell
powershell -NoProfile -File scripts/setup-skills-events.ps1 -Endpoint https://redoma-skills-events.trolcidanos.workers.dev -RepositoryRoot .
```

O receptor inicia no login do usuario como tarefa `Redoma-Skills-Events`, sem janela
e sem privilegio administrativo. A credencial e protegida pelo DPAPI do Windows.
Nao ha senha ou token no repositorio. O administrador pode revogar uma maquina.

O atualizador so recebe: faz fetch dos clones, usa snapshots dos commits remotos,
confere hashes e aprovacoes e faz preflight dos dois catalogos antes de instalar.
Preserva clones de trabalho e pausa diante de conflito em skill local. Marks antigas
inalteradas recebem backup fora das pastas ativas. Nao executa comandos vindos da
mensagem; o runtime e fixado no cadastro e so muda ao executar novamente o setup.
Novidades de fornecedores externos continuam pelo instalador explicito de fontes
externas; o receptor automatico instala os catalogos aprovados da Redoma.

Estado e logs locais: `~/.codex/hub/skills-events/status.json`, `events.jsonl` e
`receiver.jsonl`. Uma notificacao informa sucesso ou conflito. O recebimento em uma
maquina nao comprova instalacao nas demais; confira o registro de cada dispositivo.
