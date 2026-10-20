---
id: term-barista
kind: term
subject: term:barista
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/statemachine/om.asl.json; backends/5-order-manager/robot/"
    version: 9d494a2
    extraction: inferred
---
# Barista
Ator humano (ou simulado pela extensão `OrderRobotExtension`/`backends/5-order-manager/robot/`) que reivindica (`make`/`unmake`), prepara e conclui (`complete`) ou cancela (`cancel`) um pedido através da mesma rota `PUT /orders/{id}` usada pelo cliente, diferenciado pelo campo `action` e por seu `baristaUserId`.

Não confundir com: "Cliente" (quem faz o pedido), "robot" (flag booleana no registro do pedido que indica se ele foi originado por um robô de teste, não pelo app real).
