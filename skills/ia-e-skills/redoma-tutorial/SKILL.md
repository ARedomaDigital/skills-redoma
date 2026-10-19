---
name: redoma-tutorial
description: Ensine e execute instalação, download, push e diagnóstico das skills Redoma nos dois repositórios, com linguagem para iniciantes e proteção de edições locais.
---

# Tutorial de skills da Redoma

Atenda a intenção concreta: aprender, baixar, enviar ou diagnosticar. Explique brevemente e execute as operações já solicitadas. Para primeiro acesso, use também `redoma-welcoming`. Leia [a operação dos dois repositórios](references/operacao.md) antes de alterar instalações ou sincronização.

## Explicação para leigos

- Repositório: a biblioteca compartilhada no GitHub.
- Clone: a cópia dessa biblioteca neste computador.
- Instalação: copiar uma skill do clone para a pasta que a IA consulta.
- Pull: receber atualizações do GitHub no clone. Ainda falta atualizar a instalação.
- Commit: registrar um conjunto de mudanças no histórico local.
- Push: enviar commits ao GitHub. Ainda falta os outros computadores receberem e instalarem.
- Conflito: duas pessoas alteraram a mesma base de formas diferentes; conservar as duas versões até reconciliar.

Use só os conceitos necessários à dúvida. Para ensinar, mostre uma operação curta e seu resultado verificável, sem despejar todos os comandos de uma vez.

## Decisões obrigatórias

Trabalhe com `ARedomaDigital/skills-redoma` e `ARedomaDigital/skills-equipe`. Verifique os remotes; não envie ao proprietário anterior. Preserve a divisão geral/público e interno/privado. Acesso público permite baixar, mas não concede permissão de envio.

Uma skill nova precisa de classificação explícita no arquivo `distribution-policy.json` antes da publicação. Uma skill de cliente pertence ao privado. Skills externas seguem as fontes oficiais e suas licenças. Não copie arquivos pessoais ou de clientes para o público.

Compare mudanças antes de atualizar. Não resolva divergências por data do arquivo, `reset --hard`, force push ou sobrescrita de pastas. A ausência de uma skill em um computador não autoriza removê-la da biblioteca compartilhada.

A rotina `library.py sync --push` exporta fontes locais e envia; ela não faz sozinha o caminho completo de recebimento e instalação. Não descreva esse comando como sincronização bidirecional. Leia seu comportamento atual antes de usá-lo em um computador novo, especialmente a exigência de fontes completas e a política de distribuição.

## Como concluir

Ao baixar, confira os dois clones e os arquivos instalados. Ao enviar, confira o commit remoto de cada destino; se um falhar depois de o outro concluir, registre o resultado parcial e não repita o envio bem-sucedido sem necessidade. Ao diagnosticar, informe o erro e a próxima ação específica. Não declare configuração dos três computadores a partir de um único teste local.

Para economizar tokens, carregue apenas o catálogo, a política e a skill envolvida. Ler todos os corpos das skills não é necessário para conferir versões.
