---
id: cap-atendimento-inteligente
kind: capability
subject: capability:atendimento-inteligente
camada: 1
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [flow-atendimento-assistente-virtual]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/
    version: aefaf7f
    extraction: inferred
---

# Atender por assistente virtual (IA generativa)
A clínica oferece um canal conversacional em que o usuário pergunta ou pede ações sobre tutores, pets e veterinários em linguagem natural, sem precisar navegar pelas telas tradicionais.

## Fluxos que a realizam
- [Atendimento via assistente virtual](../fluxos/flow-atendimento-assistente-virtual.md)

## Sistemas envolvidos
- `genai-service` — dono da capacidade (orquestra LLM + tools)
- `customers-service`, `vets-service` — fontes de dado consultadas/alteradas pelo assistente
- `api-gateway` — canal de acesso
