---
id: cmp-validator-verify-qr-code
kind: component
subject: component:validator-service:verify-qr-code
camada: 5
status: proposed
realiza: [sys-validator-service]
realizado-por: [res-ddb-validator-table, res-event-bus-serverlesspresso]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/9-validator/code/verifyCode.js; 01-appCore/template.yaml#L447-L477"
    version: 9d494a2
    extraction: extracted
---
# verify-qr-code
Confere o token escaneado contra o bucket da janela atual; se válido, gera o `orderId` e publica `Validator.NewOrder`, iniciando o pedido.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | `POST /qr-code` via API Gateway (Cognito authorizer) |
| Entrada | `queryStringParameters.{eventId, token}`, `requestContext.authorizer.claims.sub` (userId) |
| Saída | `200 {orderId}`; `400 {error: "Invalid code"}` ou `{error: "No tokens remaining"}` (este último com `statusCode 200`, ver nota); `422` se faltar parâmetro |
| Timeout / memória / concorrência | 10 s / 128 MB |

## Dependências
- `serverlesspresso-validator` (DynamoDB) — lê o bucket e decrementa `availableTokens`
- EventBridge `Serverlesspresso` — publica `Validator.NewOrder`

## Erros e retentativas
Sem `Retry`/DLQ. Nota de qualidade: a resposta "sem tokens restantes" usa `statusCode: 200` em vez de um código de erro (`error` só aparece no corpo) — o cliente HTTP precisa inspecionar o corpo, não o status, para tratar esse caso.
