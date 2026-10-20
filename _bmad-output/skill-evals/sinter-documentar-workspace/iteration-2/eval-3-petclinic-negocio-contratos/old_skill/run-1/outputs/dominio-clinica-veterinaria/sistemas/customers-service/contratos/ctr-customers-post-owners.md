---
id: ctr-customers-post-owners
kind: contract
subject: contract:customers-service:POST-/owners
camada: 4
status: proposed
realiza: [cap-cadastro-clientes-pets]
realizado-por: [cmp-customers-owner-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/OwnerResource.java#L57-L62
    version: aefaf7f
    extraction: extracted
---

# POST /owners
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `customers-service` |
| Consumidores | `api-gateway` (frontend AngularJS), `genai-service` (tool `addOwnerToPetclinic`) |
| Especificação | sem OpenAPI; extraído de `OwnerResource.createOwner` |

Cria um novo tutor. Retorna `201 Created` com o owner criado (incluindo `id` gerado).

## Exemplo
```json
// request
{ "firstName": "Ana", "lastName": "Souza", "address": "Rua 1", "city": "Curitiba", "telephone": "41999990000" }
// response 201
{ "id": 11, "firstName": "Ana", "lastName": "Souza", "address": "Rua 1", "city": "Curitiba", "telephone": "41999990000", "pets": [] }
```
