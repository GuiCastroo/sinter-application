# 2. Catálogo de Lambdas

Todas as funções Lambda do repositório (Node.js 14.x, `aws-sdk` v2), agrupadas pelo serviço a que
pertencem. Para cada uma: **gatilho**, **o que faz**, **entrada/saída relevantes** e
**efeitos colaterais** (o que ela lê/grava/publica).

Legenda de gatilho: 🌐 API Gateway · 📬 regra EventBridge · 🔀 tarefa de Step Functions ·
🗄️ DynamoDB Stream · 🔑 gatilho do Cognito · 🏗️ Custom Resource (CloudFormation).

---

## 00-baseCore — Autenticação e bootstrap de infra

### `GetIoTEndpointFunction` — `00-baseCore/GetIoTEndpoint.js`
🏗️ Custom Resource, chamado uma vez no deploy.
Chama `iot:DescribeEndpoint` e devolve o endpoint de dados do IoT Core para o CloudFormation
expor como output (`IotEndpointAddress`), consumido pelos frontends para abrir a conexão MQTT.

### `DefineAuthChallenge` — `cognito-triggers/define-auth-challenge.js`
🔑 Cognito **Define Auth Challenge** trigger.
Máquina de estados do fluxo de login sem senha: decide se emite tokens, falha a autenticação
(após ≥3 tentativas erradas) ou repete o desafio `CUSTOM_CHALLENGE`. Também contorna um bug
conhecido do SDK iOS que reenvia `SRP_A` em vez de `CUSTOM_CHALLENGE`.

### `CreateAuthChallenge` — `cognito-triggers/create-auth-challenge.js`
🔑 Cognito **Create Auth Challenge** trigger.
Gera um código OTP de 6 dígitos (`crypto-secure-random-digit`) e envia por **SMS via SNS** para o
`phone_number` do usuário. Em tentativas subsequentes da mesma sessão, reaproveita o código já
enviado (extraído do `challengeMetadata`) em vez de gerar um novo.

### `VerifyAuthChallengeResponse` — `cognito-triggers/verify-auth-challenge-response.js`
🔑 Cognito **Verify Auth Challenge Response** trigger.
Compara a resposta do usuário (`challengeAnswer`) com o `passCode` esperado; simples igualdade
de string.

### `PreSignUp` — `cognito-triggers/pre-sign-up.js`
🔑 Cognito **Pre Sign-up** trigger.
Sempre `autoConfirmUser = true` e `autoVerifyPhone = true` — dispensa o fluxo padrão de
confirmação, já que o próprio OTP de login cumpre esse papel.

### `FillDatabasesCustomResource` — `01-appCore/initDB/app.js` (+ `initMenu.js`)
🏗️ Custom Resource (`Create`/`Update`/`Delete`).
Em `Create`/`Update`, chama `initMenu()`, que faz um `BatchWriteItem` carregando
`initMenuState.JSON` em `ConfigTable` (cardápio + config inicial) e `initCountingState.JSON` em
`CountingTable` (contadores zerados). Implementa manualmente o protocolo de resposta
pré-assinada do CloudFormation (`sendResponse` via HTTPS PUT).

---

## 8-order-journey

### `GenerateHtml` — `functions/GenerateHtml/app.js`
🔀 Tarefa da `OrderJourneyService` state machine (state **"Generate HTML"**).
Recebe o resultado de uma DynamoDB `Query` (todos os eventos daquele `orderId`, já ordenados) e
monta, em memória, uma página HTML de linha do tempo ("order journey"): um bloco por evento
(título amigável extraído do `detail-type`, mensagem, timestamp), escolhe a imagem do diagrama do
Step Functions (sucesso vs. cancelamento) e adiciona um botão de compartilhar no Twitter. Devolve
`{ html, fileName }`; a state machine grava esse HTML no S3 no state seguinte ("Save to S3").
⚠️ **Nota**: as URLs de assets estáticos (CSS/JS/imagens) estão *hardcoded* para um bucket
específico (`serverlesspresso-order-journey-journeybucket-1lc9wg7eac1f4.s3.us-west-2...`), não
para o bucket real criado pela stack (`JourneyBucket`) — só funciona porque aquele bucket
específico do ambiente de referência da AWS ainda hospeda os assets estáticos.

---

