---
id: cmp-counting-reset-order-id
kind: component
subject: component:counting-service:reset-order-id
camada: 5
status: proposed
realiza: [sys-counting-service]
realizado-por: [res-ddb-counting-table]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/1-counting-service/code/resetOrderId.js"
    version: 9d494a2
    extraction: extracted
---
# reset-order-id
Zera o contador de pedidos.

| Campo | Valor |
|---|---|
| Tipo | lambda (código presente, **sem `template.yaml` que o implante** — órfão) |
| Gatilho | Desconhecido — provavelmente pensado para acionamento manual/agendado |
| Entrada | Nenhuma |
| Saída | Nenhuma |
| Timeout / memória / concorrência | Não definido (sem template) |

## Dependências
- `CountingTable` — `UpdateItem` (`IDvalue = 0` para `PK='orderID'`)

## Erros e retentativas
N/A — não implantado.
