---
id: ctr-order-processor-waiting-completion
kind: contract
subject: contract:event:OrderProcessor.WaitingCompletion
camada: 4
status: proposed
realiza: [sys-order-processing-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json#L138-L157"
    version: 9d494a2
    extraction: extracted
---
# OrderProcessor.WaitingCompletion
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge, `putEvents.waitForTaskToken`) |
| Produtor | order-processing-service |
| Consumidores | order-manager-service (`waitingCompletion` lambda), order-journey-service, publisher-service |
| Especificação | Sem AsyncAPI formal |

## Exemplo
```json
{
  "Message": "You pressed 'submit order'...",
  "TaskToken": "AAAAKgAAAAIAAAAA...",
  "orderId": "V1StGXR8_Z5jdHi6B-myT",
  "orderNumber": "42",
  "userId": "cognito-sub",
  "eventId": "ABC"
}
```