## 6-publisher-service — ponte EventBridge → IoT Core (MQTT)

Três funções quase idênticas: recebem um evento do EventBridge e o republicam em um tópico MQTT
do IoT Core, para que os frontends (inscritos via WebSocket/MQTT) recebam updates sem fazer
polling.

### `PublisherFunctionAdmin` — `code/publishToIOT.js`
📬 Regra: `detail-type` com prefixo `OrderManager.` / `OrderProcessor.` / `Validator.` /
`ConfigService.`.
Publica em `serverlesspresso-admin-<eventId>` — canal do **dashboard do barista/admin**.

### `PublisherFunctionUser` — `code/publishToIOTuserTopic.js`
📬 Regra: prefixo `OrderManager.` ou `OrderProcessor.`.
Publica em `serverlesspresso-user-<userId>` — canal **por cliente**, para o app do cliente ver o
status do seu próprio pedido em tempo real.

### `PublisherFunctionConfig` — `code/publishToIOTconfig.js`
📬 Regra: prefixo `ConfigService.`.
Publica em `serverlesspresso-config-<eventId>`. O `eventId` aqui é extraído de forma diferente das
outras duas: vem do `NewImage.PK.S` do stream do DynamoDB (formato `config-<eventId>`), fazendo
`split('-')[1]`.

---

## 2-config-service

### `ConfigChangedFunction` — `code/configChanged.js`
🗄️ DynamoDB Stream de `ConfigTable` (`BatchSize: 1`, `TRIM_HORIZON`).
A cada alteração na tabela (ex.: barista abre/fecha a loja via `PUT /store`, ou atualização de
cardápio), publica `ConfigService.ConfigChanged` no EventBridge com o `NewImage` completo. É o
único produtor de eventos do serviço — não expõe lógica de negócio própria, só *observa* mudanças
feitas diretamente pela API Gateway na tabela.

---

## 9-validator

### `GetQRcodeFunction` — `code/getCode.js`
🌐 `GET /qr-code` (exige grupo Cognito `admin`, checado manualmente em
`requestContext.authorizer.claims['cognito:groups']`).
Gera (ou reaproveita) um **token rotativo por janela de 5 minutos** (`TIME_INTERVAL`) por evento:
calcula um `bucket` (`PK = <eventId>-<timeBucketId>`), e se ainda não existir na `ValidatorTable`
para essa janela, cria um novo com `nanoid(CodeLength)` como código e `availableTokens` copiado do
`drinksPerBarcode` do `ConfigTable`. Esse `bucket` é o que vira o QR code exibido no balcão.

### `VerifyQRcodeFunction` — `code/verifyCode.js`
🌐 `POST /qr-code` (Cognito).
Recalcula o `bucket` da janela de 5 min atual, valida que o `token` enviado bate com
`bucket.last_code` e que ainda há `availableTokens`. Se válido: decrementa o contador
(`decrementToken`), gera um novo `orderId` (`nanoid()`), extrai o `userId` do JWT (`sub`) e
**emite `Validator.NewOrder`** no EventBridge — este é o **evento que dispara toda a jornada do
pedido** (ver [`04-fluxo-pedido-sequencia.md`](./04-fluxo-pedido-sequencia.md)).

### `ddb.js` (módulo compartilhado, não é um handler)
Funções utilitárias de acesso a `ApplicationTable`/`ValidatorTable`: `getConfig`, `getItem`,
`saveItem`, `decrementToken` — usadas pelas duas funções acima.

---

## 5-order-manager

### `SanitizeOrderLambda` — `functions/sanitize/app.js`
🔀 Tarefa da `OrderManagerStateMachine` (state **"Sanitize order"**).
Recebe o pedido (`event.body`, com `drink` + `modifiers`) e o cardápio (`event.menu.Item`, ainda
no formato bruto do DynamoDB, "unwrapped" com `dynamodb-data-types`). Confere se a bebida existe no
cardápio e se cada modificador pedido está entre as `Options` permitidas para aquela bebida.
Retorna `true`/`false`. ⚠️ **Nota**: não há checagem de nulidade em `order.modifiers` antes do
`.map()` — se o app cliente enviar um pedido sem o campo `modifiers`, a função lança exceção em
vez de devolver `false`; o state `Sanitize order` da state machine tem `Retry` configurado para
erros de serviço/infra do Lambda, mas não trata esse tipo de erro de payload.

