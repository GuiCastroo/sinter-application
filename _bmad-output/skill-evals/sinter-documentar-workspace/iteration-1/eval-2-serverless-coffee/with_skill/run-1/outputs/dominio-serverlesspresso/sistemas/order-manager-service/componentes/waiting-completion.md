---
id: cmp-order-manager-waiting-completion
kind: component
subject: component:order-manager-service:waiting-completion
camada: 5
status: proposed
realiza: [sys-order-manager-service]
realizado-por: [res-ddb-order-table, res-event-bus-serverlesspresso]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/functions/waitingCompletion/app.js"
    version: 9d494a2
    extraction: extracted
---
# waiting-completion
Grava o número do pedido e o novo Task Token (o que vai destravar o barista) e avisa o resto do sistema que o pedido está na fila, pronto para ser preparado.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Evento EventBridge `detail-type` com prefixo `OrderProcessor.WaitingCompletion` |
| Entrada | `event.detail.{orderId, userId, TaskToken, orderNumber, eventId}` |
| Saída | Publica `OrderManager.WaitingCompletion` no bus |
| Timeout / memória / concorrência | 15 s / 128 MB |

## Dependências
- `serverlesspresso-order-table` — `UpdateItem` condicionado a `USERID` bater (`ConditionExpression`)
- EventBridge `Serverlesspresso` — publica o evento consumido por publisher, journey, métricas e extensões

## Erros e retentativas
Se a condição (`USERID` diferente) falhar, o `UpdateItem` lança e não há `Retry` configurado — a mensagem é perdida (sem DLQ na regra do EventBridge).
