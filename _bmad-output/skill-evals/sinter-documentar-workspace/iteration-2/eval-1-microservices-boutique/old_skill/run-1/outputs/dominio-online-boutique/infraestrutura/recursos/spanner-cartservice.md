---
id: res-spanner-cartservice
kind: resource
subject: resource:spanner-cartservice
camada: 6
status: proposed
realiza: [sys-cartservice]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: kustomize/components/spanner/kustomization.yaml
    version: 38e7348
    extraction: extracted
---

# Cloud Spanner (backend alternativo do cartservice)

| Campo | Valor |
|---|---|
| Tipo | banco (relacional distribuído) |
| Tecnologia | Google Cloud Spanner |
| Ambientes | Opcional — overlay `kustomize/components/spanner` |
| Definido em | `kustomize/components/spanner/kustomization.yaml` (troca env `REDIS_ADDR` por `SPANNER_PROJECT`/`SPANNER_CONNECTION_STRING`, remove o Deployment/Service `redis-cart`, anota a ServiceAccount do `cartservice` com Workload Identity para uma conta de serviço do GCP) |

## Usado por
- cartservice — via `SpannerCartStore.cs`

## Observação
**Este componente Kustomize não cria a instância Spanner** — ele só aponta o serviço para uma instância que precisa existir previamente (o placeholder `SPANNER_DB_USER_GSA_ID` precisa ser preenchido manualmente). Não há Terraform correspondente neste repositório. `[extracted — ausência de recurso `google_spanner_*` em terraform/]`
