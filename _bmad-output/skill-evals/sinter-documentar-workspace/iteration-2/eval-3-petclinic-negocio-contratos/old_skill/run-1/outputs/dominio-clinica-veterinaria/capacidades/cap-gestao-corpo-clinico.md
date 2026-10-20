---
id: cap-gestao-corpo-clinico
kind: capability
subject: capability:gestao-corpo-clinico
camada: 1
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-vets-service/
    version: aefaf7f
    extraction: inferred
---

# Divulgar o corpo clínico e suas especialidades
A clínica consegue apresentar, a tutores e à própria equipe, quais veterinários atendem e em quais especialidades — hoje como um catálogo de consulta, sem fluxo de cadastro/edição exposto por API.

## Fluxos que a realizam
Nenhum fluxo de ponta a ponta foi identificado no código para *gerir* (criar/editar) o corpo clínico — apenas para consultá-lo (dentro do fluxo de [Atendimento via assistente virtual](../fluxos/flow-atendimento-assistente-virtual.md) e nas telas do `api-gateway`). **Pergunta ao PM**: como o cadastro de veterinários é feito hoje (direto no banco, outra ferramenta)?

## Sistemas envolvidos
- `vets-service` — dono do catálogo (somente leitura via API)
- `api-gateway` — canal de consulta (tela de veterinários)
- `genai-service` — canal de consulta (busca semântica de veterinários no chat)
