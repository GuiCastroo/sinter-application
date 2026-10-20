---
id: rule-timeout-cliente-envio-pedido
kind: rule
subject: rule:timeout-cliente-envio-pedido
camada: 0
status: proposed
realiza: [flow-pedido-de-cafe]
realizado-por: [cmp-order-processor-state-machine]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json#L54-L86"
    version: 9d494a2
    extraction: extracted
---
# Timeout do cliente para enviar o pedido
Depois de escanear o QR code, o cliente tem **5 minutos** (`HeartbeatSeconds: 300` no state `Emit - Workflow Started TT`) para montar e enviar a bebida antes de o pedido ser cancelado automaticamente por timeout.

## Onde está implementada
- `backends/4-order-processing/statemachine/op.asl.json`, state `Emit - Workflow Started TT`

## Conflito
Não identificado. Valor hardcoded no ASL, não configurável por variável de ambiente — mudar exige alterar e reimplantar a definição da state machine.
