---
id: sub-extensoes
kind: subdomain
subject: subdomain:extensoes
camada: 3
status: proposed
realiza: [dom-serverlesspresso]
realizado-por: [sys-ext-event-player, sys-ext-order-robot, sys-ext-persist-metrics-dynamodb, sys-ext-wait-times]
provenance:
  - source: repo:serverless-coffee
    locator: "extensions/README.md"
    version: 9d494a2
    extraction: extracted
---
# Subdomínio Extensões
Add-ons opcionais que demonstram a extensibilidade da arquitetura orientada a eventos: cada um só cria novas regras do EventBridge sobre o bus `Serverlesspresso` existente, não tem permissão de acessar recursos do core e pode ser implantado/removido independentemente (regra documentada em `extensions/README.md`).

## Sistemas
| Sistema | Papel |
|---|---|
| extensao-event-player | Simula 15 minutos de operação do balcão, reproduzindo uma sequência de eventos gravada |
| extensao-order-robot | Simula um robô que faz pedidos e um robô barista que os prepara |
| extensao-persist-metrics-dynamodb | Consome `OrderManager.WaitingCompletion` via fila SQS e grava em uma tabela DynamoDB própria |
| extensao-wait-times | Calcula o tempo médio de preparo por bebida a partir dos eventos de início/fim do pedido |

## Fluxos executados aqui
Nenhum fluxo de negócio principal; cada extensão observa eventos do [pedido de café](../fluxos/pedido-de-cafe.sequencia.md) de fora, sem participar da orquestração.
