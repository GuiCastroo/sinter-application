---
id: term-task-token
kind: term
subject: term:task-token
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json; backends/5-order-manager/statemachine/om.asl.json"
    version: 9d494a2
    extraction: extracted
---
# Task Token
Identificador opaco que o AWS Step Functions gera quando uma execução usa o padrão `waitForTaskToken`. O `order-processing-service` gera um token, o `order-manager-service` guarda esse token no DynamoDB (campo `TaskToken` do pedido) e, quando a ação humana correspondente acontece (cliente envia o pedido, barista conclui), chama `SendTaskSuccess` com o token para "acordar" a execução pausada.

Não confundir com: o "código"/token de 6 dígitos do login por SMS (ver `create-auth-challenge`), nem com o token do QR code do balcão (ver componente `verify-qr-code`).
