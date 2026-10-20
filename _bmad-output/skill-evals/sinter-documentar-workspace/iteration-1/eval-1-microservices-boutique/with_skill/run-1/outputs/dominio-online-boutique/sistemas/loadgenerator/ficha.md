---
id: sys-loadgenerator
kind: system
subject: system:loadgenerator
camada: 4
status: proposed
realiza: []
realizado-por: [cmp-loadgenerator-locust]
provenance:
  - source: repo:microservices-demo
    locator: src/loadgenerator/locustfile.py#L1-L90
    version: 38e7348
    extraction: extracted
---

# loadgenerator

Ferramenta de teste/demo (Locust) que simula clientes reais navegando e comprando na loja continuamente. Não faz parte do domínio de negócio — é infraestrutura de teste/demonstração. `[extracted, README.md#L36]`

| Campo | Valor |
|---|---|
| Subdomínio | Nenhum (ferramenta de suporte, atravessa todos) |
| Dono | Não identificado `[a confirmar]` |
| Stack | Python / Locust |
| Repositório | `src/loadgenerator/` |
| Criticidade | Nenhuma para produção real — existe para gerar tráfego de demonstração `[inferred]` |

## Expõe
- Nada; é um cliente HTTP.

## Consome
- `frontend` via HTTP (`FRONTEND_ADDR=frontend:80`), executando literalmente os mesmos passos do [fluxo de compra do cliente](../../fluxos/compra-do-cliente.md): home → trocar moeda → navegar produto → adicionar ao carrinho → ver carrinho → esvaziar carrinho → checkout → logout, com pesos de frequência distintos por tarefa. `[extracted, src/loadgenerator/locustfile.py#L44-L90]`

## Observação
Pode ser removido do deployment via o overlay Kustomize `kustomize/components/without-loadgenerator`. `[extracted]`
