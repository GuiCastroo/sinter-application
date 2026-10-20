---
id: res-user-pool-cognito
kind: resource
subject: resource:cognito-user-pool:ServerlesspressoUserPool
camada: 6
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/template.yaml#L159-L219"
    version: 9d494a2
    extraction: extracted
---
# Cognito User Pool "ServerlesspressoUserPool"
| Campo | Valor |
|---|---|
| Tipo | banco de identidade / autenticação |
| Tecnologia | Amazon Cognito User Pool, login por `phone_number`, fluxo `CUSTOM_CHALLENGE` (sem senha) |
| Ambientes | core (00-baseCore); ARN e ID publicados via SSM (`/Serverlesspresso/core/userpool*`) para todos os outros stacks |
| Definido em | `00-baseCore/template.yaml` |

## Usado por
- validator-service (autoriza `GET/POST /qr-code`)
- order-manager-service (autoriza `GET/PUT /orders*`)
- config-service (autoriza `GET /admin-config`, `PUT /store`)
- Todas as 4 lambdas de trigger do Cognito (`pre-sign-up`, `define-auth-challenge`, `create-auth-challenge`, `verify-auth-challenge-response`)
