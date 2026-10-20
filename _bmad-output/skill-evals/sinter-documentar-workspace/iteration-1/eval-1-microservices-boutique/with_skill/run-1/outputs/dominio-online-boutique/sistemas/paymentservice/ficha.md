---
id: sys-paymentservice
kind: system
subject: system:paymentservice
camada: 4
status: proposed
realiza: [sub-checkout-e-pagamento]
realizado-por: [cmp-paymentservice-charge]
provenance:
  - source: repo:microservices-demo
    locator: src/paymentservice/charge.js#L61-L86
    version: 38e7348
    extraction: extracted
---

# paymentservice

Valida os dados de um cartão de crédito e simula a cobrança, devolvendo um id de transação. **Não há integração real com nenhuma adquirente/processadora** — nenhum valor é de fato debitado. `[extracted]`

| Campo | Valor |
|---|---|
| Subdomínio | Checkout e Pagamento |
| Dono | Não identificado `[a confirmar]` |
| Stack | Node.js, `simple-card-validator`, `uuid` |
| Repositório | `src/paymentservice/` |
| Criticidade | Alta — bloqueia o pedido se falhar `[inferred]` |

## Expõe

| Contrato | Tipo | Detalhe |
|---|---|---|
| `PaymentService.Charge` | gRPC | Ver [componente charge](./componentes/charge.md) e [regras de cartão](../../regras-de-negocio/bandeiras-de-cartao-aceitas.md) |

`[extracted, protos/demo.proto#L177-L195]`

## Consome
- Nenhum outro sistema.

## Dados
Não persiste nada — cada chamada é sem estado; o `transaction_id` retornado é um UUID aleatório, não rastreável depois. `[extracted, src/paymentservice/charge.js#L85]`

## Qualidade
- Erros de validação (`InvalidCreditCard`, `UnacceptedCreditCard`, `ExpiredCreditCard`) têm `code = 400` mas são propagados como gRPC error genérico; o `checkoutservice` os traduz para `Internal` (500) na resposta ao cliente — perde-se a granularidade do motivo da recusa. `[extracted, src/paymentservice/charge.js#L30-L53; src/checkoutservice/main.go#L262-L266]`
