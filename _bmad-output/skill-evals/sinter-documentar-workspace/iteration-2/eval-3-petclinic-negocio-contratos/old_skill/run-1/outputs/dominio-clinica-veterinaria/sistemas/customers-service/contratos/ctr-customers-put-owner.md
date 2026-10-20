---
id: ctr-customers-put-owner
kind: contract
subject: contract:customers-service:PUT-/owners/{ownerId}
camada: 4
status: proposed
realiza: [cap-cadastro-clientes-pets]
realizado-por: [cmp-customers-owner-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/OwnerResource.java#L83-L89
    version: aefaf7f
    extraction: extracted
---

# PUT /owners/{ownerId}
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `customers-service` |
| Consumidores | `api-gateway` (frontend AngularJS, tela de edição de tutor) |
| Especificação | sem OpenAPI; extraído de `OwnerResource.updateOwner` |

Atualiza os dados de um tutor existente. Retorna `204 No Content`. Lança `ResourceNotFoundException` (caminho de erro) se `ownerId` não existir.

## Exemplo
```json
// PUT /owners/1
{ "firstName": "George", "lastName": "Franklin", "address": "110 W. Liberty St.", "city": "Madison", "telephone": "6085551023" }
// -> 204 No Content
```
