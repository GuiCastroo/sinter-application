---
id: res-redis-cart
kind: resource
subject: resource:redis-cart
camada: 6
status: proposed
realiza: [sys-cartservice]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: kubernetes-manifests/cartservice.yaml
    version: 38e7348
    extraction: extracted
---

# redis-cart

| Campo | Valor |
|---|---|
| Tipo | banco (cache in-memory) |
| Tecnologia | Redis (imagem `redis:alpine`, container `redis` no mesmo manifesto do `cartservice`) |
| Ambientes | Padrão em todos os ambientes que usam a base do `kubernetes-manifests/` sem overlay; removido pelos overlays `memorystore`, `spanner` e `alloydb` |
| Definido em | `kubernetes-manifests/cartservice.yaml` (Deployment `redis-cart`, Service `redis-cart:6379`, volume `emptyDir` chamado `redis-data`) |

## Usado por
- cartservice — leitura e escrita do carrinho (`REDIS_ADDR=redis-cart:6379`)

## Observação
O volume é `emptyDir` — **não sobrevive a um restart do pod**; o carrinho é efetivamente descartável/não durável neste ambiente padrão. `[extracted]`
