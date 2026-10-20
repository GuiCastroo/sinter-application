---
id: ctr-customers-post-pet
kind: contract
subject: contract:customers-service:POST-/owners/{ownerId}/pets
camada: 4
status: proposed
realiza: [cap-cadastro-clientes-pets]
realizado-por: [cmp-customers-pet-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java#L53-L61
    version: aefaf7f
    extraction: extracted
---

# POST /owners/{ownerId}/pets
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `customers-service` |
| Consumidores | `api-gateway` (formulário de cadastro de pet), `genai-service` (tool `addPetToOwner`) |
| Especificação | sem OpenAPI; extraído de `PetResource.processCreationForm` |

Cria um novo pet associado a um tutor existente. IDs de tipo de pet válidos: 1=cat, 2=dog, 3=lizard, 4=snake, 5=bird, 6=hamster (conforme descrição da tool `addPetToOwner` do `genai-service`). Retorna `201 Created`.

## Exemplo
```json
// POST /owners/1/pets
{ "name": "Rex", "birthDate": "2022-01-10", "typeId": 2 }
// -> 201
{ "id": 15, "name": "Rex", "birthDate": "2022-01-10", "type": {"id":2,"name":"dog"} }
```
