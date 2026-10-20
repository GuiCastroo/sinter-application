---
id: cmp-paymentservice-charge
kind: component
subject: component:paymentservice:charge
camada: 5
status: proposed
realiza: [sys-paymentservice]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: src/paymentservice/charge.js#L61-L86
    version: 38e7348
    extraction: extracted
---

# Charge

| Campo | Valor |
|---|---|
| Tipo | endpoint gRPC |
| Gatilho | chamada `PaymentService.Charge` (só o `checkoutservice` chama) |
| Entrada | `amount: Money`, `credit_card: CreditCardInfo` |
| Saída | `transaction_id` (uuid v4 aleatório) ou erro |
| Timeout / memória / concorrência | Não configurado explicitamente no código; pod sem limites de CPU/memória customizados além do padrão do manifesto `[extracted, kubernetes-manifests/paymentservice.yaml]` |

## Dependências
- Nenhuma (biblioteca `simple-card-validator`, em processo).

## Erros e retentativas
Sem retentativa. Três validações, nesta ordem, cada uma lança uma exceção que vira erro gRPC:
1. `InvalidCreditCard` — número não passa no algoritmo de Luhn/formato.
2. `UnacceptedCreditCard` — bandeira diferente de Visa/MasterCard (ex.: Amex, Diners).
3. `ExpiredCreditCard` — `ano*12+mês` do cartão é anterior ao mês atual.

Nenhuma fila de mensagens mortas — é uma chamada síncrona simples. `[extracted, src/paymentservice/charge.js#L30-L86]`
