---
id: res-metrics-queue-sqs
kind: resource
subject: resource:sqs-queue:MetricsQueue
camada: 6
status: proposed
realiza: [sys-ext-persist-metrics-dynamodb]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "extensions/PersistOrderMetricsToDynamoDB/template.yaml#L7-L47"
    version: 9d494a2
    extraction: extracted
---
# SQS "MetricsQueue"
| Campo | Valor |
|---|---|
| Tipo | fila |
| Tecnologia | Amazon SQS, `SqsManagedSseEnabled: true`, `VisibilityTimeout: 30s` |
| Ambientes | extensão `PersistOrderMetricsToDynamoDB` (independente) |
| Definido em | `extensions/PersistOrderMetricsToDynamoDB/template.yaml` |

## Usado por
- extensao-persist-metrics-dynamodb (`publishMetric` lambda consome via `EventSourceMapping`)
