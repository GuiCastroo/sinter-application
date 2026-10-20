---
id: cmp-order-manager-order-timed-out
kind: component
subject: component:order-manager-service:order-timed-out
camada: 5
status: proposed
realiza: [sys-order-manager-service]
realizado-por: [res-ddb-order-table]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/functions/OrderTimedOut/app.js"
    version: 9d494a2
    extraction: extracted
---
# order-timed-out
Marca o pedido como cancelado quando o cliente ou o barista estouram o tempo limite no `order-processing-service`.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Evento EventBridge `detail-type` com prefixo `OrderProcessor.OrderTimeOut` |
| Entrada | `event.detail.{orderId, eventId, cause}` |
| Saída | Nenhuma (grava e termina) |
| Timeout / memória / concorrência | 15 s / 128 MB |

## Dependências
- `serverlesspresso-order-table` — `UpdateItem` (`ORDERSTATE={eventId}-CANCELLED`, `reason=cause`)

## Erros e retentativas
Sem `Retry`/DLQ configurados.