### `WorkFlowStarted` — `functions/workflowStarted/app.js`
📬 Regra: `detail-type` com prefixo `OrderProcessor.WorkflowStarted`.
Cria o registro inicial do pedido em `OrderTable`: `PK="orders"`, `SK=orderId`,
`USERID`, `ORDERSTATE=<eventId>-CREATED`, `TaskToken` (o task token do Step Functions do Order
Processor, guardado para ser usado depois via `sendTaskSuccess`), `robot` (flag opcional).

### `WaitingCompletion` — `functions/waitingCompletion/app.js`
📬 Regra: `detail-type` com prefixo `OrderProcessor.WaitingCompletion`.
Atualiza o registro do pedido com o **novo** `TaskToken` e o `orderNumber` gerado pelo Order
Processor (condicionado a `USERID` bater, evitando overwrite cruzado). Em seguida emite
`OrderManager.WaitingCompletion` com o pedido completo (drinkOrder, estado, etc.) — este evento é
consumido pelo `PublisherFunctionUser/Admin` (realtime) e pelo `OrderManagerWaitingCompletionFunction`
do serviço de métricas.

### `OrderTimedOut` — `functions/OrderTimedOut/app.js`
📬 Regra: `detail-type` com prefixo `OrderProcessor.OrderTimeOut`.
Marca o pedido como `<eventId>-CANCELLED` em `OrderTable`, gravando o `cause` (motivo do timeout,
ex. "Customer timedout"/"Barista timedout") e o timestamp.

---

## 4-order-processing — funções presentes no repo mas **não usadas** na stack consolidada

Estas duas funções existem em `backends/4-order-processing/functions/`, com seu próprio
`env.json`/`template.yaml` de teste local, mas **a state machine consolidada (`op.asl.json`)
implementa a mesma lógica diretamente em Amazon States Language**, sem chamá-las. Prováveis
sobras de uma versão anterior/alternativa do workshop — documentadas aqui porque fazem parte do
repositório e podem confundir quem está lendo o código pela primeira vez.

### `isCapacityAvailable` — `functions/capacity/isCapacityAvailable.js`
Chamaria `stepFunctions.listExecutions` e compararia contra `MaxQueueCapacity` para decidir se
ainda há vaga na fila. **Equivalente implementado na ASL**: states `ListExecutions` +
`Is capacity available?` em `op.asl.json`.

### `resumeWF` — `functions/resumeWF/app.js`
Chamaria `stepfunctions.sendTaskSuccess` dado `orderId`+`TaskToken` de um evento.
**Equivalente implementado na ASL**: states `Resume Order Processor - customer` /
`Resume Order Processor - Barista` em `om.asl.json`, que chamam
`arn:aws:states:::aws-sdk:sfn:sendTaskSuccess` diretamente, sem Lambda.

---

## 1-counting-service — idem, código presente mas superado pela ASL

### `getOrderId` — `code/getOrderId.js`
Incrementaria atomicamente `IDvalue` em `CountingTable` (`PK='orderID'`) e devolveria o
`orderNumber`. **Na stack consolidada**, o state **"Generate Order Number"** do
`OrderProcessorStateMachine` faz o mesmo `UpdateItem` diretamente via integração nativa do Step
Functions com o DynamoDB (chave `orderID-<eventId>`, não `orderID` fixo como nesta versão
standalone).

### `resetOrderId` — `code/resetOrderId.js`
Utilitário administrativo/de demo: zera o contador (`IDvalue = 0`). Não tem gatilho declarado
(nenhum `template.yaml` na pasta) — é invocado manualmente (ex. `localTest.js`) entre
demonstrações.

---

## 7-metrics-service — publica métricas no CloudWatch

Stack standalone (`template.yaml` próprio), 4 Lambdas praticamente idênticas: todas assinam um
`detail-type` específico e escrevem 1 (ou mais) pontos de métrica com
`cloudWatch.putMetricData`, namespace `${AppName}-dev`.

### `ValidatorNewOrderFunction` — `code/ValidatorNewOrder.js`
📬 `detail-type` prefixo `Validator.NewOrder`.
Publica métrica `Drink` (dimensão `Drink=<nome da bebida>`) e uma métrica `Drink` adicional por
cada modificador pedido (dimensão `Modifier=<modificador>`) — permite ver no CloudWatch quais
bebidas/modificadores são mais pedidos.

