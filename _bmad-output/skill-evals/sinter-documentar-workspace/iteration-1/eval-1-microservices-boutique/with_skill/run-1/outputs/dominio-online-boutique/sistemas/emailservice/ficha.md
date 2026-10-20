---
id: sys-emailservice
kind: system
subject: system:emailservice
camada: 4
status: proposed
realiza: [sub-checkout-e-pagamento]
realizado-por: [cmp-emailservice-grpc]
provenance:
  - source: repo:microservices-demo
    locator: src/emailservice/email_server.py#L60-L118
    version: 38e7348
    extraction: extracted
---

# emailservice

Envia (mock, por padrão) o e-mail de confirmação do pedido. `[extracted, README.md#L32]`

| Campo | Valor |
|---|---|
| Subdomínio | Checkout e Pagamento |
| Dono | Não identificado `[a confirmar]` |
| Stack | Python |
| Repositório | `src/emailservice/` |
| Criticidade | Baixa — falha aqui não impede o pedido (ver [regra](../../regras-de-negocio/falha-pos-cobranca-nao-reverte-pedido.md)) `[extracted, src/checkoutservice/main.go#L277-L282]` |

## Expõe

| Contrato | Tipo | Detalhe |
|---|---|---|
| `EmailService.SendOrderConfirmation` | gRPC | Recebe e-mail + `OrderResult`; em modo padrão (`dummy_mode`) só loga; se configurado, usa a API do SendGrid |

`[extracted, protos/demo.proto#L199-L220; src/emailservice/email_server.py#L86-L118]`

## Consome
- Nenhum outro sistema do domínio; opcionalmente a API externa do SendGrid, se configurada (fora do escopo padrão do repositório). `[extracted]`

## Qualidade
- Chamada é best-effort do ponto de vista do `checkoutservice` — erro é logado como aviso, nunca falha o pedido.
