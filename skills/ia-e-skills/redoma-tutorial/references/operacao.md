# Operação dos dois repositórios

## Acesso e pastas

Destinos oficiais: `https://github.com/ARedomaDigital/skills-redoma.git` (geral) e `https://github.com/ARedomaDigital/skills-equipe.git` (interno).

Cada integrante usa sua conta GitHub. O administrador concede leitura e, para colaboradores que enviam mudanças, escrita nos dois destinos. Não envie convites sem uma solicitação e os usuários exatos. O privado só pode ser baixado depois que o acesso estiver disponível. Não compartilhar credenciais de outro integrante.

Exemplo Windows; execute cada comando separadamente, verificando o resultado. Adapte a pasta e reutilize clones existentes após inspeção:

```powershell
git --version
python --version
python -c "from zoneinfo import ZoneInfo; print(ZoneInfo('America/Sao_Paulo'))"
```

Se faltar o banco de fusos, instale `tzdata` no Python que executará a rotina. Não use o fuso do sistema como substituto silencioso.

```powershell
python -m pip install tzdata
$redomaRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Redoma'
New-Item -ItemType Directory -Force -Path $redomaRoot
git clone https://github.com/ARedomaDigital/skills-redoma.git (Join-Path $redomaRoot 'skills-redoma')
git clone https://github.com/ARedomaDigital/skills-equipe.git (Join-Path $redomaRoot 'skills-equipe')
```

No macOS/Linux, adapte ao shell e à pasta pessoal. Não execute PowerShell por suposição.

## Baixar e instalar tudo que os catálogos fornecem

Antes: leia `git status --short`, confira `origin`, branch e os recibos de instalação. Salve fora das pastas gerenciadas uma cópia das skills que tenham alterações. Se o clone estiver editado ou houver commits divergentes, faça comparação antes do pull.

Nos dois clones, execute `git pull --ff-only`. No clone público:

```powershell
python scripts/install.py --all --update
python scripts/install_external.py --all --update
```

No clone privado:

```powershell
python scripts/install.py --all --update
```

O destino padrão é `~/.agents/skills`. O instalador de catálogo usa `.skills-equipe-install.json`; o de fontes externas usa `.skills-redoma-install.json`. Esses recibos registram hashes da versão instalada. `--update` não autoriza apagar uma edição local: o instalador deve parar quando ela existir. Não apague recibos para contornar um conflito.

`install_external.py --all` cobre somente entradas marcadas `upstream`. Consulte `external-sources.json` para separar as que exigem plugins ou componentes fornecidos pelo aplicativo. O resultado “tudo instalado” precisa distinguir essas categorias. Instalar uma instrução não instala necessariamente executáveis ou conecta serviços.

## Enviar alterações

Na máquina publicadora já configurada, a rotina existente é:

```powershell
python scripts/library.py sync --push
```

Ela procura as fontes de `sync.local.json`, valida a política de distribuição, reconstrói os catálogos, confere visibilidade, cria commits e verifica os dois pushes. Os clones devem ser irmãos. A configuração local não deve ser copiada de outro computador: contém caminhos específicos. As duas raízes pessoais são fontes obrigatórias; plugins e outras pastas só entram se forem realmente usados.

Antes de usar essa rotina em uma nova máquina, confira a completude das fontes contra os DOIS catálogos e `distribution-policy.json`. O exportador reconstrói o catálogo a partir do que descobre. NÃO exporte uma instalação parcial: preserve as skills compartilhadas que esse computador não recebeu. Se a configuração não puder representar todas as fontes necessárias, pare somente a publicação e informe o ajuste necessário. Baixar e usar as skills pode continuar.

Para mudanças em skills existentes, compare três versões: a base registrada no recibo, o arquivo local e o arquivo remoto recebido. Se apenas o remoto mudou, instale. Se apenas o local mudou, preserve e publique antes de atualizar seu recibo. Se ambos mudaram de forma diferente, reconcilie em uma cópia e valide o resultado antes do envio. Nunca atualize o recibo para fingir que uma edição foi instalada pelo mecanismo.

Para skill nova, valide metadados e referências e classifique como `public`, `private` ou `external` na política. Não altere a visibilidade do repositório nem transfira arquivos entre as categorias para fazer um comando passar.

Depois do push, compare `git rev-parse HEAD` com `git ls-remote origin refs/heads/main` em CADA clone. Só informe envio confirmado quando os hashes coincidirem. Uma rejeição porque outra pessoa enviou primeiro exige receber e reconciliar; não fazer force push.

## Rotina diária coordenada pelo assistente

