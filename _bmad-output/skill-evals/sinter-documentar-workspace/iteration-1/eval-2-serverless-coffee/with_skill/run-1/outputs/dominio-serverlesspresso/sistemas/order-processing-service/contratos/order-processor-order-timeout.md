---
id: ctr-order-processor-order-timeout
kind: contract
subject: contract:event:OrderProcessor.OrderTimeOut
camada: 4
status: proposed
realiza: [sys-order-processing-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json#L93-L113"
    version: 9d494a2
    extraction: extracted
---
# OrderProcessor.OrderTimeOut
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge) |
| Produtor | order-processing-service (dois pontos distintos do ASL: timeout do cliente e timeout do barista) |
| Consumidores | order-manager-service (`OrderTimedOut` lambda, marca o pedido como cancelado), metrics-service, order-journey-service, publisher-service |
| Especificação | Sem AsyncAPI formal |

## Exemplo
```json
{
  "Message": "The order timed out. Step Functions waits a set amount of time...",
  "userId": "cognito-sub",
  "orderId": "V1StGXR8_Z5jdHi6B-myT",
  "eventId": "ABC",
  "cause": "Customer timedout"
}
```
