---
id: sub-assistente-de-compras
kind: subdomain
subject: subdomain:assistente-de-compras
camada: 3
status: proposed
realiza: [dom-online-boutique, cap-assistir-compra-com-ia]
realizado-por: [sys-shoppingassistantservice]
provenance:
  - source: repo:microservices-demo
    locator: kustomize/components/shopping-assistant/kustomization.yaml#L1-L40
    version: 38e7348
    extraction: extracted
---

# Subdomínio Assistente de Compras

Recurso opcional (desligado por padrão) que responde perguntas em linguagem natural sobre o catálogo usando busca vetorial + um modelo de linguagem generativo. `[extracted]`

## Sistemas

| Sistema | Papel |
|---|---|
| [shoppingassistantservice](../sistemas/shoppingassistantservice/ficha.md) | Recebe a pergunta, busca produtos similares em um vetor armazenado no AlloyDB e gera a resposta com Gemini |

## Fluxos executados aqui

Sem sequência dedicada nesta rodada de documentação — a chamada é isolada (`frontend POST /bot → shoppingassistantservice`), sem orquestração com os demais subdomínios. `[extracted]`

## Ativação

Só existe quando:
1. o overlay Kustomize `kustomize/components/shopping-assistant` é aplicado (adiciona o Deployment do serviço e liga `ENABLE_ASSISTANT=true` no frontend); e
2. as variáveis `PROJECT_ID`, `REGION`, `ALLOYDB_*` estão configuradas.

`[extracted, kustomize/components/shopping-assistant/kustomization.yaml]`
