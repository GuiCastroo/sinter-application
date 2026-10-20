---
id: cap-atendimento-omnicanal
kind: capability
subject: capability:atendimento-omnicanal
camada: 1
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [flow-consulta-historico-tutor]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/
    version: aefaf7f
    extraction: inferred
---

# Atender o tutor num único canal digital
A clínica oferece uma única porta de entrada (tela web) onde o tutor ou a equipe encontram, numa mesma consulta, o cadastro, os pets e o histórico de visitas — sem precisar saber que essas informações vêm de sistemas diferentes.

## Fluxos que a realizam
- [Consulta de histórico do tutor](../fluxos/flow-consulta-historico-tutor.md)

## Sistemas envolvidos
- `api-gateway` — canal único e agregador
- `customers-service`, `visits-service`, `vets-service` — fontes de dado agregadas
