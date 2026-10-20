# Relatório de documentação — Domínio Serverlesspresso

Gerado a partir de `fixtures/serverless-coffee` (repo `aws-samples/serverless-coffee`, commit `9d494a2`, 2026-07-27). Escopo: repositório inteiro (infraestrutura como código SAM/CDK, 3 pilhas + 4 extensões, ~20 lambdas, 5 state machines, EventBridge). Construído de baixo para cima conforme `references/padrao.md` do skill `sinter-documentar`.

## Itens por camada

| Camada | Itens | `extracted` | `inferred` |
|---|---|---|---|
| 0 — Transversal (glossário, regras, decisão, padrão) | 10 | 6 | 4 |
| 1 — Negócio (capacidade, fluxo macro) | 2 | 0 | 2 |
| 2 — Domínio (README) | 1 | 0 | 1 |
| 3 — Subdomínio + sequência técnica | 5 | 1 | 4 |
| 4 — Sistema (fichas + contratos) | 22 | 20 | 2 |
| 5 — Componente | 28 | 27 | 1 |
| 6 — Infraestrutura (recursos + ambientes) | 19 | 16 | 3 |
| **Total** | **87** | **70** | **17** |

A imensa maioria dos fatos técnicos (infra, componentes, contratos de evento) veio direto do código — `template.yaml`, arquivos `.asl.json`, handlers `.js`. As camadas 1 (negócio) e 2 (domínio) são as mais inferidas, como esperado: não há documento de produto no repositório, só READMEs de instalação.

## Sistemas e componentes mapeados
11 sistemas "core" + 4 extensões: `nucleo-serverlesspresso` (5 componentes), `config-service` (3), `validator-service` (2 + 1 contrato), `order-processing-service` (1 + 4 contratos), `order-manager-service` (6 + 3 contratos), `publisher-service` (3), `order-journey-service` (2), `counting-service` (2, **órfãos**), `metrics-service` (4), mais 4 extensões documentadas em nível de ficha (event-player, order-robot, persist-metrics-dynamodb, wait-times).

## Fluxo de pedido de café
Documentado de ponta a ponta em `fluxos/pedido-de-cafe.md` (negócio) e `fluxos/pedido-de-cafe.sequencia.md` (técnico, com diagrama `sequenceDiagram` cobrindo os 2 caminhos felizes e 4 caminhos de erro: token inválido, loja/fila indisponível, timeout do cliente, bebida fora do cardápio, timeout do barista).

## Decisões de organização do repositório (para o avaliador entender escolhas)
- **Sem pastas `mapa/` e `eventos/` na camada 2**: o diagrama de contexto e a tabela de eventos de domínio já estão completos em `README.md`; o contrato técnico de cada evento vive em `sistemas/<produtor>/contratos/`, para não duplicar a mesma informação em dois lugares (princípio "um lugar por informação" do skill).
- Cada state machine (Step Functions) foi modelada como **componente tipo `job`** (camada 5), não como recurso de infraestrutura — ela tem gatilho, entrada e saída bem definidos, como uma lambda.
- APIs com integração direta API Gateway → DynamoDB/Step Functions (sem lambda) foram modeladas como **um componente tipo `endpoint` por sistema** (agrupando as rotas), em vez de um arquivo por rota, para não fragmentar demais um comportamento simples.

## Conflitos encontrados (não resolvidos sozinho — registrados para decisão humana)
1. **`OrderProcessor.orderFinished` não distingue conclusão de cancelamento** — o ASL do `order-processing-service` emite o mesmo evento final tanto quando o barista completa quanto quando cancela (`backends/4-order-processing/statemachine/op.asl.json`, states `Pass`→`Emit - order finished`). Ver `sistemas/order-processing-service/contratos/order-processor-order-finished.md`.
2. **Duas topologias de implantação coexistem**: a pilha consolidada `01-appCore` (caminho oficial do README) e templates standalone completos em `backends/7-metrics-service`, `backends/8-order-journey` e `backends/9-validator` (usam SSM Parameter Store do core). O `validator-service` standalone usa HTTP API + JWT authorizer manual; a versão consolidada usa REST API + Cognito User Pools authorizer — **arquiteturas de autenticação diferentes para o mesmo serviço**. Ver `infraestrutura/ambientes/modulos-standalone-backends.md` e `sistemas/validator-service/ficha.md`.
3. **`metrics-service` não é implantado pelo caminho documentado** (`01-appCore` não o inclui), então as métricas de CloudWatch dele provavelmente não existem em uma instalação seguindo só o README raiz.
4. **`counting-service` (`backends/1-counting-service/code/`) é código órfão**: nenhum `template.yaml` no repositório implanta `getOrderId.js`/`resetOrderId.js`. A contagem real acontece dentro do ASL do `order-processing-service`, usando uma chave (`orderID-{eventId}`) diferente da que o código órfão usa (`orderID` fixo).
5. **`backends/4-order-processing/functions/capacity/isCapacityAvailable.js` e `functions/resumeWF/app.js`** também parecem órfãos: o `op.asl.json` real faz a checagem de capacidade com um state `ListExecutions` direto, não invocando essas lambdas.
6. **`backends/4-order-processing/api.yaml`** descreve uma HTTP API que publica `OrderProcessor.OrderStarted` direto no bus — mas o `OrderProcessorStateMachine` real é iniciado por `Validator.NewOrder`, e não há recurso `HttpApi` em `01-appCore/template.yaml` usando esse `api.yaml`. Parece um ponto de entrada alternativo/legado, não conectado.

