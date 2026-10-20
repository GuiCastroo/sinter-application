---
id: std-orquestracao-por-task-token
kind: standard
subject: standard:orquestracao-por-task-token
camada: 0
status: proposed
realiza: []
realizado-por: [sys-order-processing-service, sys-order-manager-service]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json; backends/5-order-manager/statemachine/om.asl.json"
    version: 9d494a2
    extraction: inferred
---
# Orquestração por Task Token entre duas state machines
Como o domínio conecta um processo de longa duração (o pedido, minutos a horas) com ações humanas assíncronas (cliente monta o pedido, barista conclui), sem fazer polling nem manter uma lambda "esperando".

## Exemplo
1. State machine A emite `events:putEvents.waitForTaskToken` e pausa.
2. O evento carrega o `$$.Task.Token` no `detail`.
3. Uma lambda ou outra state machine guarda esse token em um banco (aqui, no campo `TaskToken` do pedido em DynamoDB).
4. Quando a ação humana ocorre, quem tem o token chama `states:SendTaskSuccess` (ou `SendTaskFailure`) para retomar a state machine A.
5. Um `Catch` de `States.Timeout` com `HeartbeatSeconds` cobre o caso de a ação humana nunca acontecer.

## Onde se aplica
- `order-processing-service` ↔ `order-manager-service`, nos dois pontos do [fluxo de pedido de café](../fluxos/pedido-de-cafe.sequencia.md) (cliente envia o pedido; barista conclui/cancela)
