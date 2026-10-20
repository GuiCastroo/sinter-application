---
id: cmp-checkoutservice-placeorder
kind: component
subject: component:checkoutservice:place-order
camada: 5
status: proposed
realiza: [sys-checkoutservice]
realizado-por: [res-nenhum-recurso-proprio]
provenance:
  - source: repo:microservices-demo
    locator: src/checkoutservice/main.go#L237-L394
    version: 38e7348
    extraction: extracted
---

# PlaceOrder

Endpoint gRPC único do `checkoutservice`; orquestra todo o passo a passo do checkout (ver [sequência técnica completa](../../../fluxos/compra-do-cliente.sequencia.md)).

| Campo | Valor |
|---|---|
| Tipo | endpoint gRPC |
| Gatilho | chamada `CheckoutService.PlaceOrder` (do `frontend`) |
| Entrada | `PlaceOrderRequest` (user_id, user_currency, address, email, credit_card) |
| Saída | `PlaceOrderResponse` (OrderResult) ou erro gRPC |
| Timeout / memória / concorrência | Sem timeout de handler configurado; requests `cpu: 100m/limit 200m`, `memory: 64Mi/limit 128Mi` no pod `[extracted, kubernetes-manifests/checkoutservice.yaml#L64-L69]` |

## Dependências
- cartservice — GetCart, EmptyCart
- productcatalogservice — GetProduct (um por item do carrinho)
- currencyservice — Convert (um por item + um para o frete)
- shippingservice — GetQuote, ShipOrder
- paymentservice — Charge

## Erros e retentativas
Sem retentativa em nenhuma chamada. Erros de `GetCart`, `GetProduct`, `Convert` ou `GetQuote` abortam com `codes.Internal` antes de qualquer cobrança. Erro em `Charge` aborta com `codes.Internal` (o pedido nunca chega a existir). Erro em `ShipOrder` **após** a cobrança aborta com `codes.Unavailable` — nesse ponto o cartão já foi debitado e nenhum pedido é registrado (ver risco em [RELATORIO.md](../../../RELATORIO.md)). Erros de `EmptyCart` e `SendOrderConfirmation` são descartados/logados e não abortam a resposta. `[extracted, src/checkoutservice/main.go#L241-L283]`
