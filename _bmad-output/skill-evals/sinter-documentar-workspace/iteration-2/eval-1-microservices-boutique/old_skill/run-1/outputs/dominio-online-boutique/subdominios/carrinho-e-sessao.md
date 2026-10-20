---
id: sub-carrinho-e-sessao
kind: subdomain
subject: subdomain:carrinho-e-sessao
camada: 3
status: proposed
realiza: [dom-online-boutique, cap-vender-produtos-online]
realizado-por: [sys-frontend, sys-cartservice]
provenance:
  - source: repo:microservices-demo
    locator: src/frontend/middleware.go#L80-L110
    version: 38e7348
    extraction: extracted
---

# Subdomínio Carrinho e Sessão

Identifica o visitante sem exigir cadastro e mantém o carrinho de compras entre requisições, mesmo sem estado no navegador além de um cookie. `[extracted]`

## Sistemas

| Sistema | Papel |
|---|---|
| [frontend](../sistemas/frontend/ficha.md) | Gera e propaga o `session_id` (cookie `shop_session-id`); usa esse id como `user_id` em todas as chamadas downstream |
| [cartservice](../sistemas/cartservice/ficha.md) | Persiste o carrinho por `user_id`; suporta três backends de dados intercambiáveis (Redis, Cloud Spanner, AlloyDB) |

## Fluxos executados aqui
- [Compra do cliente](../fluxos/compra-do-cliente.sequencia.md) — passos 1, 3, 4 e 10

## Ponto de atenção

O `user_id` é literalmente o valor do cookie de sessão — não há verificação de identidade. Um cliente que limpa cookies ou troca de dispositivo perde o carrinho e "vira" outro usuário. `[inferred a partir da ausência de login]`
