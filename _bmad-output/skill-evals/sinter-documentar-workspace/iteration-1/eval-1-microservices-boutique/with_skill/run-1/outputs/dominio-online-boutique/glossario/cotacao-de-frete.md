---
id: term-cotacao-de-frete
kind: term
subject: term:cotacao-de-frete
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: src/shippingservice/main.go#L118-L138
    version: 38e7348
    extraction: extracted
---

# Cotação de frete

Valor em USD devolvido por `shippingservice.GetQuote`, calculado apenas a partir da contagem total de itens do carrinho — o endereço de entrega é recebido no contrato mas não influencia o cálculo neste mock.

Não confundir com: "expedição"/"ShipOrder" (a ação de despachar, que gera o código de rastreio; é uma chamada separada, feita depois da cobrança aprovada).