## Segredos encontrados
Nenhum segredo, chave ou senha em texto plano foi encontrado. Notas:
- `GenerateSecret: false` no `UserPoolClient` (`00-baseCore/template.yaml`) — não há client secret a proteger.
- O termo `apiKey` aparece como **tipo de security scheme do OpenAPI** em `backends/5-order-manager/RestAPIs/api.yaml` e `backends/2-config-service/RestAPIs/api.yaml`, mas a autorização real é `cognito_user_pools` — não é uma API key literal.

## Perguntas para as pessoas

### Para o PM
- Quem é o dono/time responsável hoje por este domínio (o repositório é um sample público da AWS)?
- A capacidade "Vender café sob demanda" e os indicadores propostos (tempo médio de preparo, taxa de cancelamento, utilização de capacidade) fazem sentido, ou existem outros indicadores de negócio que devem substituir os propostos?
- O limite de 20 pedidos simultâneos e as janelas de 5/15 minutos são parâmetros de negócio reais ou apenas valores de demonstração do workshop?

### Para o arquiteto
- Qual topologia de implantação é a "oficial": só `01-appCore`, ou os módulos standalone (`7-metrics-service`, `8-order-journey`, `9-validator`) rodando lado a lado/substituindo partes dela? (conflito 2)
- `metrics-service` deveria ser incluído em `01-appCore`? Hoje ele não é implantado pelo caminho documentado (conflito 3).
- O evento `OrderManager.Order{eventId}-COMPLETED`/`-CANCELLED` (com o `eventId` embutido no nome do `detail-type`) é intencional? Isso impede regras EventBridge simples por `prefix` fixo.
- `backends/4-order-processing/api.yaml` (HTTP API → EventBridge `OrderProcessor.OrderStarted`) ainda é um ponto de entrada válido, ou é código morto a remover? (conflito 6)

### Para o tech lead
- `backends/1-counting-service/code/*` e `backends/4-order-processing/functions/{capacity,resumeWF}/*` podem ser removidos com segurança (órfãos, sem `template.yaml` que os implante)? (conflitos 4 e 5)
- `OrderProcessor.ShopUnavailable` não tem consumidor lambda identificado no código — algum front-end trata esse evento, ou ele só é usado pelo `order-journey-service` (que grava todo evento) e pelo `publisher-service`?
- É aceitável que "bebida fora do cardápio" (state `Is Order Valid?` no `om.asl.json`) termine em `Succeed` silencioso, deixando o `order-processing-service` esperando até o timeout de 5 minutos sem avisar o cliente do motivo?
- As funções `get-qr-code`/`ddb.js` do validator engolem erros de DynamoDB com `console.error` sem propagar exceção — isso é aceitável ou deveria falhar explicitamente (hoje pode devolver um bucket vazio silenciosamente)?
- O limite de capacidade "20" está como índice de array hardcoded no ASL (`$.isCapacityAvailable[20]`) em vez de parâmetro nomeado — vale a pena refatorar para uma variável de ambiente/`DefinitionSubstitutions`?

## Como continuar
- Repositório em `dominio-serverlesspresso/`, pronto para revisão humana (todo item `status: proposed`).
- Próxima rodada, se aprovada a abordagem: aprofundar os 4 sistemas de extensão (hoje só fichas) com componentes detalhados, e resolver as perguntas acima antes de promover os itens para `status: approved`.
