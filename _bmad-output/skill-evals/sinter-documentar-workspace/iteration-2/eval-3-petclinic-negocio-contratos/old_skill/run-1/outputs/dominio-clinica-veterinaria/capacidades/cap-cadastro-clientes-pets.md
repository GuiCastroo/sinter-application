---
id: cap-cadastro-clientes-pets
kind: capability
subject: capability:cadastro-clientes-pets
camada: 1
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [flow-cadastro-tutor-pet, flow-consulta-historico-tutor]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/
    version: aefaf7f
    extraction: inferred
---

# Cadastrar e manter clientes e seus pets
A clínica consegue cadastrar tutores e seus pets, mantendo esse cadastro atualizado e disponível para todos os demais atendimentos.

## Fluxos que a realizam
- [Cadastro de tutor e pet](../fluxos/flow-cadastro-tutor-pet.md)
- [Consulta de histórico do tutor](../fluxos/flow-consulta-historico-tutor.md)

## Sistemas envolvidos
- `customers-service` — dono do cadastro (CRUD completo)
- `api-gateway` — canal de acesso ao cadastro
- `genai-service` — canal alternativo (assistente virtual) para consultar/cadastrar
