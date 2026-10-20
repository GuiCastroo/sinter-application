---
id: res-service-mesh-istio
kind: resource
subject: resource:service-mesh-istio
camada: 6
status: proposed
realiza: [sys-frontend]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: istio-manifests/frontend-gateway.yaml#L15-L30
    version: 38e7348
    extraction: extracted
---

# Malha de serviço (Istio / Cloud Service Mesh)

| Campo | Valor |
|---|---|
| Tipo | gateway / malha de serviço |
| Tecnologia | Istio (`networking.istio.io/v1alpha3`) — Gateway + VirtualService |
| Ambientes | Opcional — pasta `istio-manifests/` aplicada à parte, e/ou overlay `kustomize/components/service-mesh-istio` |
| Definido em | `istio-manifests/frontend-gateway.yaml` (Gateway `frontend-gateway` na porta 80, VirtualService `frontend-ingress` roteando tudo para o serviço `frontend`), `istio-manifests/allow-egress-googleapis.yaml` |

## Usado por
- frontend — recebe o tráfego externo através deste Gateway em vez do `Service` `LoadBalancer` padrão
- Todos os serviços, indiretamente, via anotação `sidecar.istio.io/rewriteAppHTTPProbers: "true"` presente no manifesto do `frontend` `[extracted, kubernetes-manifests/frontend.yaml#L28-L29]`

## Observação
Este é um caminho de rede **alternativo**, não cumulativo por padrão, ao `Service` `frontend-external` (`LoadBalancer`) já definido em `kubernetes-manifests/frontend.yaml`. Qual dos dois é usado em produção depende de qual conjunto de manifestos foi aplicado — não está explícito no repositório qual é o padrão real de produção. `[inferred — pergunta para o time de infra]`
