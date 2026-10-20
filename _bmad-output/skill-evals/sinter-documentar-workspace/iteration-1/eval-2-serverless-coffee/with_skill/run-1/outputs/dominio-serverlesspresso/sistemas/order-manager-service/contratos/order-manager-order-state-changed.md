---
id: ctr-order-manager-order-state-changed
kind: contract
subject: contract:event:OrderManager.OrderStateChanged
camada: 4
status: proposed
realiza: [sys-order-manager-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/statemachine/om.asl.json#L69-L98"
    version: 9d494a2
    extraction: extracted
---
# OrderManager.Order{eventId}-COMPLETED / OrderManager.Order{eventId}-CANCELLED
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge); `detail-type` é montado dinamicamente com `States.Format('OrderManager.Order{}', $.detail.ORDERSTATE)` |
| Produtor | order-manager-service (`order-manager-state-machine`, states `Complete Order`/`Cancel Order`) |
| Consumidores | order-journey-service (decide qual imagem de diagrama mostrar), publisher-service |
| Especificação | Sem AsyncAPI formal. **Nome de evento incomum**: o próprio `eventId` do pedido vira parte do `detail-type` (ex.: `OrderManager.OrderABC-COMPLETED`), o que dificulta criar uma regra EventBridge só com `prefix` — ver `RELATORIO.md` |

## Exemplo
```json
{
  "eventId": "ABC",
  "orderId": "V1StGXR8_Z5jdHi6B-myT",
  "userId": "cognito-sub",
  "ORDERSTATE": "ABC-COMPLETED",
  "Message": "Barrista has cancelled or completed the order"
}
```
