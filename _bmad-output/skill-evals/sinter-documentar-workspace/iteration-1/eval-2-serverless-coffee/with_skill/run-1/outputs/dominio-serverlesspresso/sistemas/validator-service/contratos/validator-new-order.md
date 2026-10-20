---
id: ctr-validator-new-order
kind: contract
subject: contract:event:Validator.NewOrder
camada: 4
status: proposed
realiza: [sys-validator-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/9-validator/code/verifyCode.js#L82-L101; 01-appCore/template.yaml#L798-L807"
    version: 9d494a2
    extraction: extracted
---
# Validator.NewOrder
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge) |
| Produtor | validator-service (`verify-qr-code`) |
| Consumidores | order-processing-service (regra EventBridge que inicia a state machine diretamente, sem lambda) |
| Especificação | Sem OpenAPI/AsyncAPI formal; contrato inferido do código |

## Exemplo
```json
{
  "orderId": "V1StGXR8_Z5jdHi6B-myT",
  "userId": "cognito-sub-do-cliente",
  "eventId": "ABC",
  "Message": "A Lambda function is invoked by a POST request...",
  "bucket": { "PK": "ABC-123456", "last_code": "9f8a7b6c5d", "availableTokens": 4 }
}
```
