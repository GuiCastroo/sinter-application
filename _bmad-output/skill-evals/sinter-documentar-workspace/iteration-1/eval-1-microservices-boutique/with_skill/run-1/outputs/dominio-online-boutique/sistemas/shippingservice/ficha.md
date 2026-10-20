---
id: sys-shippingservice
kind: system
subject: system:shippingservice
camada: 4
status: proposed
realiza: [sub-checkout-e-pagamento]
realizado-por: [cmp-shippingservice-grpc]
provenance:
  - source: repo:microservices-demo
    locator: src/shippingservice/main.go#L118-L154
    version: 38e7348
    extraction: extracted
---

# shippingservice

Dá uma cotação de frete e "expede" o pedido (mock: gera um código de rastreio determinístico; não integra transportadora real). `[extracted, README.md#L33]`

| Campo | Valor |
|---|---|
| Subdomínio | Checkout e Pagamento |
| Dono | Não identificado `[a confirmar]` |
| Stack | Go |
| Repositório | `src/shippingservice/` |
| Criticidade | Média-alta — bloqueia a confirmação do pedido se falhar `[inferred]` |

## Expõe

| Contrato | Tipo | Detalhe |
|---|---|---|
| `ShippingService.GetQuote` | gRPC | Custo em USD calculado a partir da contagem de itens (`CreateQuoteFromCount`), endereço não influencia o valor apesar de fazer parte do contrato |
| `ShippingService.ShipOrder` | gRPC | Devolve `tracking_id` mock (`CreateTrackingId`) a partir do endereço |

`[extracted, src/shippingservice/main.go#L118-L154]`

## Consome
- Nenhum outro sistema.

## Dados
Sem persistência — cálculo puro em memória.

## Qualidade
- Determinístico e sem I/O externo — não tem por que falhar em produção normal; falhas seriam de rede/infra, não de regra de negócio.
