---
id: term-eventid
kind: term
subject: term:eventId
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "presente em quase todo o código, ex.: backends/9-validator/code/getCode.js, backends/4-order-processing/statemachine/op.asl.json"
    version: 9d494a2
    extraction: extracted
---
# eventId
Identificador do "evento pop-up" físico (ex.: um dia específico do balcão em um re:Invent ou conferência). É a partição usada em quase todas as tabelas (`config-{eventId}`, `orderID-{eventId}`) e no nome dos tópicos IoT — permite que várias edições do Serverlesspresso rodem sobre a mesma infraestrutura sem se misturar.

Não confundir com: `orderId` (identifica um pedido individual), `EventBridge event` (a mensagem que trafega no barramento, chamada de "evento" no sentido de arquitetura orientada a eventos).
