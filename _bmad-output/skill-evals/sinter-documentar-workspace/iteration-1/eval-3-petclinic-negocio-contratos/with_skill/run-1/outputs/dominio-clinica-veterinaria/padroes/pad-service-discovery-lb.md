---
id: pad-service-discovery-lb
kind: standard
subject: standard:service-discovery-lb
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/application/CustomersServiceClient.java; VisitsServiceClient.java; spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/AIDataProvider.java
    version: aefaf7f
    extraction: extracted
---

# Chamadas entre serviços sempre via nome lógico + Eureka
Nenhum sistema deste domínio chama outro por host/IP fixo. Todas as chamadas HTTP entre sistemas usam o nome lógico do serviço (`http://customers-service/...`, `http://vets-service/...`) resolvido em tempo de execução pelo `discovery-server` (Eureka), seja via `lb://` nas rotas do Spring Cloud Gateway, seja via `WebClient`/`RestClient` com `@LoadBalanced` ou `DiscoveryClient` explícito.

## Exemplo
```java
// api-gateway
uri("http://customers-service/owners/{ownerId}", ownerId)
// genai-service
discoveryClient.getInstances("customers-service").get(0).getUri()
```

## Onde se aplica
- `api-gateway` (`CustomersServiceClient`, `VisitsServiceClient`, rotas do Gateway)
- `genai-service` (`AIDataProvider`, `VectorStoreController`)
