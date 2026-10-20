---
id: term-veterinario-especialidade
kind: term
subject: term:veterinario-especialidade
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-vets-service/src/main/java/org/springframework/samples/petclinic/vets/model/Vet.java; Specialty.java
    version: aefaf7f
    extraction: extracted
---

# Veterinário / Especialidade
Veterinário (`Vet`): profissional da clínica, com nome e uma ou mais especialidades. Especialidade (`Specialty`): área de atuação do veterinário (ex.: radiologia — visto em dado de exemplo), associada em relação muitos-para-muitos com `Vet` via `vet_specialties`.

Não confundir com: **Corpo clínico** — o conjunto de todos os veterinários da clínica (capacidade de negócio), não um veterinário individual.
