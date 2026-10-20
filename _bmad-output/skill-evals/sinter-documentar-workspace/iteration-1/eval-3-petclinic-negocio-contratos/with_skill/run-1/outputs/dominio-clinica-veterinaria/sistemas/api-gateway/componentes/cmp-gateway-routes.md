---
id: cmp-gateway-routes
kind: component
subject: component:api-gateway:cloud-gateway-routes
camada: 5
status: proposed
realiza: [sys-api-gateway]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/src/main/resources/application.yml#L1-L40
    version: aefaf7f
    extraction: extracted
---

# Rotas do Spring Cloud Gateway
Proxy reverso declarativo que encaminha chamadas do frontend para os serviços de negócio, resolvendo o host via Eureka (`lb://`).

| Campo | Valor |
|---|---|
| Tipo | worker (roteador reativo, WebFlux) |
| Gatilho | HTTP, prefixos `/api/vet/**`, `/api/visit/**`, `/api/customer/**`, `/api/genai/**` |
| Entrada | requisição HTTP do frontend |
| Saída | requisição encaminhada ao serviço alvo, com os 2 primeiros segmentos do path removidos (`StripPrefix=2`) |
| Timeout / memória / concorrência | não configurado explicitamente (sem `httpclient.connect-timeout`/`response-timeout` nas fontes lidas) |

## Dependências
- `discovery-server` — resolve `lb://vets-service`, `lb://visits-service`, `lb://customers-service`, `lb://genai-service`
- `vets-service`, `visits-service`, `customers-service`, `genai-service`

## Erros e retentativas
- Filtro `CircuitBreaker` padrão em todas as rotas, fallback `forward:/fallback`.
- Filtro `Retry` padrão: 1 retentativa, apenas para `POST` com resposta `503 SERVICE_UNAVAILABLE`.
- Rota `genai-service` tem circuit breaker nomeado adicional `genaiCircuitBreaker`.
