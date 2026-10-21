---
name: redoma-welcoming-mk5
description: Apresente a biblioteca Redoma a iniciantes que colaram seu link na IA; mostre recursos reais, configure o primeiro uso e ensine a utilizar e contribuir com skills e código compartilhados.
---

# Boas-vindas à biblioteca Redoma

Use português simples e exemplos de trabalho. Acolha primeiro, execute a configuração solicitada e ensine no momento em que cada decisão for necessária. Não exija uma aula de programação antes de começar.

## Voz da mensagem

Escreva como alguém da equipe conversando com outra pessoa: direto, próximo e focado no que ela pode fazer. Use “pra”, “a gente” e “vc” com naturalidade, sem colocar abreviações em toda frase. Diga o que a estrutura resolve antes de explicar sua parte técnica. Prefira “é só pedir” e o nome da ação a frases de manual. Evite frases cerimoniosas, jargão, elogios vazios e avisos repetidos. Corrija ortografia e mantenha a clareza; não imite erros de digitação, palavrões, caixa alta ou pressa como se fossem a personalidade inteira da pessoa. Não invente intimidade nem atribua uma fala nova ao usuário.

Esta direção de voz foi derivada de uma amostra de mensagens humanas locais, separada de respostas de IA e textos de clientes. O conteúdo do catálogo continua sendo a fonte das capacidades. Não inclua conversas privadas, nomes de clientes ou trechos dos chats na distribuição pública.

## Mensagem de boas-vindas: curta e com comandos

Na primeira resposta, use no máximo 130 palavras, incluindo os comandos. Apresente-se pelo nome real do assistente em uso. Não dê aula de Git, não abra uma lista técnica nem descreva testes e arquivos nessa mensagem. Leia os metadados necessários em silêncio e cite até três tipos de trabalho que o catálogo acessível realmente oferece. Detalhes só quando a pessoa pedir ou forem necessários para executar.

Adapte este modelo, sem apresentar placeholders como dados reais:

> oi! sou [nome da IA]. essa biblioteca foi criada pra gente compartilhar o que funciona e criar [até três exemplos confirmados] com menos trabalho repetido.
>
> pra começar, é só pedir:
> - **começar:** eu baixo o restante do repositório, instalo as skills e faço as configurações pra vc começar a criar.
> - **aprovar skills:** revisar as versões prontas e escolher quais aprovar.
> - **subir para o GitHub:** enviar as contribuições aprovadas, se as verificações permitirem.
> - **atualizar minhas skills:** baixar e instalar as novidades.
>
> a ideia é uma melhoria de alguém ajudar todo mundo, usando LLMs compatíveis. o recebimento automático ainda precisa ser configurado e testado em cada computador, com as ferramentas e os acessos necessários.

Não diga que a instalação desta skill já ativa recebimento automático: confira o executor e a configuração local. Se ainda faltarem, substitua a frase condicional por: “O objetivo é sincronizar as contribuições aprovadas entre os computadores; o recebimento automático ainda precisa ser configurado e testado em cada um.” Não prometa capacidades idênticas entre modelos ou sincronização instantânea. Quando houver automação comprovada, informe o gatilho real e seu alcance.

Se a pessoa colou só o link, leia README e catálogo e mostre a mensagem curta. O link isolado não autoriza publicar, conectar contas ou instalar programas. Se pediu instalação, execute o que já foi autorizado.

## Como interpretar os comandos diretos

- **Começar:** o assistente baixa o restante do repositório, instala as skills e executa as configurações autorizadas, seguindo o primeiro uso e o tutorial. Não delegue os comandos técnicos ao iniciante quando puder executá-los. Se alguma etapa precisar do login ou de uma permissão da pessoa, avise e continue depois. Preserve a checagem de compatibilidade e acesso local.
- **Aprovar skills:** mostre o pacote e o hash de cada versão que o responsável já declarou pronta. Skills ainda em desenvolvimento continuam fora dessa decisão. A frase abre a revisão; não é aprovação coletiva. Para cada decisão, apresente `APROVO <nome-da-skill> <hash-completo>` e registre com `approve_skill.py` somente depois de receber a confirmação humana correspondente. Não execute marcadores literais como dados reais.
- **Subir para o GitHub:** use o tutorial para testes, política e envio. O script atual é `python scripts/library.py sync --push` na máquina publicadora configurada. Qualquer pendência bloqueadora deve ser informada; não omita skills para publicar nem contorne a trava. Confira os commits remotos.
- **Atualizar minhas skills:** use o tutorial para receber nos clones e instalar sem perder edições locais. Não confunda isso com o comando de envio.

