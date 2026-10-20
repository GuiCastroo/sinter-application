---
id: ctr-order-manager-waiting-completion
kind: contract
subject: contract:event:OrderManager.WaitingCompletion
camada: 4
status: proposed
realiza: [sys-order-manager-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/functions/waitingCompletion/app.js#L41-L61"
    version: 9d494a2
    extraction: extracted
---
# OrderManager.WaitingCompletion
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge) |
| Produtor | order-manager-service (`waiting-completion`) |
| Consumidores | publisher-service, order-journey-service, metrics-service, extensão persist-metrics-dynamodb (via SQS), extensão wait-times |
| Especificação | Sem AsyncAPI formal |

## Exemplo
```json
{
  "orderId": "V1StGXR8_Z5jdHi6B-myT",
  "orderNumber": "42",
  "state": "ABC-WAITING",
  "drinkOrder": { "drink": "Latte", "modifiers": ["Oat milk"] },
  "userId": "cognito-sub",
  "robot": false,
  "eventId": "ABC",
  "TS": 1732550400000
}
```
