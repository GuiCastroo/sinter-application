---
id: res-http-api-validator
kind: resource
subject: resource:apigateway:validator-service-api
camada: 6
status: proposed
realiza: [sys-validator-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L478-L493; backends/9-validator/template.yaml#L52-L76"
    version: 9d494a2
    extraction: extracted
---
# API Gateway do validator-service
| Campo | Valor |
|---|---|
| Tipo | gateway |
| Tecnologia | Na pilha consolidada (01-appCore): API Gateway **REST** (`RESTApiValidatorService`) com autorização Cognito User Pools. No template standalone (`backends/9-validator/template.yaml`): API Gateway **HTTP** (`MyAdminApi`) com autorizador JWT do Cognito configurado manualmente (issuer/audience) — **duas tecnologias de API diferentes para o mesmo serviço**, ver `RELATORIO.md` |
| Ambientes | consolidado (01-appCore) e módulo standalone (backends/9-validator) |
| Definido em | `01-appCore/template.yaml`; `backends/9-validator/template.yaml` |

## Usado por
- validator-service (`get-qr-code`, `verify-qr-code`)