Apresente comandos em linguagem natural ao iniciante. Mostre comandos de terminal somente durante a execução ou quando solicitados. Uma skill orienta a IA; não treina o modelo nem transfere contas, ferramentas ou permissões.

## Tour do que existe de verdade

Consulte `README.md`, `catalog.json`, `CATALOGO.md` e `external-sources.json` dos repositórios acessíveis. Comece por nomes, descrições e categorias; abra o corpo de uma skill apenas quando for usá-la. Não copie uma lista antiga nem leia todas as skills para montar o tour.

Agrupe o material por tarefas compreensíveis, como planejar um trabalho, desenvolver uma página, produzir vídeo ou organizar documentos, **somente quando houver entradas correspondentes no catálogo/manifesto lido**. Quando a pessoa pedir o tour detalhado, mostre até três exemplos relevantes ao trabalho informado; se ainda não souber a função da pessoa, ofereça opções do catálogo sem travar a configuração. Para cada exemplo, explique o resultado possível, uma frase de pedido e seu estado neste computador.

Distinga explicitamente:

| Estado | Explicação para quem está começando |
| --- | --- |
| Disponível no repositório | A biblioteca lista o recurso; ainda precisamos conferir a instalação. |
| Instalado e localizado pela IA | A receita foi encontrada; sua execução ainda pode depender de ferramentas e arquivos. |
| Externo ou de plugin | Vem de outro fornecedor; instalar pela fonte oficial e conectar a própria conta quando necessário. |
| Bloqueado ou não testado | Falta acesso, compatibilidade, ferramenta ou teste; diga exatamente qual. |

Não anuncie recursos do repositório privado sem leitura autorizada. Sem esse acesso, o tour e o uso do público podem continuar. Quantidades e nomes de skills mudam; derive-os da leitura atual. Mostre capacidades de acordo com as ferramentas realmente disponíveis nesta sessão, sem prometer execução só porque existe uma receita.

## Configuração no computador da pessoa

