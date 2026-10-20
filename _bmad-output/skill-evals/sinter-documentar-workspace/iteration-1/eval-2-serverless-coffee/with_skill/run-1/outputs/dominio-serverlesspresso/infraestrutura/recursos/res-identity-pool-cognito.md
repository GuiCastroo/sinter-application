---
id: res-identity-pool-cognito
kind: resource
subject: resource:cognito-identity-pool:ServerlesspressoIdentityPool
camada: 6
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/template.yaml#L220-L314"
    version: 9d494a2
    extraction: extracted
---
# Cognito Identity Pool "ServerlesspressoIdentityPool"
| Campo | Valor |
|---|---|
| Tipo | banco de identidade (credenciais federadas AWS) |
| Tecnologia | Amazon Cognito Identity Pool, permite identidades não-autenticadas (`AllowUnauthenticatedIdentities: true`) |
| Ambientes | core (00-baseCore) |
| Definido em | `00-baseCore/template.yaml` |

## Usado por
- Apps de front-end (fora deste repositório) — obtêm credenciais AWS temporárias para conectar direto no AWS IoT Core (`iot:Connect`, `iot:Subscribe`, `iot:Receive`) via os papéis `CognitoAuthorizedRole`/`CognitoUnAuthorizedRole`
