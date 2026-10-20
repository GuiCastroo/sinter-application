---
id: term-visita-consulta
kind: term
subject: term:visita-consulta
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/src/main/java/org/springframework/samples/petclinic/visits/model/Visit.java
    version: aefaf7f
    extraction: extracted
---

# Visita / Consulta
Registro de um atendimento veterinário prestado a um pet, com data e descrição textual (até 8192 caracteres). No código é chamado de `Visit`. Usamos "visita" e "consulta" como sinônimos neste domínio, já que o código só usa `Visit`.

Não confundir com: **Prontuário clínico** (exames, prescrições, diagnósticos detalhados) — não encontrado no código; a `Visit` é apenas uma descrição textual livre.
