---
id: rule-cartao-nao-pode-estar-vencido
kind: rule
subject: rule:cartao-nao-pode-estar-vencido
camada: 0
status: proposed
realiza: []
realizado-por: [cmp-paymentservice-charge]
provenance:
  - source: repo:microservices-demo
    locator: src/paymentservice/charge.js#L76-L80
    version: 38e7348
    extraction: extracted
---

# Cartão não pode estar vencido

A cobrança só é aceita se `ano_expiração*12 + mês_expiração >= ano_atual*12 + mês_atual`; caso contrário a cobrança é recusada com `ExpiredCreditCard`. `[extracted]`

## Onde está implementada
- `src/paymentservice/charge.js#L76-L80`
