---
id: ctr-order-manager-make-order
kind: contract
subject: contract:event:OrderManager.MakeOrder
camada: 4
status: proposed
realiza: [sys-order-manager-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/statemachine/om.asl.json#L274-L302"
    version: 9d494a2
    extraction: extracted
---
# OrderManager.MakeOrder
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge) |
| Produtor | order-manager-service (`order-manager-state-machine`, states `Make OR Unmake?`/`Transform record`) |
| Consumidores | publisher-service, order-journey-service |
| Especificação | Sem AsyncAPI formal |

## Exemplo
```json
{
  "baristaUserId": "cognito-sub-do-barista",
  "orderId": "V1StGXR8_Z5jdHi6B-myT",
  "eventId": "ABC",
  "userId": "cognito-sub-do-cliente",
  "Message": "The barista has pressed the 'Make order' button..."
}
```
