---
id: res-metrics-table-dynamodb
kind: resource
subject: resource:dynamodb-table:serverlesspresso-metrics-table
camada: 6
status: proposed
realiza: [sys-ext-persist-metrics-dynamodb]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "extensions/PersistOrderMetricsToDynamoDB/template.yaml#L49-L65"
    version: 9d494a2
    extraction: extracted
---
# DynamoDB "serverlesspresso-metrics-table"
| Campo | Valor |
|---|---|
| Tipo | banco |
| Tecnologia | Amazon DynamoDB, capacidade **provisionada** (5 RCU / 5 WCU) — diferente do `PAY_PER_REQUEST` usado no restante do domínio |
| Ambientes | extensão `PersistOrderMetricsToDynamoDB` (independente) |
| Definido em | `extensions/PersistOrderMetricsToDynamoDB/template.yaml` |

## Usado por
- extensao-persist-metrics-dynamodb (`publishMetric` lambda)
