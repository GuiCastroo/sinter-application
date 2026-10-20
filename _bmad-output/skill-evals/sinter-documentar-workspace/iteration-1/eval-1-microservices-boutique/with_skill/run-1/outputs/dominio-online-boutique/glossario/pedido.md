---
id: term-pedido
kind: term
subject: term:pedido
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: protos/demo.proto#L208-L220
    version: 38e7348
    extraction: extracted
---

# Pedido (OrderResult)

Resultado devolvido por `checkoutservice.PlaceOrder`: id do pedido, itens com preço convertido, custo e endereço de frete, e código de rastreio. **Não é persistido em nenhum banco** — existe apenas na resposta da chamada e na tela de confirmação exibida ao cliente.

Não confundir com: "carrinho" (existe antes do checkout e é apagado depois dele); "transação" (é o retorno do `paymentservice`, um simples UUID, não o pedido inteiro).
