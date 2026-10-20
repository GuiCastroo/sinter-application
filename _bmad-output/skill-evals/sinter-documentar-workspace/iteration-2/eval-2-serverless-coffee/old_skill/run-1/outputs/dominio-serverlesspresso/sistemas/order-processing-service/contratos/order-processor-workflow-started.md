---
id: ctr-order-processor-workflow-started
kind: contract
subject: contract:event:OrderProcessor.WorkflowStarted
camada: 4
status: proposed
realiza: [sys-order-processing-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json#L54-L86"
    version: 9d494a2
    extraction: extracted
---
# OrderProcessor.WorkflowStarted
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge, `putEvents.waitForTaskToken`) |
| Produtor | order-processing-service |
| Consumidores | order-manager-service (`workflowStarted` lambda), order-journey-service, publisher-service |
| Especificação | Sem AsyncAPI formal |

## Exemplo
```json
{
  "Message": "The workflow waits for your order to be submitted...",
  "TaskToken": "AAAAKgAAAAIAAAAA...",
  "orderId": "V1StGXR8_Z5jdHi6B-myT",
  "userId": "cognito-sub",
  "eventId": "ABC"
}
```
