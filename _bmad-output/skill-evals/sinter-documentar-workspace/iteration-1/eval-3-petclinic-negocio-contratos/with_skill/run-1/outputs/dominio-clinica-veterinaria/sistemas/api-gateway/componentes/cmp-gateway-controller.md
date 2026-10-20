---
id: cmp-gateway-controller
kind: component
subject: component:api-gateway:api-gateway-controller
camada: 5
status: proposed
realiza: [sys-api-gateway]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java
    version: aefaf7f
    extraction: extracted
---

# ApiGatewayController
Endpoint de agregação (padrão *Backend for Frontend*) que junta owner + pets + visitas numa única resposta, evitando que o frontend faça 3 chamadas separadas.

| Campo | Valor |
|---|---|
| Tipo | endpoint (controller reativo WebFlux) |
| Gatilho | HTTP GET `/api/gateway/owners/{ownerId}` |
| Entrada | `ownerId` de path |
| Saída | `OwnerDetails` (JSON) com `pets[].visits` preenchido |
| Timeout / memória / concorrência | reativo (`Mono`), sem timeout explícito configurado no componente |

## Dependências
- `CustomersServiceClient` → `customers-service` (`GET /owners/{ownerId}`)
- `VisitsServiceClient` → `visits-service` (`GET pets/visits?petId=...`)
- `ReactiveCircuitBreakerFactory` (Resilience4j) — protege especificamente a chamada a `visits-service`

## Erros e retentativas
- Se a chamada a `visits-service` falhar (erro ou timeout), o circuit breaker (`cbFactory.create("getOwnerDetails")`) intercepta e retorna `Visits` vazio — o owner e seus pets ainda são exibidos, sem histórico de visitas (degradação graciosa).
- Se a chamada a `customers-service` falhar, não há fallback específico neste método — o erro se propaga (o comportamento final depende do circuit breaker padrão da rota Gateway, se esta chamada passar por ela; **inferido**, pois este é um `WebClient` direto, não uma rota do Gateway).
