---
id: ctr-order-processor-order-finished
kind: contract
subject: contract:event:OrderProcessor.orderFinished
camada: 4
status: proposed
realiza: [sys-order-processing-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json#L197-L220"
    version: 9d494a2
    extraction: extracted
---
# OrderProcessor.orderFinished
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge) |
| Produtor | order-processing-service |
| Consumidores | order-journey-service (gatilho para montar a página HTML da jornada do pedido), extensão wait-times, publisher-service |
| Especificação | Sem AsyncAPI formal |

## Exemplo
```json
{
  "Message": "The order has reached the end of the workflow...",
  "userId": "cognito-sub",
  "orderId": "V1StGXR8_Z5jdHi6B-myT",
  "eventId": "ABC"
}
```

Nota: este evento é emitido tanto quando o barista **conclui** quanto quando **cancela** o pedido — o ASL não distingue os dois casos neste ponto (ver `RELATORIO.md`).
