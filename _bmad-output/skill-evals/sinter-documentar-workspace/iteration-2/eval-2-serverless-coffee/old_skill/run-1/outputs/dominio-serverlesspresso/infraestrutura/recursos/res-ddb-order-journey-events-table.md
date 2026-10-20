---
id: res-ddb-order-journey-events-table
kind: resource
subject: resource:dynamodb-table:OrderJourneyEventsTable
camada: 6
status: proposed
realiza: [sys-order-journey-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L142-L157"
    version: 9d494a2
    extraction: extracted
---
# DynamoDB "OrderJourneyEventsTable"
| Campo | Valor |
|---|---|
| Tipo | banco (log de eventos) |
| Tecnologia | Amazon DynamoDB, `PAY_PER_REQUEST`, Streams (`NEW_AND_OLD_IMAGES`, sem consumidor do stream identificado) |
| Ambientes | consolidado (01-appCore) |
| Definido em | `01-appCore/template.yaml` |

## Usado por
- order-journey-service (grava todo evento do domínio; consulta ao montar a página HTML)
