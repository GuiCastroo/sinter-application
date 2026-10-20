---
id: res-rest-api-config
kind: resource
subject: resource:apigateway:ServerlesspressoConfigServiceRestApi
camada: 6
status: proposed
realiza: [sys-config-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L330-L341"
    version: 9d494a2
    extraction: extracted
---
# API Gateway REST "ServerlesspressoConfigServiceRestApi"
| Campo | Valor |
|---|---|
| Tipo | gateway |
| Tecnologia | Amazon API Gateway (REST), integração direta com DynamoDB |
| Ambientes | consolidado (01-appCore) |
| Definido em | `01-appCore/template.yaml`, corpo da API em `backends/2-config-service/RestAPIs/api.yaml` |

## Usado por
- config-service (`rest-api-config`: `GET /config`, `GET /admin-config`, `PUT /store`)
