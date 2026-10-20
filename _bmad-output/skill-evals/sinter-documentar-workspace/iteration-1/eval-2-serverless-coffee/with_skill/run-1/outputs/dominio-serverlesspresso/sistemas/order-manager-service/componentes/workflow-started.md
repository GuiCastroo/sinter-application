---
id: cmp-order-manager-workflow-started
kind: component
subject: component:order-manager-service:workflow-started
camada: 5
status: proposed
realiza: [sys-order-manager-service]
realizado-por: [res-ddb-order-table]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/functions/workflowStarted/app.js"
    version: 9d494a2
    extraction: extracted
---
# workflow-started
Cria o registro inicial do pedido assim que o `order-processing-service` sinaliza que está esperando o cliente montar a bebida.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Evento EventBridge `detail-type` com prefixo `OrderProcessor.WorkflowStarted` |
| Entrada | `event.detail.{orderId, userId, TaskToken, eventId, robot}` |
| Saída | Nenhuma (grava e termina) |
| Timeout / memória / concorrência | 15 s / 128 MB |

## Dependências
- `serverlesspresso-order-table` — `PutItem` (`PK=orders`, `SK=orderId`, `ORDERSTATE={eventId}-CREATED`, `TaskToken`)

## Erros e retentativas
Sem `Retry`/DLQ configurados na regra do EventBridge nem na função.
