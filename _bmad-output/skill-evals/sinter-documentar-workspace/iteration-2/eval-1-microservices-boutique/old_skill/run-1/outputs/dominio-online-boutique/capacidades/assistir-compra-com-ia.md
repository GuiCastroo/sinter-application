---
id: cap-assistir-compra-com-ia
kind: capability
subject: capability:assistir-compra-com-ia
camada: 1
status: proposed
realiza: []
realizado-por: [sub-assistente-de-compras]
provenance:
  - source: repo:microservices-demo
    locator: src/shoppingassistantservice/shoppingassistantservice.py#L1-L60
    version: 38e7348
    extraction: inferred
  - source: repo:microservices-demo
    locator: kustomize/components/shopping-assistant/kustomization.yaml#L1-L30
    version: 38e7348
    extraction: extracted
---

# Assistir a compra com IA (recurso opcional)

A empresa pode oferecer um assistente conversacional que sugere produtos do catálogo a partir de uma pergunta em linguagem natural do cliente (ex.: "o que você recomenda para decorar minha sala?"). É um recurso opt-in: só existe quando o componente `kustomize/components/shopping-assistant` é aplicado e a env `ENABLE_ASSISTANT=true` está ligada no frontend. `[extracted — flag e componente kustomize condicionais; a natureza "capacidade de negócio" é inferred]`

## Fluxos que a realizam
- Sem fluxo macro dedicado documentado; tecnicamente é uma chamada HTTP isolada `frontend → shoppingassistantservice` (ver [ficha do sistema](../sistemas/shoppingassistantservice/ficha.md)).

## Sistemas envolvidos
- frontend — endpoint `/bot` e página `/assistant`, habilitados por flag
- shoppingassistantservice — busca por similaridade vetorial no catálogo (AlloyDB) e gera a resposta com um modelo Gemini (`ChatGoogleGenerativeAI`)
