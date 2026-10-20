---
id: cap-vender-cafe-sob-demanda
kind: capability
subject: capability:vender-cafe-sob-demanda
camada: 1
status: proposed
realiza: []
realizado-por: [flow-pedido-de-cafe, sub-pedido, sub-configuracao-da-loja]
provenance:
  - source: repo:serverless-coffee
    locator: "README.md; backends/4-order-processing/README.md"
    version: 9d494a2
    extraction: inferred
---
# Vender café sob demanda em um evento pop-up
A empresa consegue operar um balcão de café pop-up onde o cliente pede pelo celular via QR code, entra numa fila com capacidade limitada, e acompanha o pedido até a entrega pelo barista, sem uso de caixa registradora ou app dedicado de pagamento.

Capacidade proposta a partir do que o código implementa (fila com capacidade, cardápio configurável, validação de token); **não confirmado com PM** — não há documento de negócio no repositório.

## Fluxos que a realizam
- [Pedido de café](../fluxos/pedido-de-cafe.md)

## Sistemas envolvidos
- validator-service — emite e valida o token/QR code do cliente
- config-service — mantém o cardápio e o estado aberto/fechado da loja
- order-processing-service — controla capacidade da fila e orquestra o pedido de ponta a ponta
- order-manager-service — guarda o estado do pedido e atende as ações do barista
- publisher-service — leva o estado do pedido em tempo real para os apps
- order-journey-service — monta o resumo/jornada do pedido ao final
