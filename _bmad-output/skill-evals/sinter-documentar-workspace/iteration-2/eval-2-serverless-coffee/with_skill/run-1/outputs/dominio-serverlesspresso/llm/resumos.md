# Serverlesspresso: resumos

Degrau 1. Cada página e cada seção de serviço e de jornada em poucas linhas. Para o detalhe, abra a seção indicada.

## Negócio (1-negocio.md)
uma cafeteria de eventos (pop-up, tipo re:Invent) em que o cliente pede café pelo celular escaneando um QR code no balcão, e o barista prepara na ordem em que os pedidos chegam. O domínio controla quem pode pedir, quantos pedidos cabem ao mesmo tempo, e acompanha cada pedido do QR code até um recibo final — sem fila física e sem dinheiro trocando de mãos no sistema.

Parede do domínio:
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Admin | Abre a loja e publica o cardápio do evento | Loja configurada | Pedido só é aceito com a loja aberta |
| 2 | Cliente | Escaneia o QR code do balcão | Pedido iniciado | Só se houver token livre na janela de 5 min (10 por padrão) |
| 3 | Sistema | Confere se a loja está aberta e há vaga | Loja indisponível *ou* pedido aceito | No máx. 20 pedidos em andamento ao mesmo tempo |
| 4 | Cliente | Escolhe a bebida e envia | Pedido registrado com número | Expira em 5 min se não enviar; bebida precisa constar do cardápio |
| 5 | Barista | Assume, prepara e conclui (ou cancela) | Pedido em preparo → concluído *ou* cancelado | Expira em 15 min se o barista não agir; cliente é avisado na hora |
| 6 | Sistema | Fecha o pedido e monta o recibo | Pedido finalizado | Recibo em HTML com a trilha completa de eventos |

## Arquitetura (2-arquitetura.md)
um único event bus do EventBridge (`Serverlesspresso`) conecta nove serviços serverless; dois deles são máquinas de Step Functions que se revezam para orquestrar o pedido, o resto é coreografia por eventos (nome do evento como contrato). Nada é síncrono entre serviços, exceto as chamadas REST que vêm de fora (dos 3 frontends) e o par de `SendTaskSuccess` que liga as duas máquinas de estado.

## Serviços (3-servicos.md)
nove serviços na stack principal (mais quatro extensões opcionais), quase todos Lambda + EventBridge; dois deles são máquinas de estado do Step Functions que cooperam para tocar o pedido do início ao fim. Cada seção lista os lambdas daquele serviço um a um, o contrato que expõe e os eventos que produz/consome.

