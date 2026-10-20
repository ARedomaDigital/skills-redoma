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

## Aprovacao antes de enviar

Toda criacao ou alteracao fica em teste local ate aprovacao humana explicita do criador/responsavel. Testes e feedback sobre uma imagem nao aprovam automaticamente a skill. Nao autoaprovar. A decisao vale para o hash exato dos arquivos; qualquer edicao exige nova decisao. Leia [o fluxo de aprovacao](references/aprovacao.md) antes de enviar ou distribuir instalacoes. A rotina diaria deve respeitar essa trava.

## Como concluir

Ao baixar, confira os dois clones e os arquivos instalados. Ao enviar, confira o commit remoto de cada destino; se um falhar depois de o outro concluir, registre o resultado parcial e não repita o envio bem-sucedido sem necessidade. Ao diagnosticar, informe o erro e a próxima ação específica. Não declare configuração dos três computadores a partir de um único teste local.

Para economizar tokens, carregue apenas o catálogo, a política e a skill envolvida. Ler todos os corpos das skills não é necessário para conferir versões.

## Testes e relatorio final de erro

Regra do usuario em 20/10/2026: em todo envio ou atualizacao da biblioteca, executar os testes automatizados antes da publicacao. A rotina library.py aplica essa verificacao antes de Git/rede; testes reprovados interrompem o envio. Toda correcao de bug deve incluir regressao que falhe antes e passe depois, cobrindo o comportamento real.

Toda falha deve gerar e exibir um log final com etapa, causa sem credenciais, efeito no envio e proxima acao. Salvar .local/last-error.json, .local/errors.jsonl e um arquivo por evento em .local/errors/. Se o disco nao permitir gravar, manter o relatorio no terminal e informar a falha de gravacao. Na resposta final ao usuario, incluir o erro e o caminho do log; nao ocultar esse relato por haver outra entrega concluida.

Quando o controle diario pular um dia cuja tentativa falhou, emitir o erro anterior como lembrete, sem repetir Git/rede. Detalhes e limites estao em references/operacao.md. Nunca prometer ausencia universal de falhas: testar os cenarios conhecidos e tornar falhas futuras observaveis.
