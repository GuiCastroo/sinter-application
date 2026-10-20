---
id: ctr-vets-get-vets
kind: contract
subject: contract:vets-service:GET-/vets
camada: 4
status: proposed
realiza: [cap-gestao-corpo-clinico]
realizado-por: [cmp-vets-vet-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-vets-service/src/main/java/org/springframework/samples/petclinic/vets/web/VetResource.java#L36-L40
    version: aefaf7f
    extraction: extracted
---

# GET /vets
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `vets-service` |
| Consumidores | `api-gateway` (rota `/api/vet/**`, tela de lista de veterinários), `genai-service` (`VectorStoreController` no startup, para popular o vector store de RAG) |
| Especificação | sem OpenAPI; extraído de `VetResource.showResourcesVetList` |

Retorna a lista completa de veterinários com suas especialidades. Resposta cacheada em produção (`@Cacheable("vets")`).

## Exemplo
```json
// GET /vets -> 200
[ { "id": 1, "firstName": "James", "lastName": "Carter", "specialties": [] },
  { "id": 2, "firstName": "Helen", "lastName": "Leary", "specialties": [ {"id":1,"name":"radiology"} ] } ]
```
