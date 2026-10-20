---
id: cap-registro-consultas
kind: capability
subject: capability:registro-consultas
camada: 1
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [flow-registro-consulta, flow-consulta-historico-tutor]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/
    version: aefaf7f
    extraction: inferred
---

# Registrar e consultar o histórico de consultas
A clínica consegue registrar cada consulta realizada em um pet e recuperar esse histórico depois, tanto pet a pet quanto agregado por tutor.

## Fluxos que a realizam
- [Registro de consulta veterinária](../fluxos/flow-registro-consulta.md)
- [Consulta de histórico do tutor](../fluxos/flow-consulta-historico-tutor.md)

## Sistemas envolvidos
- `visits-service` — dono do histórico de consultas
- `api-gateway` — canal de acesso (registro e consulta agregada)
