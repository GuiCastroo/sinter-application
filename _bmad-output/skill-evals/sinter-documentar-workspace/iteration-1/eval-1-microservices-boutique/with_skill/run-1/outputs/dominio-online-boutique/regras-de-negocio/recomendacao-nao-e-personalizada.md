---
id: rule-recomendacao-nao-e-personalizada
kind: rule
subject: rule:recomendacao-nao-e-personalizada
camada: 0
status: proposed
realiza: []
realizado-por: [sys-recommendationservice]
provenance:
  - source: repo:microservices-demo
    locator: src/recommendationservice/recommendation_server.py#L70-L86
    version: 38e7348
    extraction: extracted
---

# Recomendação não é personalizada

Apesar do nome, o `recommendationservice` não usa histórico de compras, similaridade de produto nem qualquer modelo — ele sorteia aleatoriamente até um número fixo de produtos do catálogo que ainda não estão no carrinho (`random.sample`). O `frontend` corta o resultado para no máximo 4 itens exibidos. `[extracted]`

## Onde está implementada
- `src/recommendationservice/recommendation_server.py#L70-L86`
- `src/frontend/rpc.go#L99-L117` (corte para 4 itens)
