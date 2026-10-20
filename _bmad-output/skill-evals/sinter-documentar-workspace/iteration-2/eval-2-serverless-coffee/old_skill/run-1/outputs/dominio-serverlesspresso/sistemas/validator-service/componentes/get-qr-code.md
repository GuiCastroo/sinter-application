---
id: cmp-validator-get-qr-code
kind: component
subject: component:validator-service:get-qr-code
camada: 5
status: proposed
realiza: [sys-validator-service]
realizado-por: [res-ddb-validator-table]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/9-validator/code/getCode.js; 01-appCore/template.yaml#L413-L446"
    version: 9d494a2
    extraction: extracted
---
# get-qr-code
Gera ou recupera o "bucket" de tokens da janela de 5 minutos atual e devolve o código para o app do cliente exibir como QR code.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | `GET /qr-code` via API Gateway (Cognito authorizer; exige `cognito:groups` conter `admin`) |
| Entrada | `queryStringParameters.eventId` |
| Saída | `200 {bucket: {PK, last_code, start_ts, end_ts, availableTokens, eventId}}`, `403` se não-admin, `400` se `eventId` ausente ou não encontrado no config |
| Timeout / memória / concorrência | 3–15 s (diverge entre templates) / 128 MB / não limitada explicitamente |

## Dependências
- `serverlesspresso-validator` (DynamoDB) — lê/cria o bucket de tokens da janela atual
- `ConfigTable` — lê `drinksPerBarcode` para saber quantos tokens a janela deve ter

## Erros e retentativas
Sem `Retry`/DLQ configurados. Erros de leitura no DynamoDB são apenas logados (`console.error`) na função `getConfig`/`getItem` de `ddb.js`, sem propagar exceção — **uma falha do DynamoDB pode retornar `bucket` vazio silenciosamente**. Achado a reportar (ver `RELATORIO.md`).
