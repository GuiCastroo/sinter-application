---
id: term-pet
kind: term
subject: term:pet
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/model/Pet.java
    version: aefaf7f
    extraction: extracted
---

# Pet
Animal de estimação vinculado a um tutor, com nome, data de nascimento e um tipo (`PetType`). É o sujeito das visitas/consultas registradas em `visits-service`.

Não confundir com: **Tipo de pet** (`PetType`) — a espécie/categoria do pet (cat, dog, lizard, snake, bird, hamster), não o pet individual.
