---
id: cmp-counting-get-order-id
kind: component
subject: component:counting-service:get-order-id
camada: 5
status: proposed
realiza: [sys-counting-service]
realizado-por: [res-ddb-counting-table]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/1-counting-service/code/getOrderId.js"
    version: 9d494a2
    extraction: extracted
---
# get-order-id
Incrementa e devolve o contador de pedidos.

| Campo | Valor |
|---|---|
| Tipo | lambda (código presente, **sem `template.yaml` que o implante** — órfão) |
| Gatilho | Desconhecido — nenhum `Events:` encontrado em templates do repositório |
| Entrada | Nenhuma (ignora o `event`) |
| Saída | `{orderNumber}` |
| Timeout / memória / concorrência | Não definido (sem template) |

## Dependências
- `CountingTable` (via `process.env.TableName`) — `UpdateItem` incrementando `IDvalue` para `PK='orderID'` (chave fixa, sem `eventId` — diferente do que a state machine do order-processing usa hoje, que é `orderID-{eventId}`)

## Erros e retentativas
N/A — não implantado.
