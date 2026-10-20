---
id: res-ddb-config-table
kind: resource
subject: resource:dynamodb-table:serverlesspresso-config-table
camada: 6
status: proposed
realiza: [sys-config-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L316-L328"
    version: 9d494a2
    extraction: extracted
---
# DynamoDB "serverlesspresso-config-table"
| Campo | Valor |
|---|---|
| Tipo | banco |
| Tecnologia | Amazon DynamoDB, `PAY_PER_REQUEST`, Streams (`NEW_AND_OLD_IMAGES`) |
| Ambientes | consolidado (01-appCore) |
| Definido em | `01-appCore/template.yaml` |

## Usado por
- config-service (`config-changed` lê o stream; API REST lê/escreve direto)
- validator-service (lê `drinksPerBarcode`)
- order-processing-service (lê `storeOpen`)
- order-manager-service (lê o cardápio)
- fill-databases-custom-resource (popula na criação/atualização da pilha)
