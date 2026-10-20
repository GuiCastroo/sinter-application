---
id: ctr-customers-get-pettypes
kind: contract
subject: contract:customers-service:GET-/petTypes
camada: 4
status: proposed
realiza: [cap-cadastro-clientes-pets]
realizado-por: [cmp-customers-pet-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java#L48-L51
    version: aefaf7f
    extraction: extracted
---

# GET /petTypes
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `customers-service` |
| Consumidores | `api-gateway` (formulário de cadastro de pet) |
| Especificação | sem OpenAPI; extraído de `PetResource.getPetTypes` |

Lista os tipos de pet cadastrados (dado de referência), usados para popular o formulário de cadastro de pet.

## Exemplo
```json
// GET /petTypes -> 200
[ {"id":1,"name":"cat"}, {"id":2,"name":"dog"}, {"id":3,"name":"lizard"}, {"id":4,"name":"snake"}, {"id":5,"name":"bird"}, {"id":6,"name":"hamster"} ]
```
