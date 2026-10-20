---
id: cap-descobrir-e-recomendar-produtos
kind: capability
subject: capability:descobrir-e-recomendar-produtos
camada: 1
status: proposed
realiza: []
realizado-por: [sub-catalogo-e-descoberta]
provenance:
  - source: repo:microservices-demo
    locator: src/recommendationservice/recommendation_server.py#L70-L86
    version: 38e7348
    extraction: inferred
---

# Descobrir e recomendar produtos

A empresa consegue guiar o cliente até produtos relevantes: por navegação/busca no catálogo, por recomendações associadas ao que já está no carrinho e por anúncios contextuais nas páginas. `[inferred]`

## Fluxos que a realizam
- Sem fluxo macro dedicado hoje — a descoberta ocorre embutida na navegação e é reforçada na etapa de confirmação do pedido, dentro de [Compra do cliente](../fluxos/compra-do-cliente.md).

## Sistemas envolvidos
- productcatalogservice — lista e busca produtos
- recommendationservice — recomenda produtos a partir do carrinho atual (hoje: seleção aleatória entre os demais produtos, não personalização real — ver [regra](../regras-de-negocio/recomendacao-nao-e-personalizada.md))
- adservice — anúncios por categoria/contexto
