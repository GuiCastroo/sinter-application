---
id: reg-limite-descricao-visita
kind: rule
subject: rule:limite-descricao-visita
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/src/main/java/org/springframework/samples/petclinic/visits/model/Visit.java#L38-L40
    version: aefaf7f
    extraction: extracted
---

# Descrição da visita limitada a 8192 caracteres
A descrição de uma visita (`Visit.description`) é validada com `@Size(max = 8192)` e a coluna do banco é `VARCHAR(8192)`.

## Onde está implementada
- `spring-petclinic-visits-service` — entidade `Visit` e `db/mysql/schema.sql` (coluna `description VARCHAR(8192)`)
