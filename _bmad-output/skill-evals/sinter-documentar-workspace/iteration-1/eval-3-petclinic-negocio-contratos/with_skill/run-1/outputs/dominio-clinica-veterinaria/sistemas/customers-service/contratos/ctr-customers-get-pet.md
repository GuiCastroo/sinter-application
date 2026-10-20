---
id: ctr-customers-get-pet
kind: contract
subject: contract:customers-service:GET-owners/*/pets/{petId}
camada: 4
status: proposed
realiza: [cap-cadastro-clientes-pets]
realizado-por: [cmp-customers-pet-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java#L86-L90
    version: aefaf7f
    extraction: extracted
---

# GET owners/*/pets/{petId}
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `customers-service` |
| Consumidores | `api-gateway` (tela de detalhe/edição de pet) |
| Especificação | sem OpenAPI; extraído de `PetResource.findPet` |

Retorna os detalhes de um pet, incluindo o nome completo do tutor (`PetDetails` monta `owner.getFirstName() + " " + owner.getLastName()`).

## Exemplo
```json
// GET owners/1/pets/15 -> 200
{ "id": 15, "name": "Rex", "owner": "Ana Souza", "birthDate": "2022-01-10", "type": {"id":2,"name":"dog"} }
```
