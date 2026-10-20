---
id: term-sessao
kind: term
subject: term:sessao
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: src/frontend/middleware.go#L87-L107
    version: 38e7348
    extraction: extracted
---

# Sessão

Identificador único (UUID) atribuído automaticamente a cada visitante da loja no primeiro acesso, guardado no cookie `shop_session-id`. É o mesmo valor usado como `user_id` em `cartservice` e `checkoutservice` — não representa uma conta de cliente cadastrada.

Não confundir com: "usuário" ou "conta" (não existem no domínio); "carrinho" (é o dado associado à sessão, não a sessão em si).
