---
id: ctr-visits-get-visits-batch
kind: contract
subject: contract:visits-service:GET-pets/visits
camada: 4
status: proposed
realiza: [cap-registro-consultas]
realizado-por: [cmp-visits-visit-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/src/main/java/org/springframework/samples/petclinic/visits/web/VisitResource.java#L65-L69
    version: aefaf7f
    extraction: extracted
---

# GET pets/visits
| Campo | Valor |
|---|---|
| Tipo | API (síncrona, REST/JSON) |
| Produtor | `visits-service` |
| Consumidores | `api-gateway` (`VisitsServiceClient.getVisitsForPets`, chamada em lote no fluxo de agregação de dados do tutor) |
| Especificação | sem OpenAPI; extraído de `VisitResource.read(List<Integer> petIds)` |

Consulta em lote: recebe uma lista de `petId` na query string (`?petId=1&petId=2...`, unidos por vírgula pelo cliente) e retorna todas as visitas desses pets, agrupadas no envelope `{ "items": [...] }`. É a chamada usada pelo fluxo [Consulta de histórico do tutor](../../../fluxos/flow-consulta-historico-tutor.md) para evitar N chamadas (uma por pet).

## Exemplo
```json
// GET pets/visits?petId=15,16 -> 200
{ "items": [ { "id": 42, "date": "2026-09-20", "description": "Vacina antirrábica", "petId": 15 } ] }
```
