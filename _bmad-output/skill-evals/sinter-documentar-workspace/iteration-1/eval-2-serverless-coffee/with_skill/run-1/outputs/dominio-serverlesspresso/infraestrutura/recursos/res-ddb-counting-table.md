---
id: res-ddb-counting-table
kind: resource
subject: resource:dynamodb-table:serverlesspresso-counting-table
camada: 6
status: proposed
realiza: [sys-counting-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L196-L206"
    version: 9d494a2
    extraction: extracted
---
# DynamoDB "serverlesspresso-counting-table"
| Campo | Valor |
|---|---|
| Tipo | banco |
| Tecnologia | Amazon DynamoDB, `PAY_PER_REQUEST` |
| Ambientes | consolidado (01-appCore) |
| Definido em | `01-appCore/template.yaml` |

## Usado por
- order-processing-service (`Generate Order Number` — `UpdateItem` direto, incrementa `IDvalue`)
- fill-databases-custom-resource (popula na criação/atualização da pilha)
- counting-service (código órfão `getOrderId.js`/`resetOrderId.js` referencia esta tabela mas não está implantado — ver ficha do sistema)
