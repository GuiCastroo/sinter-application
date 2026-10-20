---
id: rule-bandeiras-de-cartao-aceitas
kind: rule
subject: rule:bandeiras-de-cartao-aceitas
camada: 0
status: proposed
realiza: []
realizado-por: [cmp-paymentservice-charge]
provenance:
  - source: repo:microservices-demo
    locator: src/paymentservice/charge.js#L43-L46, #L72-L74
    version: 38e7348
    extraction: extracted
---

# Bandeiras de cartão aceitas

Somente cartões **Visa** e **MasterCard** são aceitos. Qualquer outra bandeira identificada (ex.: American Express, Diners Club) é rejeitada com a mensagem "Sorry, we cannot process {bandeira} credit cards. Only VISA or MasterCard is accepted." `[extracted]`

## Onde está implementada
- `src/paymentservice/charge.js` (classe `UnacceptedCreditCard`, função `charge`)
