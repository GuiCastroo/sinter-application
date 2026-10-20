---
id: ctr-gateway-post-fallback
kind: contract
subject: contract:api-gateway:POST-/fallback
camada: 4
status: proposed
realiza: [cap-atendimento-omnicanal]
realizado-por: [cmp-gateway-routes]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/FallbackController.java
    version: aefaf7f
    extraction: extracted
---

# POST /fallback
| Campo | Valor |
|---|---|
| Tipo | API (fallback de circuit breaker) |
| Produtor | `api-gateway` |
| Consumidores | invocado internamente pelas rotas do Gateway (`fallbackUri: forward:/fallback`) quando o serviço de destino falha |
| Especificação | sem OpenAPI; extraído de `FallbackController.fallback` |

Retorna sempre `503 Service Unavailable` com uma mensagem fixa. Usado principalmente quando o `genai-service` está indisponível ("Chat is currently unavailable...").

## Exemplo
```
// POST /fallback -> 503
"Chat is currently unavailable. Please try again later."
```
