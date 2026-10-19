---
name: redoma-welcoming
description: Receba novos integrantes da Redoma e configure o primeiro uso dos repositórios skills-redoma e skills-equipe no computador deles.
---

# Boas-vindas à biblioteca Redoma

Fale em português simples. Explique que uma skill é uma receita de trabalho para a IA; GitHub guarda a versão compartilhada, e cada computador usa uma cópia. Instalar skills não conecta contas nem transfere permissões de outros integrantes.

Os dois destinos oficiais são `ARedomaDigital/skills-redoma` (geral, público) e `ARedomaDigital/skills-equipe` (interno, privado). Kellerr é uma origem histórica de migração, nunca o destino de novas alterações. Confira a visibilidade real; se o estado divergir, informe e não publique conteúdo interno no destino geral.

## Primeiro uso

1. Detecte sistema operacional, pasta pessoal, Git, Python 3.10+ e Codex. No Windows, confira `tzdata` para `America/Sao_Paulo`. Adapte caminhos ao usuário atual; não copie caminhos de outro computador.
2. Confira leitura dos dois repositórios e escrita de quem vai enviar mudanças. Cada pessoa autentica sua própria conta. Se faltar acesso ao privado, explique que o administrador precisa concedê-lo e o integrante precisa aceitar o convite. Não peça senhas ou tokens no chat. O link sozinho não concede acesso.
3. Use uma pasta de trabalho escolhida pelo usuário ou `~/Documents/Redoma`, com clones irmãos `skills-redoma` e `skills-equipe`. Se já existirem, confira seus remotes e mudanças antes de reutilizar. ZIP serve para comparação/recuperação; use clone Git para sincronizar.
4. Leia `README.md` nos dois clones e a referência `references/operacao.md` da skill `redoma-tutorial`. Instale as skills próprias dos dois catálogos e as externas disponíveis pelas fontes oficiais. Componentes de plugins e do sistema exigem o instalador do fornecedor. Relate os que faltam; não declare que todos foram instalados se isso não ocorreu.
5. Configure as duas raízes pessoais `.codex/skills` e `.agents/skills` como fontes de consulta, com uma única cópia editável de cada skill. Use `.agents/skills` como destino padrão. Não copie `.system`, caches, credenciais ou a configuração inteira do computador de origem.
6. Quando o pedido incluir automação, configure a rotina da referência de operação nas instruções globais do assistente, preservando regras existentes. O padrão Redoma é uma tentativa na primeira mensagem humana do dia e também sob pedido explícito. Não crie tarefa por intervalo ou login. Explique que depende de o assistente executar as instruções, com rede e acesso aos arquivos.
7. Verifique os hashes da instalação e mostre uma skill encontrada. Confira separadamente recebimento, envio e configuração diária. Só marque um teste remoto como concluído depois de verificar o commit no destino correto. Não publique um arquivo de teste no repositório público.

## Entrega ao integrante

Responda com os dois links, a pasta de instalação, o que foi testado e o que depende de acesso ou instalação adicional. Apresente estes pedidos prontos:

- “Use redoma-tutorial para baixar as atualizações dos dois repositórios.”
- “Use redoma-tutorial para enviar minhas alterações, separando conteúdo geral e interno.”
- “Use redoma-tutorial e confira se meu computador está sincronizado.”

Para repassar a instalação a outra pessoa, use [o prompt de primeiro acesso](references/primeiro-acesso.md). Execute o que já estiver autorizado e peça somente o dado que bloquear a próxima etapa.
