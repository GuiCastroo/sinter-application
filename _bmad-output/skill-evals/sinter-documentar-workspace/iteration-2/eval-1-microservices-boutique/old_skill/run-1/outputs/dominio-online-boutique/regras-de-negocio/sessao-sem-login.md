---
id: rule-sessao-sem-login
kind: rule
subject: rule:sessao-sem-login
camada: 0
status: proposed
realiza: []
realizado-por: [cmp-frontend-handlers]
provenance:
  - source: repo:microservices-demo
    locator: src/frontend/middleware.go#L87-L107
    version: 38e7348
    extraction: extracted
  - source: repo:microservices-demo
    locator: README.md#L17
    version: 38e7348
    extraction: extracted
---

# Sessão sem login

A loja não exige cadastro nem autenticação. Ao primeiro acesso, um `session_id` (UUID) é gerado e gravado num cookie (`shop_session-id`, validade de 48h); esse id é usado como `user_id` em todo o domínio (carrinho, checkout). Perder o cookie é perder a identidade — não há recuperação de conta. `[extracted]`

## Onde está implementada
- `src/frontend/middleware.go#L87-L107`
- `src/frontend/main.go#L41-L45`
