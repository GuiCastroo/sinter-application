---
id: sub-checkout-e-pagamento
kind: subdomain
subject: subdomain:checkout-e-pagamento
camada: 3
status: proposed
realiza: [dom-online-boutique, cap-vender-produtos-online]
realizado-por: [sys-checkoutservice, sys-paymentservice, sys-shippingservice, sys-emailservice, sys-currencyservice]
provenance:
  - source: repo:microservices-demo
    locator: src/checkoutservice/main.go#L67-L84
    version: 38e7348
    extraction: extracted
---

# Subdomínio Checkout e Pagamento

Orquestra a finalização do pedido: reúne o carrinho, precifica na moeda do cliente, cota e executa o frete, cobra o cartão e confirma por e-mail. `[extracted]`

## Sistemas

| Sistema | Papel |
|---|---|
| [checkoutservice](../sistemas/checkoutservice/ficha.md) | Orquestrador central — único ponto que fala com cart, catálogo, câmbio, frete, pagamento e e-mail |
| [paymentservice](../sistemas/paymentservice/ficha.md) | Valida e "cobra" o cartão (mock) |
| [shippingservice](../sistemas/shippingservice/ficha.md) | Cota e "executa" o frete (mock) |
| [emailservice](../sistemas/emailservice/ficha.md) | Envia (mock) a confirmação do pedido |
| [currencyservice](../sistemas/currencyservice/ficha.md) | Converte todos os valores monetários para a moeda do cliente |

## Fluxos executados aqui
- [Compra do cliente](../fluxos/compra-do-cliente.sequencia.md) — passos 5 a 12 (o núcleo do subdomínio)

## Como o fluxo vira engenharia

O `checkoutservice` é a única porta de entrada deste subdomínio (`PlaceOrder`); nenhum outro sistema do domínio chama `paymentservice`, `shippingservice` ou `emailservice` diretamente. Isso o torna o ponto único de falha e de regra de negócio do checkout. `[extracted — nenhum outro cliente gRPC para paymentservice/shippingservice/emailservice encontrado além do checkoutservice]`
