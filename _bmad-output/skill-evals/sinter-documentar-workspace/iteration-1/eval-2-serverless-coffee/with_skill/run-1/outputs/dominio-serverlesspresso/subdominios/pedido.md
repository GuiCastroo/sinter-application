---
id: sub-pedido
kind: subdomain
subject: subdomain:pedido
camada: 3
status: proposed
realiza: [dom-serverlesspresso]
realizado-por: [sys-validator-service, sys-order-processing-service, sys-order-manager-service, sys-counting-service, sys-publisher-service, sys-order-journey-service, sys-metrics-service]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/1-counting-service, backends/4-order-processing, backends/5-order-manager, backends/6-publisher-service, backends/7-metrics-service, backends/8-order-journey, backends/9-validator"
    version: 9d494a2
    extraction: inferred
---
# Subdomínio Pedido
Do QR code escaneado pelo cliente até a bebida entregue: validação de token, verificação de capacidade, orquestração via Step Functions, persistência do estado do pedido, contagem sequencial, notificação em tempo real e montagem da página de jornada do pedido.

## Sistemas
| Sistema | Papel |
|---|---|
| validator-service | Emite e valida o token/QR code; inicia o pedido publicando `Validator.NewOrder` |
| order-processing-service | Orquestra o pedido de ponta a ponta (Step Functions); controla capacidade da fila e timeouts |
| order-manager-service | Guarda o estado do pedido; expõe a API que cliente e barista usam; sanitiza o pedido contra o cardápio |
| counting-service | Gera o número sequencial do pedido (hoje embutido na state machine do order-processing; ver ficha) |
| publisher-service | Republica os eventos do pedido nos tópicos MQTT (IoT Core) para os apps |
| order-journey-service | Ao final do pedido, monta uma página HTML com a linha do tempo dos eventos |
| metrics-service | Publica métricas customizadas no CloudWatch a partir dos eventos do pedido |

## Fluxos executados aqui
- [Pedido de café](../fluxos/pedido-de-cafe.sequencia.md)
