---
id: ctr-customers-get-owner
kind: contract
subject: contract:customers-service:GET-/owners/{ownerId}
camada: 4
status: proposed
realiza: [cap-cadastro-clientes-pets]
realizado-por: [cmp-customers-owner-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/OwnerResource.java#L67-L70
    version: aefaf7f
    extraction: extracted
---

# GET /owners/{ownerId}
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `customers-service` |
| Consumidores | `api-gateway` (`CustomersServiceClient.getOwner`, via Eureka `lb://customers-service`), `genai-service` (indiretamente, via `listOwners`) |
| Especificação | sem OpenAPI; extraído de `OwnerResource.findOwner` |

Retorna um tutor pelo id, incluindo a lista de pets (`Owner.pets`, carregada `EAGER`). É a chamada base do fluxo [Consulta de histórico do tutor](../../../fluxos/flow-consulta-historico-tutor.md).

## Exemplo
```json
// GET /owners/1 -> 200
{ "id": 1, "firstName": "George", "lastName": "Franklin", "address": "110 W. Liberty St.", "city": "Madison",
  "telephone": "6085551023", "pets": [ { "id": 1, "name": "Leo", "birthDate": "2010-09-07", "type": { "id": 1, "name": "cat" } } ] }
```