### `OrderManagerOrderCancelledFunction` — `code/OrderManagerOrderCancelled.js`
📬 `detail-type` prefixo `OrderManager.OrderCancelled`.
Publica métrica `Order` (dimensão `State=Cancelled`, valor 1).

### `OrderProcessorOrderTimeOutFunction` — `code/OrderProcessorOrderTimeOut.js`
📬 `detail-type` prefixo `OrderProcessor.OrderTimeOut`.
Publica métrica `Order` (dimensão `State=Timeout`, valor 1).

### `OrderManagerWaitingCompletionFunction` — `code/OrderManagerWaitingCompletion.js`
📬 `detail-type` prefixo `OrderManager.WaitingCompletion`.
Publica métrica `Order` (dimensão `State=Started`, valor 1) — nome um pouco enganoso: mede
"pedido aguardando conclusão", usado como proxy de "pedido iniciado".

---

## Tabela-resumo (todas as 25 Lambdas)

| # | Função | Serviço | Gatilho | Grava/Publica em |
|---|---|---|---|---|
| 1 | GetIoTEndpointFunction | baseCore | Custom Resource | Output do CFN |
| 2 | DefineAuthChallenge | baseCore | Cognito | — (controla fluxo) |
| 3 | CreateAuthChallenge | baseCore | Cognito | SNS (SMS) |
| 4 | VerifyAuthChallengeResponse | baseCore | Cognito | — |
| 5 | PreSignUp | baseCore | Cognito | — |
| 6 | FillDatabasesCustomResource | appCore bootstrap | Custom Resource | ConfigTable, CountingTable |
| 7 | GenerateHtml | 8-order-journey | Step Functions | (retorno usado p/ S3 no state seguinte) |
| 8 | PublisherFunctionAdmin | 6-publisher-service | EventBridge | IoT topic `serverlesspresso-admin-*` |
| 9 | PublisherFunctionUser | 6-publisher-service | EventBridge | IoT topic `serverlesspresso-user-*` |
| 10 | PublisherFunctionConfig | 6-publisher-service | EventBridge (via Stream) | IoT topic `serverlesspresso-config-*` |
| 11 | ConfigChangedFunction | 2-config-service | DynamoDB Stream | EventBridge (`ConfigService.ConfigChanged`) |
| 12 | GetQRcodeFunction | 9-validator | API Gateway | ValidatorTable |
| 13 | VerifyQRcodeFunction | 9-validator | API Gateway | ValidatorTable, EventBridge (`Validator.NewOrder`) |
| 14 | SanitizeOrderLambda | 5-order-manager | Step Functions | — (retorna bool) |
| 15 | WorkFlowStarted | 5-order-manager | EventBridge | OrderTable |
| 16 | WaitingCompletion | 5-order-manager | EventBridge | OrderTable, EventBridge (`OrderManager.WaitingCompletion`) |
| 17 | OrderTimedOut | 5-order-manager | EventBridge | OrderTable |
| 18 | isCapacityAvailable | 4-order-processing (não usada) | — | — |
| 19 | resumeWF | 4-order-processing (não usada) | — | Step Functions `sendTaskSuccess` |
| 20 | getOrderId | 1-counting-service (não usada) | — | CountingTable |
| 21 | resetOrderId | 1-counting-service (utilitário) | manual | CountingTable |
| 22 | ValidatorNewOrderFunction | 7-metrics-service | EventBridge | CloudWatch Metrics |
| 23 | OrderManagerOrderCancelledFunction | 7-metrics-service | EventBridge | CloudWatch Metrics |
| 24 | OrderProcessorOrderTimeOutFunction | 7-metrics-service | EventBridge | CloudWatch Metrics |
| 25 | OrderManagerWaitingCompletionFunction | 7-metrics-service | EventBridge | CloudWatch Metrics |

> As Lambdas das **extensões opcionais** (`extensions/`) ficam fora desta contagem por não
> fazerem parte do core do domínio; estão descritas em
> [`03-sistemas.md#extensões-opcionais`](./03-sistemas.md#5-extensões-opcionais).
