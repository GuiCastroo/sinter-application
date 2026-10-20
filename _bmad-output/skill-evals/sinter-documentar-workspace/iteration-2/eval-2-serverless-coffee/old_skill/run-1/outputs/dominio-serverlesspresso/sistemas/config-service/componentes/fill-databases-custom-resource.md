---
id: cmp-config-fill-databases
kind: component
subject: component:config-service:fill-databases-custom-resource
camada: 5
status: proposed
realiza: [sys-config-service]
realizado-por: [res-ddb-config-table, res-ddb-counting-table]
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/initDB/app.js; 01-appCore/initDB/initMenu.js; 01-appCore/template.yaml#L513-L536"
    version: 9d494a2
    extraction: extracted
---
# fill-databases-custom-resource
Custom Resource do CloudFormation que popula `ConfigTable` (cardápio inicial) e `CountingTable` (contador zerado) toda vez que a pilha `01-appCore` é criada ou atualizada.

| Campo | Valor |
|---|---|
| Tipo | job (Lambda-backed CloudFormation Custom Resource) |
| Gatilho | `AWS::CloudFormation::CustomResource` nos eventos `Create`/`Update`/`Delete` do stack |
| Entrada | `initMenuState.JSON`, `initCountingState.JSON` (embutidos no pacote da função) |
| Saída | `BatchWriteItem` em `ConfigTable` e `CountingTable`; responde ao CloudFormation via `ResponseURL` |
| Timeout / memória / concorrência | 15 s / 128 MB |

## Dependências
- `ConfigTable`, `CountingTable` — `dynamodb:BatchWriteItem`

## Erros e retentativas
`Delete` não limpa dados (apenas responde `SUCCESS`); não há tratamento de falha parcial do `BatchWriteItem` (itens não processados não são reenviados).
