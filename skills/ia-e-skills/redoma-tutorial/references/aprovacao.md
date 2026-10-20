# Aprovacao humana de skills

Regra do usuario de 20/10/2026. Fluxo: rascunho → teste local → pacote revisavel → aprovacao humana explicita → envio verificado → recebimento e instalacao nas outras maquinas.

O teste local pode acontecer antes de aprovar. O agente nao pode fabricar a decisao nem tratar “crie um teste” como aprovacao. Para o usuario atual, ele aprova as skills que esta criando. Em trabalho de equipe, registrar o humano criador/responsavel e sua decisao.

O arquivo skill-approvals.json registra nome, hash da arvore normalizada, criador, aprovador, data com fuso e evidencia. Uma alteracao em qualquer arquivo invalida o recibo anterior para a nova versao; conservar historico. Nao autoaprovar versoes antigas nem criar excecao silenciosa para legado.

library.py verifica as fontes antes de Git/rede e os arquivos exportados antes do push. scripts/install.py verifica os recibos antes de escrever qualquer destino e preserva a protecao contra edicoes locais. scripts/check_release_approvals.py permite a mesma verificacao em CI. A ausencia de aprovacao bloqueia a distribuicao compartilhada; nao impede testar a fonte local.

Consultar: python scripts/approve_skill.py status. Para registrar uma decisao ja recebida, usar approve com --skill, --sha256, --creator, --by, --confirmation e --evidence. A confirmacao e APROVO seguida do nome e do hash completo. Nao existe opcao de aprovar tudo automaticamente. O registro e uma declaracao auditavel, nao assinatura criptografica ou autenticacao humana independente; nao prometer resistencia a um publicador malicioso.

O arquivo de CI so se torna impedimento de merge/push quando o check for obrigatorio nas regras da branch. Nao alterar permissoes ou afirmar protecao remota sem verificacao. Preservar politicas existentes. Depois de aprovado o pacote, distribuir o codigo pelos repositorios e receber/instalar em cada maquina, conferindo separadamente. Ate isso ocorrer, a protecao aplicada e local.

Skills de terceiros continuam external e nao sao redistribuidas como autoria da equipe. Uma adocao local nao permite declarar que o autor original aprovou uma alteracao nossa. Recibos e evidencias no repositorio publico nao podem conter dados de clientes ou credenciais.

Quando o bloqueio ocorrer, mostrar a causa, a versao pendente e o log. Nao apagar a skill do catalogo, pular a verificacao ou repetir o envio para contornar a falta de aprovacao.
