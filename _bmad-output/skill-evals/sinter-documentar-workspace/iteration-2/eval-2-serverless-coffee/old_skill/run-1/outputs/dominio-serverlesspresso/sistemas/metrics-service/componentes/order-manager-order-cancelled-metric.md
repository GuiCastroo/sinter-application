---
id: cmp-metrics-order-manager-cancelled
kind: component
subject: component:metrics-service:order-manager-order-cancelled-metric
camada: 5
status: proposed
realiza: [sys-metrics-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/7-metrics-service/code/OrderManagerOrderCancelled.js; backends/7-metrics-service/template.yaml#L50-L67"
    version: 9d494a2
    extraction: extracted
---
# order-manager-order-cancelled-metric
Registra no CloudWatch pedidos cancelados pelo barista.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Evento EventBridge `detail-type` prefixo `OrderManager.OrderCancelled` — **ver divergência de nome de evento na ficha do sistema** |
| Entrada | Evento `OrderManager.Order*-CANCELLED` |
| Saída | `cloudwatch:PutMetricData` |
| Timeout / memória / concorrência | 3 s / 128 MB |

## Dependências
- CloudWatch Metrics

## Erros e retentativas
Sem `Retry`/DLQ configurados.
