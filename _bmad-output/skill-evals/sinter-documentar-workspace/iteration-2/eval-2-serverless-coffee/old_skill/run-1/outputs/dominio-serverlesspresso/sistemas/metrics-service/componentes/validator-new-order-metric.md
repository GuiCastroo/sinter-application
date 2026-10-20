---
id: cmp-metrics-validator-new-order
kind: component
subject: component:metrics-service:validator-new-order-metric
camada: 5
status: proposed
realiza: [sys-metrics-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/7-metrics-service/code/ValidatorNewOrder.js; backends/7-metrics-service/template.yaml#L31-L48"
    version: 9d494a2
    extraction: extracted
---
# validator-new-order-metric
Registra no CloudWatch cada novo pedido validado.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Evento EventBridge `detail-type` prefixo `Validator.NewOrder` |
| Entrada | Evento `Validator.NewOrder` |
| Saída | `cloudwatch:PutMetricData` |
| Timeout / memória / concorrência | 3 s / 128 MB (globais do template) |

## Dependências
- CloudWatch Metrics (`CloudWatchPutMetricPolicy`)

## Erros e retentativas
Sem `Retry`/DLQ configurados.
