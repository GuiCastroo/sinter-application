---
id: term-moeda-de-exibicao
kind: term
subject: term:moeda-de-exibicao
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: src/frontend/main.go#L44-L45
    version: 38e7348
    extraction: extracted
---

# Moeda de exibição

Código ISO 4217 (ex.: `USD`, `EUR`, `BRL`) escolhido pelo cliente via `POST /setCurrency` e guardado no cookie `shop_currency`. Todo preço mostrado — e o total cobrado no checkout — é convertido para esta moeda a partir do preço-base em USD do catálogo.

Não confundir com: a moeda em que o catálogo é definido internamente (sempre USD, campo `price_usd` de `Product`).