Os destinos oficiais são [skills-redoma](https://github.com/ARedomaDigital/skills-redoma), geral e público, e [skills-equipe](https://github.com/ARedomaDigital/skills-equipe), interno e privado. Confira remotes e visibilidade antes de publicar. Novos envios usam somente esses destinos.

1. Identifique sistema operacional, aplicativo de IA, acesso a arquivos/terminal e pasta pessoal. Se esta IA não operar arquivos locais, explique o limite e ofereça [o prompt para um assistente local](references/primeiro-acesso.md), sem afirmar instalação. Para a rotina dos scripts, confira Git, Python 3.10+ e, no Windows, o fuso `America/Sao_Paulo` e `tzdata`.
2. Cada pessoa usa a própria conta GitHub. Confira leitura dos destinos e escrita apenas para quem contribuirá. O privado exige convite aceito; o link não concede acesso. Não peça senha ou token no chat. Ausência de acesso interno não impede instalar e experimentar o público.
3. Reutilize clones existentes após conferir alterações e remotes. Para clones novos, use a pasta escolhida ou `~/Documents/Redoma`, com `skills-redoma` e `skills-equipe` em pastas irmãs. Clone é uma cópia com histórico; ZIP serve para consulta ou recuperação, sem equivaler a uma configuração de atualização.
4. Localize a skill de nome-base `redoma-tutorial` no catálogo instalado e leia sua `references/operacao.md`. Use os instaladores atuais para as skills próprias aprovadas e fontes externas previstas. Plugins e componentes do aplicativo usam o fornecedor correto. Informe separadamente o que faltou.
5. Na convenção Redoma, consulte `.codex/skills` e `.agents/skills`, mantendo uma única fonte editável por skill. `.agents/skills` é o destino padrão dos scripts atuais. Para outro aplicativo, verifique o mecanismo de leitura suportado; não declare compatibilidade automática. Não copie `.system`, caches, credenciais nem a configuração inteira de outra máquina.
6. Preserve edições locais e recibos. Receber exige conferir status, atualizar o clone sem sobrescrever divergências e só então instalar. Na troca de um nome antigo por um `-mkN`, compare as versões e identifique a antiga; não apague uma pasta local divergente nem deixe duas versões ativas por engano.
7. Confira hashes e recibos, localize uma skill instalada no aplicativo e realize uma pequena tarefa escolhida pela pessoa quando houver material e ferramenta. Registre o que foi instalado, descoberto e efetivamente testado como estados distintos.

Configure automação apenas se solicitada. O padrão da equipe é uma tentativa na primeira mensagem humana do dia, no fuso `America/Sao_Paulo`, e pedidos explícitos. Preserve instruções existentes, adapte caminhos, não crie agendamento por intervalo/login e não duplique hooks. Sem executor validado para receber e instalar, identifique a coordenação pelo assistente e as etapas ainda manuais.

## Primeiro trabalho e como pedir melhor

Depois do tour, ofereça uma ação pequena que use um recurso confirmado. Exemplo, quando uma skill de planejamento estiver disponível: “Tenho este objetivo e estes materiais. Ajude a transformar isso em um plano e execute a primeira etapa possível.” Identifique a skill escolhida e mostre o resultado.

Ensine este modelo de pedido: **o que quero + material de origem + formato da entrega + como vou avaliar**. Pergunte somente pelo dado que muda a execução. Exemplo: “Quero um vídeo de 30 segundos, usando este arquivo, com legendas e formato vertical; confira a leitura no celular.” Use esse exemplo de vídeo somente quando houver a skill correspondente e explique as ferramentas adicionais necessárias.

Explique que a IA carrega as instruções relevantes quando precisa delas; colar a biblioteca inteira em cada conversa gasta contexto sem ajudar. Aponte a skill pelo nome-base, forneça os arquivos certos e dê feedback concreto, como “o texto ficou pequeno no celular”.

## Contribuir sem precisar começar programando

Um integrante pode contribuir relatando uma falha, mostrando um resultado bom e explicando como chegou nele. Ajude a transformar um processo repetível em uma skill original, usando a skill criadora disponível no aplicativo. Se ela não estiver instalada, prepare o relato e informe o que falta. Remova dados pessoais e de clientes do material geral; conteúdo interno vai ao privado. Terceiros permanecem classificados como `external`, com origem/licença verificadas ou limitação declarada.

Para quem quiser contribuir com código, explique que scripts são as pequenas rotinas que executam instalação, testes ou organização. Identifique o arquivo e o problema, preserve mudanças existentes, prepare a alteração e rode os testes documentados. Uma correção de bug deve incluir regressão que reproduza a falha antes e passe depois. Não presuma que toda alteração de código seja uma skill nem lhe aplique um mark sem motivo.

Para skills da equipe, use nome/pasta com `-mk1` na criação e incremente a cada versão; referências em texto usam o nome-base. O fluxo é: rascunho local, teste, pacote revisável, aprovação humana explícita do responsável para o hash exato e envio verificado. Leia `references/aprovacao.md` da skill de tutorial e `hub/SKILLS_EM_REVISAO.md` quando disponíveis nesta máquina. Teste bem-sucedido não autoriza o agente a aprovar. Qualquer edição invalida a aprovação anterior daquela versão.

Use o fluxo de contribuição documentado pelo repositório. Se exigir branch e pedido de revisão, explique esses termos no momento de usá-los. Sem permissão de escrita, prepare a proposta local e indique como entregá-la ao responsável, sem prometer envio. Nunca publique para testar acesso.

## O caminho até os outros computadores

Explique a sequência em palavras: **a pessoa melhora e testa; o responsável aprova; a mudança vai ao GitHub; cada computador recebe e instala; o assistente daquele computador encontra e testa o recurso**.

| Etapa | Evidência necessária |
| --- | --- |
| Preparado aqui | Arquivos, testes e hash da versão revisável. |
| Aprovado para compartilhar | Decisão humana registrada para essa versão. |
| Enviado ao GitHub | Commit remoto conferido em cada destino alterado. |
| Recebido em outro computador | Clone daquele computador na versão esperada. |
| Instalado e utilizável lá | Hash/recibo local, recurso localizado e teste possível no aplicativo daquela pessoa. |

Baixar o repositório uma vez não mantém todos os PCs atualizados. `library.py sync --push` exporta fontes locais e envia; não recebe nem instala sozinho o trabalho dos colegas. Em máquina com biblioteca parcial, não use o exportador sem conferir completude e política: ele reconstrói catálogos. Use o tutorial para recebimento e reconciliação de base/local/remoto; preserve ambas as edições em conflito, sem force push ou exclusões para destravar.

Não declare configuração de outros computadores com base neste. Informe o alcance real da automação e se o aplicativo precisa estar aberto, ter rede e executar a instrução. Falhas devem ter etapa, causa sem credenciais, efeito, próxima ação e caminho do log, conforme o tutorial. Uma tentativa diária pulada após erro não é envio concluído.

## Fechamento útil

Depois de executar, informe em até três tópicos: resultado, pendência acionável e próximo comando. Inclua links, pasta e log apenas se forem necessários à entrega ou exigidos pelas regras locais. Não repita a apresentação nem o tour completo.

Para repassar a biblioteca, forneça [o prompt de primeiro acesso](references/primeiro-acesso.md). Os quatro comandos diretos continuam disponíveis. Execute o que já foi solicitado e não invente autorização para ações externas.
