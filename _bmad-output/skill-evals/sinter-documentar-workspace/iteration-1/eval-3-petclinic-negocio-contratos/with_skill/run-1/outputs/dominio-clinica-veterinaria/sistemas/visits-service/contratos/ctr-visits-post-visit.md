---
id: ctr-visits-post-visit
kind: contract
subject: contract:visits-service:POST-owners/*/pets/{petId}/visits
camada: 4
status: proposed
realiza: [cap-registro-consultas]
realizado-por: [cmp-visits-visit-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/src/main/java/org/springframework/samples/petclinic/visits/web/VisitResource.java#L51-L58
    version: aefaf7f
    extraction: extracted
---

# POST owners/*/pets/{petId}/visits
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `visits-service` |
| Consumidores | `api-gateway` (rota `/api/visit/**`, tela de registro de visita) |
| Especificação | sem OpenAPI; extraído de `VisitResource.create` |

Registra uma nova visita para um pet. O `petId` do path sobrescreve o campo do corpo (`visit.setPetId(petId)`). Retorna `201 Created`.

## Exemplo
```json
// POST owners/1/pets/15/visits
{ "date": "2026-09-20", "description": "Vacina antirrábica" }
// -> 201
{ "id": 42, "date": "2026-09-20", "description": "Vacina antirrábica", "petId": 15 }
```
