---
id: ctr-customers-get-owners
kind: contract
subject: contract:customers-service:GET-/owners
camada: 4
status: proposed
realiza: [cap-cadastro-clientes-pets]
realizado-por: [cmp-customers-owner-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/OwnerResource.java#L75-L78
    version: aefaf7f
    extraction: extracted
---

# GET /owners
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `customers-service` |
| Consumidores | `genai-service` (tool `listOwners`, via `AIDataProvider.getAllOwners`) |
| Especificação | sem OpenAPI; extraído de `OwnerResource.findAll` |

Lista todos os tutores cadastrados, sem paginação nem filtro.

## Exemplo
```json
// GET /owners -> 200
[ { "id": 1, "firstName": "George", "lastName": "Franklin", "pets": [ /* ... */ ] } ]
```
