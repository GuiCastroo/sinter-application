---
id: res-rest-api-order-manager
kind: resource
subject: resource:apigateway:ServerlesspressoOrdermanagerRestApi
camada: 6
status: proposed
realiza: [sys-order-manager-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L712-L720"
    version: 9d494a2
    extraction: extracted
---
# API Gateway REST "ServerlesspressoOrdermanagerRestApi"
| Campo | Valor |
|---|---|
| Tipo | gateway |
| Tecnologia | Amazon API Gateway (REST), integrações diretas com DynamoDB e Step Functions, autorização Cognito User Pools |
| Ambientes | consolidado (01-appCore) |
| Definido em | `01-appCore/template.yaml`, corpo da API em `backends/5-order-manager/RestAPIs/api.yaml` |

## Usado por
- order-manager-service (`rest-api-orders`: `GET /orders`, `GET /orders/{id}`, `PUT /orders/{id}`)
