---
id: ctr-gateway-get-owner-details
kind: contract
subject: contract:api-gateway:GET-/api/gateway/owners/{ownerId}
camada: 4
status: proposed
realiza: [cap-atendimento-omnicanal, cap-cadastro-clientes-pets]
realizado-por: [cmp-gateway-controller]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java#L46-L60
    version: aefaf7f
    extraction: extracted
---

# GET /api/gateway/owners/{ownerId}
| Campo | Valor |
|---|---|
| Tipo | API (síncrona do ponto de vista do cliente, implementação reativa) |
| Produtor | `api-gateway` |
| Consumidores | frontend AngularJS (tela de detalhe do tutor) |
| Especificação | sem OpenAPI; extraído de `ApiGatewayController.getOwnerDetails` |

Agrega, numa única resposta, o tutor, seus pets e as visitas de cada pet. É o contrato central do fluxo [Consulta de histórico do tutor](../../../fluxos/flow-consulta-historico-tutor.md) — ver a sequência técnica completa lá, incluindo o caminho de erro do circuit breaker.

## Exemplo
```json
// GET /api/gateway/owners/1 -> 200
{ "id": 1, "firstName": "George", "lastName": "Franklin", "pets": [
  { "id": 1, "name": "Leo", "type": {"id":1,"name":"cat"},
    "visits": [ { "id": 42, "petId": 1, "date": "2026-09-20", "description": "Vacina" } ] } ] }
```