O padrão é uma tentativa na primeira mensagem humana de cada data `America/Sao_Paulo`, além de pedidos explícitos. Não é um serviço executado com o computador desligado ou com o assistente fechado.

Configure um bloco pequeno nas instruções globais do assistente, com caminhos absolutos desta máquina e a chamada da skill `redoma-tutorial`. Preserve regras já existentes. O bloco deve orientar o agente a:

1. Consultar um marcador diário local e um bloqueio compartilhado entre chats. Registrar a tentativa antes de acessar a rede; não repetir falhas automaticamente naquele dia.
2. Inspecionar os dois clones e os recibos, buscar as mudanças e comparar as três versões antes de qualquer instalação ou exportação.
3. Receber e instalar mudanças sem conflito; preservar edições locais. Quando a publicação estiver configurada e completa, enviar mudanças pela rotina validada. Uma edição simultânea exige revisão da parte conflitante.
4. Registrar separadamente recebimento, instalação e push de cada destino. Não usar um resultado de push como prova de instalação.
5. Em pedido explícito, executar sem o limite diário. Se o usuário pedir apenas baixar, não publicar. Se pedir apenas aprender, não alterar configurações.

O marcador `.local/message-sync.json` do exportador limita as chamadas dele. Ele não comprova nem limita uma rotina adicional de download. Se a automação incluir download, ela precisa de controle próprio para o fluxo completo. Não instale um segundo hook que duplique o mesmo envio.

Enquanto não existir um executor testado do fluxo completo, use a skill para o assistente coordenar essas etapas e identifique isso como automação por instruções. Não prometa sincronização bidirecional independente só por ter acrescentado uma frase ao AGENTS.md.

## Erros comuns e resposta útil

| Situação | O que fazer |
| --- | --- |
| Repositório privado não abre | Conferir conta, convite e permissão; o link não substitui acesso. |
| Sem permissão de push | Pedir ao administrador acesso de escrita nos dois destinos. |
| Python sem America/Sao_Paulo | Instalar tzdata no interpretador correto. |
| Skill local difere | Preservar cópia, comparar com base e remoto; não sobrescrever. |
| Remote aponta para Kellerr | Verificar a migração na ARedomaDigital antes de corrigir origin. |
| Catálogo exige fontes ausentes | Completar configuração da máquina publicadora; não remover entradas compartilhadas. |
| Pull rejeita divergência | Examinar commits locais/remotos e reconciliar sem force push. |
| Skill de plugin não executa | Instalar o plugin e conectar a conta do próprio integrante. |

Verificação do Codex: [documentação oficial sobre skills](https://learn.chatgpt.com/docs/build-skills). Ele descobre skills pessoais em `.agents/skills`; mudanças costumam ser detectadas automaticamente. Se não aparecerem, reinicie o aplicativo. Consulte também `.codex/skills` por convenção da equipe, evitando duplicar o mesmo nome.

## Verificacao automatica e log de falhas

Antes de cada sincronizacao efetiva, library.py roda test_library.py e test_install.py por unittest, sem rede. Falha ou timeout de testes interrompe o fluxo antes de Git/rede. O resultado dos testes integra o recibo de sucesso; nao substituir por uma afirmacao manual de que tudo passou.

O pacote IANA tzdata pode estar instalado em um perfil inacessivel ao processo protegido. library.py tenta o provedor normal e depois .local/tzdata/zoneinfo. Preparar essa copia a partir de um pacote confiavel, sem alterar permissoes. Atualiza-la junto com tzdata. Nao substituir silenciosamente America/Sao_Paulo por um deslocamento fixo.

Para terceiros, declarar external na politica e registrar a fonte no manifesto. Se a origem exata ainda for desconhecida, usar manual-origin-pending e deixar essa limitacao explicita; nao inventar URL nem copiar o conteudo para o repositorio publico.

Em cada erro, o terminal emite final_log com identificador do evento, etapa, causa sanitizada, proxima acao e indicacao de lembrete. Sao mantidos .local/last-error.json, .local/errors.jsonl e .local/errors/<evento>.json, fora do Git. Se gravacao falhar, log_write_errors aparece no terminal junto do erro original. O agente deve reproduzir um resumo na resposta final e apontar um arquivo acessivel. Uma falha de outro programa, encerramento forcado do processo ou indisponibilidade total do terminal pode impedir a emissao; nao prometer cobertura universal.

Uma chamada diaria pulada com previous_ok=false emite lembrete do erro anterior, nao executa sincronizacao e nao deve ser descrita como sucesso. Uma falha nova exige teste de regressao antes da correcao. Incluir cenarios de fuso, classificacao, falha de testes, marcador diario, credenciais nos logs e erro ao salvar logs.
