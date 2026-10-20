---
id: cap-vender-produtos-online
kind: capability
subject: capability:vender-produtos-online
camada: 1
status: proposed
realiza: []
realizado-por: [sub-catalogo-e-descoberta, sub-carrinho-e-sessao, sub-checkout-e-pagamento]
provenance:
  - source: repo:microservices-demo
    locator: README.md#L15-L18
    version: 38e7348
    extraction: inferred
---

# Vender produtos online

A empresa consegue vender produtos diretamente ao consumidor final por um site self-service, sem exigir cadastro: o visitante navega, monta um carrinho, escolhe a moeda de exibição, informa endereço e cartão e recebe a confirmação do pedido. `[inferred a partir do comportamento observado no frontend e no checkoutservice — confirmar com o PM se esta é a capacidade de negócio como a empresa a nomeia]`

## Fluxos que a realizam
- [Compra do cliente](../fluxos/compra-do-cliente.md)

## Sistemas envolvidos
- frontend — vitrine, sessão do visitante e formulário de checkout
- productcatalogservice — catálogo de produtos
- cartservice — carrinho de compras
- currencyservice — conversão de preços para a moeda escolhida
- checkoutservice — orquestra a finalização do pedido
- paymentservice — cobrança (mock)
- shippingservice — cotação e expedição (mock)
- emailservice — confirmação por e-mail (mock)
