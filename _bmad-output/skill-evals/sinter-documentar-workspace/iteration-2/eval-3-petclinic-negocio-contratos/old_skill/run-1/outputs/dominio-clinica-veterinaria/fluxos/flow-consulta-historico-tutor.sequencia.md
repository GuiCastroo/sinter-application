---
id: flow-consulta-historico-tutor-sequencia
kind: flow
subject: flow:consulta-historico-tutor:sequencia
camada: 3
status: proposed
realiza: [flow-consulta-historico-tutor]
realizado-por: [ctr-gateway-get-owner-details, ctr-customers-get-owner, ctr-visits-get-visits-batch]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java#L38-L65
    version: aefaf7f
    extraction: extracted
---

# Consulta de histórico do tutor: sequência técnica
Realiza as etapas do [fluxo macro](./flow-consulta-historico-tutor.md). Esta é a única sequência do domínio com um agregador de dados explícito no código (`ApiGatewayController`) e com um caminho de erro tratado deliberadamente (circuit breaker com fallback funcional, não apenas um erro genérico).

## Diagrama
```mermaid
sequenceDiagram
  participant UI as Frontend (AngularJS)
  participant GW as ApiGatewayController
  participant CUST as customers-service
  participant VIS as visits-service

  UI->>GW: GET /api/gateway/owners/{ownerId}
  GW->>CUST: GET /owners/{ownerId} (via lb://customers-service)
  CUST-->>GW: 200 OwnerDetails (com lista de pets e petIds)
  GW->>VIS: GET pets/visits?petId=... (via lb://visits-service)
  alt visits-service responde a tempo
    VIS-->>GW: 200 Visits {items: [...]}
    GW-->>GW: anexa cada visita ao pet correspondente (por petId)
  else timeout ou erro no circuit breaker "getOwnerDetails"
    GW-->>GW: emptyVisitsForPets() -> Visits vazio
  end
  GW-->>UI: 200 OwnerDetails completo (pets com ou sem visitas)
```

## Passos
### Passo 1
`api-gateway` chama `customers-service` diretamente via `WebClient` (`CustomersServiceClient.getOwner`), não através de uma rota do Spring Cloud Gateway — é uma chamada de aplicação, resolvida também por `lb://customers-service` via Eureka. Ver [ctr-customers-get-owner](../sistemas/customers-service/contratos/ctr-customers-get-owner.md).

### Passo 2
Com os `petIds` do owner em mãos, `api-gateway` chama `visits-service` em lote (`VisitsServiceClient.getVisitsForPets`, uma única requisição com todos os ids) e, com `ReactiveCircuitBreakerFactory`, protege essa chamada especificamente. Ver [ctr-visits-get-visits-batch](../sistemas/visits-service/contratos/ctr-visits-get-visits-batch.md) e o contrato do próprio agregador [ctr-gateway-get-owner-details](../sistemas/api-gateway/contratos/ctr-gateway-get-owner-details.md).

### Caminho de erro
Se a chamada a `visits-service` falhar (erro ou timeout — o timeout exato do circuit breaker Resilience4j não foi encontrado nas fontes lidas, **a confirmar**), o circuit breaker `getOwnerDetails` intercepta e devolve uma lista de visitas vazia, em vez de propagar o erro ao usuário. O tutor e seus pets continuam sendo exibidos — apenas sem o histórico de visitas. Se a chamada a `customers-service` falhar, **não há fallback específico neste método**; o comportamento observado pelo usuário final não foi confirmado nas fontes lidas (provavelmente erro 5xx propagado).
