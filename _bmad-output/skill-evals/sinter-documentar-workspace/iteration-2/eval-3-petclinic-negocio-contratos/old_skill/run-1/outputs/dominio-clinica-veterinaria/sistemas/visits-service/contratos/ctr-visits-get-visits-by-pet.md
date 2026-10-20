---
id: ctr-visits-get-visits-by-pet
kind: contract
subject: contract:visits-service:GET-owners/*/pets/{petId}/visits
camada: 4
status: proposed
realiza: [cap-registro-consultas]
realizado-por: [cmp-visits-visit-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/src/main/java/org/springframework/samples/petclinic/visits/web/VisitResource.java#L60-L63
    version: aefaf7f
    extraction: extracted
---

# GET owners/*/pets/{petId}/visits
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `visits-service` |
| Consumidores | `api-gateway` (tela de histórico de visitas de um pet específico) |
| Especificação | sem OpenAPI; extraído de `VisitResource.read(int petId)` |

Lista as visitas de um único pet.

## Exemplo
```json
// GET owners/1/pets/15/visits -> 200
[ { "id": 42, "date": "2026-09-20", "description": "Vacina antirrábica", "petId": 15 } ]
```
