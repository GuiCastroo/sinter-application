---
id: std-seguranca-de-containers
kind: standard
subject: standard:seguranca-de-containers
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: kubernetes-manifests/checkoutservice.yaml#L26-L38
    version: 38e7348
    extraction: extracted
---

# Segurança de containers (baseline Kubernetes)

Todo `Deployment` do domínio define o mesmo `securityContext` restritivo, tanto no pod quanto no container: `runAsNonRoot: true`, `runAsUser`/`runAsGroup: 1000`, `fsGroup: 1000`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `privileged: false`, `capabilities.drop: [ALL]`. Cada serviço também tem sua própria `ServiceAccount` dedicada (mesmo nome do serviço).

## Exemplo
```yaml
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop: [ALL]
  privileged: false
  readOnlyRootFilesystem: true
```

## Onde se aplica
Todos os 12 manifestos em `kubernetes-manifests/*.yaml`.
