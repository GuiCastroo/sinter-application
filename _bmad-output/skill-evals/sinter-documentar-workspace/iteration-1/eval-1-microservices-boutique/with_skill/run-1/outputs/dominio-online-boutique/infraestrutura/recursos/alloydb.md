---
id: res-alloydb
kind: resource
subject: resource:alloydb
camada: 6
status: proposed
realiza: [sys-cartservice, sys-shoppingassistantservice]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: kustomize/components/alloydb/kustomization.yaml
    version: 38e7348
    extraction: extracted
---

# AlloyDB

| Campo | Valor |
|---|---|
| Tipo | banco (Postgres-compatível gerenciado) |
| Tecnologia | Google Cloud AlloyDB |
| Ambientes | Opcional — overlays `kustomize/components/alloydb` (cartservice) e `kustomize/components/shopping-assistant` (vetor de produtos) |
| Definido em | `kustomize/components/alloydb/kustomization.yaml`; consumido em código por `src/cartservice/src/cartstore/AlloyDBCartStore.cs` e `src/shoppingassistantservice/shoppingassistantservice.py#L26-L60` |

## Usado por
- cartservice — como terceiro backend possível de carrinho (`ALLOYDB_PRIMARY_IP`)
- shoppingassistantservice — como vector store de embeddings de produto (`AlloyDBVectorStore`), com a senha buscada no [Secret Manager](./secret-manager.md)

## Observação
Assim como o Spanner, não é provisionado pelo Terraform deste repositório — o overlay assume uma instância AlloyDB já existente. `[extracted]`
