---
id: cmp-order-processor-state-machine
kind: component
subject: component:order-processing-service:order-processor-state-machine
camada: 5
status: proposed
realiza: [sys-order-processing-service]
realizado-por: [res-ddb-config-table, res-ddb-counting-table, res-event-bus-serverlesspresso]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json"
    version: 9d494a2
    extraction: extracted
---
# order-processor-state-machine
State machine (Standard) que controla todo o ciclo de vida do pedido do lado do cliente até a entrada na fila do barista, e é retomada até o fim do pedido.

| Campo | Valor |
|---|---|
| Tipo | job (Step Functions Standard Workflow) |
| Gatilho | Regra EventBridge `Validator.NewOrder` aponta direto para a state machine (`Events.ValidatorNewOrder` no SAM) — não há lambda entre o evento e o SFN |
| Entrada | `$.detail.{orderId, userId, bucket.eventId}` do evento `Validator.NewOrder` |
| Saída | Nenhuma (state machine `End: true` em cada ramo); efeitos são via `events:putEvents` e updates diretos no DynamoDB |
| Timeout / memória / concorrência | Sem `TimeoutSeconds` global; dois `waitForTaskToken` com heartbeat de 300 s e 900 s |

## Dependências
- `ConfigTable` — `dynamodb:GetItem`/`UpdateItem` (loja aberta, cardápio)
- `CountingTable` — `dynamodb:UpdateItem` (gera `orderNumber`)
- EventBridge `Serverlesspresso` — `events:PutEvents` (5 tipos de evento distintos)
- Ela mesma via `states:ListExecutions` (checagem de capacidade)
- `order-manager-service` chama de volta via `states:SendTaskSuccess` (permissão concedida à role do order-manager-state-machine, não ao contrário)

## Erros e retentativas
- `Catch States.Timeout` em ambos os `waitForTaskToken` → emite `OrderProcessor.OrderTimeOut` e termina
- Sem `Retry` configurado nos states de `putEvents`/`dynamodb` desta state machine (diferente do order-manager, que tem retry na chamada de lambda)
