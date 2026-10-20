---
id: env-producao-gke
kind: environment
subject: environment:producao-gke
camada: 6
status: proposed
realiza: [dom-online-boutique]
realizado-por: [res-gke-autopilot, res-redis-cart]
provenance:
  - source: repo:microservices-demo
    locator: kubernetes-manifests/kustomization.yaml
    version: 38e7348
    extraction: extracted
---

# Ambiente padrão (base Kubernetes / GKE Autopilot)

Configuração de referência do repositório: um único namespace, 11 Deployments + Services de aplicação, mais o Redis in-cluster. Sem overlay aplicado, este é o comportamento: backend de carrinho = Redis in-cluster, sem malha Istio, sem assistente de IA, com `loadgenerator` ativo. `[extracted, kubernetes-manifests/kustomization.yaml]`

## Implantação

```mermaid
flowchart TB
  subgraph gke["Cluster GKE Autopilot"]
    subgraph ns["namespace default"]
      FE[frontend :8080] 
      CO[checkoutservice :5050]
      CT[cartservice :7070]
      PC[productcatalogservice :3550]
      CU[currencyservice :7000]
      PAY[paymentservice :50051]
      SH[shippingservice :50051]
      EM[emailservice :5000-8080]
      RC[recommendationservice :8080]
      AD[adservice :9555]
      LG[loadgenerator]
      REDIS[(redis-cart :6379 - emptyDir)]
    end
  end
  Cliente((Cliente)) -->|LoadBalancer :80| FE
  LG --> FE
  CT --> REDIS
```
`[extracted, kubernetes-manifests/*.yaml — portas e nomes de Service extraídos de cada manifesto]`

## Segurança de container (aplicada a todos os Deployments)
`runAsNonRoot`, `runAsUser/Group 1000`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]` — ver [padrão de segurança de containers](../../padroes/seguranca-de-containers.md). `[extracted, presente em todos os `kubernetes-manifests/*.yaml`]`

## Probes
Todo serviço gRPC usa `readinessProbe`/`livenessProbe` do tipo `grpc` na própria porta do serviço (recurso nativo do Kubernetes ≥ 1.24, sem sidecar de grpc_health_probe). O `frontend` usa `httpGet /_healthz`. `[extracted]`
