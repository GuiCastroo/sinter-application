---
id: ctr-customers-put-pet
kind: contract
subject: contract:customers-service:PUT-/owners/*/pets/{petId}
camada: 4
status: proposed
realiza: [cap-cadastro-clientes-pets]
realizado-por: [cmp-customers-pet-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java#L63-L68
    version: aefaf7f
    extraction: extracted
---

# PUT /owners/*/pets/{petId}
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `customers-service` |
| Consumidores | `api-gateway` (formulário de edição de pet) |
| Especificação | sem OpenAPI; extraído de `PetResource.processUpdateForm` |

Atualiza nome, data de nascimento e tipo de um pet existente. O `ownerId` no path é ignorado (`*`) — o pet é localizado só por `petId`, presente também no corpo (`PetRequest.id`). Retorna `204 No Content`.

## Exemplo
```json
// PUT /owners/1/pets/15
{ "id": 15, "name": "Rex", "birthDate": "2022-01-10", "typeId": 2 }
// -> 204 No Content
```
