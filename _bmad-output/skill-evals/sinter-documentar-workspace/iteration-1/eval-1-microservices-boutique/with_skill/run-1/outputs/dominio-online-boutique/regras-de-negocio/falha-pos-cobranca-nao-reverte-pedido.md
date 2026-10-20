---
id: rule-falha-pos-cobranca-nao-reverte-pedido
kind: rule
subject: rule:falha-pos-cobranca-nao-reverte-pedido
camada: 0
status: proposed
realiza: []
realizado-por: [cmp-checkoutservice-placeorder]
provenance:
  - source: repo:microservices-demo
    locator: src/checkoutservice/main.go#L268-L282
    version: 38e7348
    extraction: extracted
---

# Falhas após a cobrança não revertem o pedido (nem sempre bloqueiam)

Depois que `paymentservice.Charge` é aprovado:
- se `EmptyCart` falhar, o erro é descartado (`_ = cs.emptyUserCart(...)`) e o pedido segue confirmado;
- se `SendOrderConfirmation` falhar, o erro é logado como aviso e o pedido segue confirmado;
- **mas** se `ShipOrder` falhar, o `PlaceOrder` inteiro retorna erro ao cliente (`codes.Unavailable`) — mesmo com o cartão já cobrado e sem nenhum estorno automático.

Não existe compensação/saga: nenhuma chamada de estorno ao `paymentservice` acontece em nenhum desses casos de erro. `[extracted]`

## Onde está implementada
- `src/checkoutservice/main.go#L262-L282`

## Conflito
Não há conflito de fontes aqui — é um comportamento único e claro no código. Está registrado como regra por ser uma decisão de negócio implícita e arriscada (cliente pode pagar e não ter pedido caso o frete falhe), a validar com o PM/tech lead.
