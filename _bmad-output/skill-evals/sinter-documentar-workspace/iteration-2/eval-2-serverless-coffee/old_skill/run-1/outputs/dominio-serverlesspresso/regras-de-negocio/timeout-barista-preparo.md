---
id: rule-timeout-barista-preparo
kind: rule
subject: rule:timeout-barista-preparo
camada: 0
status: proposed
realiza: [flow-pedido-de-cafe]
realizado-por: [cmp-order-processor-state-machine]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json#L138-L170"
    version: 9d494a2
    extraction: extracted
---
# Timeout do barista para concluir o pedido
Depois que o pedido entra na fila com um número, o barista tem **15 minutos** (`HeartbeatSeconds: 900` no state `Emit - Awaiting Completion TT`) para concluir ou cancelar antes de o pedido expirar por timeout.

## Onde está implementada
- `backends/4-order-processing/statemachine/op.asl.json`, state `Emit - Awaiting Completion TT`

## Conflito
Não identificado. Mesmo comentário do timeout do cliente: valor hardcoded no ASL.
