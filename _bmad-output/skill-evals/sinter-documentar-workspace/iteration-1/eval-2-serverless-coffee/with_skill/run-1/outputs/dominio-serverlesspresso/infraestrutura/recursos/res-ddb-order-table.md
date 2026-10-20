---
id: res-ddb-order-table
kind: resource
subject: resource:dynamodb-table:serverlesspresso-order-table
camada: 6
status: proposed
realiza: [sys-order-manager-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L647-L709"
    version: 9d494a2
    extraction: extracted
---
# DynamoDB "serverlesspresso-order-table"
| Campo | Valor |
|---|---|
| Tipo | banco |
| Tecnologia | Amazon DynamoDB, `PAY_PER_REQUEST`, Streams (`NEW_AND_OLD_IMAGES`), LSI `LSI-timestamp`, GSIs `GSI-status` e `GSI-userId` |
| Ambientes | consolidado (01-appCore) |
| Definido em | `01-appCore/template.yaml` |

## Usado por
- order-manager-service (lambdas `workflow-started`, `waiting-completion`, `order-timed-out`, state machine, API REST — leitura e escrita)
