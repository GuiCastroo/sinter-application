---
id: sys-recommendationservice
kind: system
subject: system:recommendationservice
camada: 4
status: proposed
realiza: [sub-catalogo-e-descoberta]
realizado-por: [cmp-recommendationservice-grpc]
provenance:
  - source: repo:microservices-demo
    locator: src/recommendationservice/recommendation_server.py#L70-L86
    version: 38e7348
    extraction: extracted
---

# recommendationservice

Sugere produtos a partir dos itens já no carrinho do cliente. `[extracted, README.md#L34]`

| Campo | Valor |
|---|---|
| Subdomínio | Catálogo e Descoberta |
| Dono | Não identificado `[a confirmar]` |
| Stack | Python |
| Repositório | `src/recommendationservice/` |
| Criticidade | Baixa — degrada a experiência mas não bloqueia compra `[inferred, src/frontend/handlers.go#L316 usa `_` para ignorar erro]` |

## Expõe

| Contrato | Tipo | Detalhe |
|---|---|---|
| `RecommendationService.ListRecommendations` | gRPC | Recebe `user_id` + ids já no carrinho; devolve uma amostra **aleatória** dos demais produtos do catálogo (`random.sample`), excluindo os já presentes |

`[extracted, protos/demo.proto#L56-L67; src/recommendationservice/recommendation_server.py#L70-L86]`

## Consome
- productcatalogservice.ListProducts — para saber o universo de produtos a sortear.

## Regra de negócio
Ver [recomendação não é personalizada](../../regras-de-negocio/recomendacao-nao-e-personalizada.md) — não há modelo de ML nem histórico de compras envolvido, apesar do nome do serviço.
