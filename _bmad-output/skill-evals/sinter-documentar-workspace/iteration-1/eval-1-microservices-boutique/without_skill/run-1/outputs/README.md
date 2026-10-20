# Documentação de Domínio — Online Boutique (microservices-demo)

Este conjunto de documentos descreve o domínio completo do repositório
`microservices-demo` (Online Boutique, demo de e-commerce da Google), com base
em leitura direta do código-fonte, dos manifests Kubernetes, do Helm chart, do
Terraform e do Skaffold presentes no repositório.

Repositório analisado (somente leitura):
`/Users/guilhermesilvacastro/harness_corp/_bmad-output/skill-evals/sinter-documentar-workspace/fixtures/microservices-demo`

## Índice

1. [01-visao-geral-e-servicos.md](./01-visao-geral-e-servicos.md)
   Visão geral do domínio, catálogo dos 11 microsserviços, linguagens,
   responsabilidades e mapa de dependências.
2. [02-comunicacao-entre-servicos.md](./02-comunicacao-entre-servicos.md)
   Como os serviços conversam entre si: protocolo (gRPC/protobuf), contratos
   (`protos/demo.proto`), endereços internos, diagrama de dependências e
   padrões de resiliência (ou a falta deles).
3. [03-infraestrutura-kubernetes.md](./03-infraestrutura-kubernetes.md)
   A infraestrutura Kubernetes: Deployments, Services, probes, segurança,
   Kustomize (base + componentes opcionais), Istio, Helm chart, Terraform e
   pipeline Skaffold/CI.
4. [04-fluxo-de-compra.md](./04-fluxo-de-compra.md)
   O fluxo de compra do cliente passo a passo, da primeira visita à página
   inicial até o e-mail de confirmação do pedido, com diagrama de sequência
   e os pontos exatos do código onde cada etapa acontece.

## Como este material foi produzido

Leitura manual e direta dos seguintes artefatos do repositório (sem uso de
ferramenta de geração automática de documentação):

- `README.md` (raiz) — descrição oficial da arquitetura.
- `protos/demo.proto` — contrato gRPC único, compartilhado por todos os
  serviços.
- `src/checkoutservice/main.go` — orquestração completa do pedido.
- `src/frontend/main.go` e `src/frontend/handlers.go` — rotas HTTP e chamadas
  gRPC de saída do frontend.
- `src/cartservice/src/Startup.cs` e `cartstore/*.cs` — persistência do
  carrinho (Redis/Spanner/AlloyDB).
- `src/paymentservice/charge.js`, `src/shippingservice/*.go`,
  `src/recommendationservice/recommendation_server.py`,
  `src/adservice/src/main/java/hipstershop/AdService.java`,
  `src/shoppingassistantservice/shoppingassistantservice.py`.
- `kubernetes-manifests/*.yaml` — manifests "batteries-included" (Deployment,
  Service, ServiceAccount por serviço).
- `kustomize/base` e `kustomize/components/*` — variantes de infraestrutura
  (Spanner, AlloyDB, Memorystore, Istio, network policies, etc.).
- `istio-manifests/*.yaml` — Gateway, VirtualServices e ServiceEntries.
- `helm-chart/` — chart Helm equivalente aos manifests kustomize.
- `terraform/` — provisionamento do cluster GKE e Memorystore no Google Cloud.
- `skaffold.yaml` e `cloudbuild.yaml` — build/deploy multi-serviço e CI.
- `src/loadgenerator/locustfile.py` — simulação do comportamento real do
  cliente, usada para validar o fluxo de compra descrito no documento 4.
