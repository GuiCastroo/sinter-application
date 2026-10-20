---
id: res-memorystore-redis
kind: resource
subject: resource:memorystore-redis
camada: 6
status: proposed
realiza: [sys-cartservice]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: terraform/memorystore.tf#L16-L30
    version: 38e7348
    extraction: extracted
---

# Memorystore (Redis gerenciado)

| Campo | Valor |
|---|---|
| Tipo | banco (cache gerenciado) |
| Tecnologia | Google Cloud Memorystore for Redis 7.0, 1 GB |
| Ambientes | Opcional — só é criado se a variável Terraform `memorystore = true`; substitui o `redis-cart` in-cluster |
| Definido em | `terraform/memorystore.tf` (`google_redis_instance.redis-cart`) |

## Usado por
- cartservice — quando o overlay `kustomize/components/memorystore` está ativo, que substitui `REDIS_ADDR` pelo host:porta real da instância (o Terraform reescreve o `kustomization.yaml` do componente via `sed`, trocando o placeholder `REDIS_CONNECTION_STRING`). `[extracted, terraform/memorystore.tf#L32-L45]`

## Observação
Esta é a única alternativa aos três backends do `cartservice` que é efetivamente **provisionada por este próprio Terraform**; Spanner e AlloyDB (ver [res-spanner-cartservice](./spanner-cartservice.md), [res-alloydb](./alloydb.md)) são assumidos como já existentes/providos fora deste repositório.
