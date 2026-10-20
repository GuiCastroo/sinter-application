---
id: env-variantes-kustomize
kind: environment
subject: environment:variantes-kustomize
camada: 6
status: proposed
realiza: [dom-online-boutique]
realizado-por: [res-memorystore-redis, res-spanner-cartservice, res-alloydb, res-service-mesh-istio]
provenance:
  - source: repo:microservices-demo
    locator: kustomize/components/
    version: 38e7348
    extraction: extracted
---

# Variantes de implantação (componentes Kustomize)

O mesmo conjunto de manifestos base pode ser combinado com "componentes" Kustomize (`kustomize/components/*`) para trocar comportamento sem alterar código. Cada linha abaixo é independente e combinável (exceto os 3 backends de carrinho, mutuamente exclusivos). `[extracted, kustomize/components/*/kustomization.yaml]`

| Componente | Efeito |
|---|---|
| `memorystore` | Troca `redis-cart` in-cluster por [Memorystore gerenciado](../recursos/memorystore-redis.md); único provisionado pelo Terraform deste repo |
| `spanner` | Troca o backend do cartservice para [Cloud Spanner](../recursos/spanner-cartservice.md) (instância externa assumida) |
| `alloydb` | Troca o backend do cartservice para [AlloyDB](../recursos/alloydb.md) (instância externa assumida) |
| `shopping-assistant` | Adiciona o Deployment do `shoppingassistantservice` e liga `ENABLE_ASSISTANT=true` no frontend |
| `service-mesh-istio` | Adiciona Gateway/VirtualService Istio e regra de egress para `*.googleapis.com` |
| `cymbal-branding` | Reskin visual do frontend (variável `CYMBAL_BRANDING=true`) — sem impacto funcional |
| `non-public-frontend` | Remove o Service `LoadBalancer` externo do frontend (torna a loja acessível só de dentro do cluster) |
| `network-policies` | Adiciona uma `NetworkPolicy` por serviço restringindo tráfego leste-oeste |
| `without-loadgenerator` | Remove o Deployment do `loadgenerator` |
| `single-shared-session` | Fixa uma única sessão compartilhada (útil para demos/testes, não para produção real) |
| `google-cloud-operations` | Integra logging/tracing/profiling gerenciado do Google Cloud |
| `container-images-registry` / `-tag` / `-tag-suffix` / `custom-base-url` | Parâmetros de build/publicação de imagem, não afetam comportamento de negócio |

## Diferenças-chave entre ambientes

- **Persistência do carrinho**: só é duradoura fora do padrão (`memorystore`, `spanner` ou `alloydb`); no padrão, um restart do pod `redis-cart` apaga todos os carrinhos ativos (`emptyDir`).
- **Exposição pública**: padrão usa `Service` `LoadBalancer`; `non-public-frontend` e/ou `service-mesh-istio` mudam esse caminho.
- **Recurso de IA**: só existe com `shopping-assistant` + AlloyDB configurado.

## Pergunta em aberto
Qual combinação destes componentes representa o ambiente de **produção real** da empresa (se este repositório for adaptado além da demo)? O repositório, por si, não declara uma combinação "canônica" de produção. `[pergunta para arquiteto/infra]`
