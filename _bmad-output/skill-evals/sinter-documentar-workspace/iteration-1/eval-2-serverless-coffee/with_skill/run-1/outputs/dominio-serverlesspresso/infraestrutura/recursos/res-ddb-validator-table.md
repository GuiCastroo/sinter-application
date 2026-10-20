---
id: res-ddb-validator-table
kind: resource
subject: resource:dynamodb-table:serverlesspresso-validator
camada: 6
status: proposed
realiza: [sys-validator-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L496-L509"
    version: 9d494a2
    extraction: extracted
---
# DynamoDB "serverlesspresso-validator"
| Campo | Valor |
|---|---|
| Tipo | banco |
| Tecnologia | Amazon DynamoDB, `PAY_PER_REQUEST`, Streams (`NEW_AND_OLD_IMAGES`, sem consumidor do stream identificado) |
| Ambientes | consolidado (01-appCore); no template standalone (`backends/9-validator/template.yaml`) o mesmo papel é cumprido por uma tabela chamada `ApplicationTable` |
| Definido em | `01-appCore/template.yaml` |

## Usado por
- validator-service (`get-qr-code`, `verify-qr-code`)