- **00-baseCore** (3-servicos.md#00-basecore): stack fundacional: cria o event bus `Serverlesspresso`, o Cognito User Pool com login por SMS (sem senha) e o endpoint IoT usado para tempo real. Todo o resto depende dela.
- **validator-service (`backends/9-validator`)** (3-servicos.md#validator-service-backends9-validator): é o portão de entrada do pedido: gera um QR code com token limitado por janela de 5 minutos e, quando o cliente escaneia, valida o token e dispara `Validator.NewOrder` — o evento que dá partida em tudo.
- **config-service (`backends/2-config-service`)** (3-servicos.md#config-service-backends2-config-service): guarda a configuração de cada evento pop-up (loja aberta/fechada, cardápio, limites) numa única tabela e propaga qualquer mudança para o resto do domínio via EventBridge.
- **order-processor (`backends/4-order-processing`)** (3-servicos.md#order-processor-backends4-order-processing): a máquina de estado que carrega o pedido do início ao fim. Não tem lambda própria: fala direto com DynamoDB e EventBridge, e pausa duas vezes esperando uma ação humana (cliente escolher a bebida, barista concluir), usando o padrão *waitForTaskToken*.
- **order-manager (`backends/5-order-manager`)** (3-servicos.md#order-manager-backends5-order-manager): a segunda máquina de estado: recebe, via API Gateway, a bebida escolhida pelo cliente e as ações do barista (assumir, liberar, concluir, cancelar), grava tudo na tabela de pedidos e é quem efetivamente "acorda" o order-processor com `SendTaskSuccess`.
- **publisher-service (`backends/6-publisher-service`)** (3-servicos.md#publisher-service-backends6-publisher-service): três lambdas puramente "escuta o bus, publica no IoT" — é assim que os 3 frontends recebem atualização em tempo real sem dar polling nas APIs.
- **order-journey-service (`backends/8-order-journey`)** (3-servicos.md#order-journey-service-backends8-order-journey): não orquestra nada — é um espectador que grava *todo* evento do domínio numa tabela própria e, quando vê o pedido terminar, monta um recibo em HTML e publica no S3/CloudFront.
- **metrics-service (`backends/7-metrics-service`)** (3-servicos.md#metrics-service-backends7-metrics-service): stack separada, opcional: quatro lambdas que só transformam evento em métrica do CloudWatch, para dashboards operacionais.
- **counting-service (`backends/1-counting-service`, não usado)** (3-servicos.md#counting-service-backends1-counting-service-não-usado): código presente no repositório (`getOrderId.js`, `resetOrderId.js`), mas sem `template.yaml` e sem nenhuma referência em outra stack. A geração do número do pedido hoje acontece dentro do próprio `order-processor` (estado `Generate Order Number`).
- **EventPlayer (`extensions/EventPlayer`)** (3-servicos.md#eventplayer-extensionseventplayer): Step Functions que reproduz ~15 minutos de eventos reais no bus, para testar extensões sem precisar operar a loja de verdade.
- **OrderRobotExtension (`extensions/OrderRobotExtension`)** (3-servicos.md#orderrobotextension-extensionsorderrobotextension): duas máquinas de estado (`orderBot`, `baristaBot`) que simulam clientes e baristas em massa (parâmetro `orders`) — é a origem do campo `robot` nas linhas da `OrderTable`.
- **PersistOrderMetricsToDynamoDB (`extensions/PersistOrderMetricsToDynamoDB`)** (3-servicos.md#persistordermetricstodynamodb-extensionspersistordermetricstodynamodb): fila SQS + Lambda + DynamoDB dedicados a guardar histórico de `OrderManager.WaitingCompletion` para análise posterior (a fila absorve picos de eventos).
- **WaitTimes (`extensions/WaitTimes`)** (3-servicos.md#waittimes-extensionswaittimes): único componente em CDK/TypeScript do repositório; escuta pedido enviado/concluído e calcula o tempo médio de espera por bebida.

## Jornadas (4-jornadas.md)
duas jornadas. A principal é **Pedir um café**: do QR code escaneado no balcão até o recibo em HTML, orquestrada por duas máquinas de Step Functions que se revezam via *task token*. A segunda é **Configurar o evento**: como o admin abre/fecha a loja e muda o cardápio, e como isso se propaga sem nenhum orquestrador — por coreografia de eventos.

- **Pedir um café** (4-jornadas.md#pedir-um-café): o cliente escaneia um QR code liberado pelo balcão, escolhe a bebida, o barista prepara e conclui, e um recibo é gerado no fim. O pedido nunca fica "girando": ele existe como duas pausas de uma máquina de estados, acordadas por eventos quando alguém age.
- **Configurar o evento** (4-jornadas.md#configurar-o-evento): o admin abre/fecha a loja e ajusta o cardápio direto na tabela de configuração; qualquer mudança se propaga sozinha para quem precisar saber, sem ninguém "chamando" ninguém.

## Infraestrutura (5-infraestrutura.md)
tudo roda em `us-east-1` só como AWS SAM/CloudFormation, sem Kubernetes nem contêineres: Lambda (Node.js 14.x quase toda), duas máquinas de estado do Step Functions, um event bus próprio do EventBridge, quatro tabelas DynamoDB, uma API Gateway REST por serviço, Cognito com fluxo de login por SMS e AWS IoT Core para tempo real. Não há ambientes dev/homologação distintos: o próprio template é reimplantado em qualquer conta/região que o operador escolher.

## Referência (6-referencia.md)
glossário, regras, decisões reconstruídas, padrões de código e um guia rápido para rodar o projeto localmente. A seção mais importante para quem for mexer aqui é "Dúvidas e perguntas": lista o código órfão encontrado e os conflitos entre a config e o código.

