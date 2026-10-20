---
id: cmp-metrics-order-manager-waiting-completion
kind: component
subject: component:metrics-service:order-manager-waiting-completion-metric
camada: 5
status: proposed
realiza: [sys-metrics-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/7-metrics-service/code/OrderManagerWaitingCompletion.js; backends/7-metrics-service/template.yaml#L88-L106"
    version: 9d494a2
    extraction: extracted
---
# order-manager-waiting-completion-metric
Registra no CloudWatch cada pedido que entrou na fila do barista.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Evento EventBridge `detail-type` prefixo `OrderManager.WaitingCompletion` |
| Entrada | Evento `OrderManager.WaitingCompletion` |
| Saída | `cloudwatch:PutMetricData` |
| Timeout / memória / concorrência | 3 s / 128 MB |

## Dependências
- CloudWatch Metrics

## Erros e retentativas
Sem `Retry`/DLQ configurados.
