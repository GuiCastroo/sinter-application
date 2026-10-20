---
id: cmp-config-rest-api
kind: component
subject: component:config-service:rest-api-config
camada: 5
status: proposed
realiza: [sys-config-service]
realizado-por: [res-ddb-config-table, res-rest-api-config]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/2-config-service/RestAPIs/api.yaml"
    version: 9d494a2
    extraction: extracted
---
# rest-api-config
Rotas de leitura e escrita da configuração da loja, todas em integração direta do API Gateway com o DynamoDB (sem lambda).

| Campo | Valor |
|---|---|
| Tipo | endpoint (API Gateway REST, integração direta) |
| Gatilho | `GET /config` (público), `GET /admin-config` (Cognito), `PUT /store` (Cognito) |
| Entrada | Query `eventId` (GET); query `eventId`, `state=open|closed` (PUT) |
| Saída | Item de `ConfigTable` (GET); item atualizado (PUT) |
| Timeout / memória / concorrência | N/A (sem lambda) |

## Dependências
- `serverlesspresso-config-table` — via role `ConfigRESTApiRole` (`dynamodb:GetItem`, `UpdateItem`, `Query`)

## Erros e retentativas
Sem lambda; erros de VTL/permissão retornam como erro genérico do API Gateway.
