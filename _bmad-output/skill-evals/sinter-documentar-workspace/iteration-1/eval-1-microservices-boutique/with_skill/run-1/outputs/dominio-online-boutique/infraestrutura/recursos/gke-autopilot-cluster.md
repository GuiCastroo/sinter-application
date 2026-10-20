---
id: res-gke-autopilot
kind: resource
subject: resource:gke-autopilot-cluster
camada: 6
status: proposed
realiza: [dom-online-boutique]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: terraform/main.tf#L27-L60
    version: 38e7348
    extraction: extracted
---

# Cluster GKE Autopilot

| Campo | Valor |
|---|---|
| Tipo | cluster Kubernetes |
| Tecnologia | Google Kubernetes Engine, modo Autopilot (`enable_autopilot = true`) |
| Ambientes | Provisionamento de referência (`terraform apply`), nome e região vêm de `var.name`/`var.region` |
| Definido em | `terraform/main.tf#L40-L60`, variáveis em `terraform/variables.tf` |

## Usado por
- Todos os 12 sistemas do domínio — é o único cluster onde tudo roda.

## Provisionamento

O Terraform, além de criar o cluster, habilita as APIs do Google Cloud necessárias (`container`, `monitoring`, `cloudtrace`, `cloudprofiler`, e `redis` se `var.memorystore=true`) e aplica os manifestos via `kubectl apply -k ${var.filepath_manifest}` (Kustomize), esperando os pods ficarem prontos. `[extracted, terraform/main.tf#L16-L98]`
