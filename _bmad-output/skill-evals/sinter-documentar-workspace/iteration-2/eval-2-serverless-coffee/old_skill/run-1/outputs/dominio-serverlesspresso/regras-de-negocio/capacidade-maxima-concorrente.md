---
id: rule-capacidade-maxima-concorrente
kind: rule
subject: rule:capacidade-maxima-concorrente
camada: 0
status: proposed
realiza: [flow-pedido-de-cafe]
realizado-por: [cmp-order-processor-state-machine]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json#L32-L52"
    version: 9d494a2
    extraction: extracted
---
# Capacidade máxima de pedidos simultâneos
No máximo **20 pedidos** podem estar em andamento ao mesmo tempo (execuções `RUNNING` da `order-processor-state-machine`); um 21º pedido é recusado com `OrderProcessor.ShopUnavailable` até que algum dos 20 termine.

## Onde está implementada
- `backends/4-order-processing/statemachine/op.asl.json`, states `ListExecutions` + `Is capacity available?` (`$.isCapacityAvailable[20]`)

## Conflito
Valor `20` está **hardcoded como índice de array** na expressão JSONPath (`$.isCapacityAvailable[20]`), não como parâmetro nomeado — forma frágil de configurar um limite de negócio; qualquer mudança exige editar o ASL. Marcado para confirmação com o tech lead sobre se isso é intencional (ver `RELATORIO.md`).
