# Skills gerais da Redoma

Este é o link público para compartilhar com a equipe: **https://github.com/Kellerr/skills-redoma**.

As skills gerais atualmente usadas na máquina de origem vêm de projetos externos. Este repositório aponta para as fontes oficiais e oferece um instalador para as 22 skills obtidas diretamente de dois projetos no GitHub. Componentes do Codex e de plugins são instalados pelos respectivos fornecedores. Skills de clientes ficam em outro repositório, privado.

## Instalar no Windows

É preciso ter [Git](https://git-scm.com/downloads) e [Python](https://www.python.org/downloads/). Abra o PowerShell:

```powershell
git clone https://github.com/Kellerr/skills-redoma.git
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
