---
id: cmp-metrics-order-processor-timeout
kind: component
subject: component:metrics-service:order-processor-order-timeout-metric
camada: 5
status: proposed
realiza: [sys-metrics-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/7-metrics-service/code/OrderProcessorOrderTimeOut.js; backends/7-metrics-service/template.yaml#L69-L86"
    version: 9d494a2
    extraction: extracted
---
# order-processor-order-timeout-metric
Registra no CloudWatch pedidos perdidos por timeout (cliente ou barista).

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Evento EventBridge `detail-type` prefixo `OrderProcessor.OrderTimeOut` |
| Entrada | Evento `OrderProcessor.OrderTimeOut` |
| Saída | `cloudwatch:PutMetricData` |
| Timeout / memória / concorrência | 3 s / 128 MB |

## Dependências
- CloudWatch Metrics

## Erros e retentativas
Sem `Retry`/DLQ configurados.
