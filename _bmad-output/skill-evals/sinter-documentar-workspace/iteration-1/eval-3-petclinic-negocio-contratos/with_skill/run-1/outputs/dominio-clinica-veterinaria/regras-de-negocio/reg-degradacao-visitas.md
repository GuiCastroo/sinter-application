---
id: reg-degradacao-visitas
kind: rule
subject: rule:degradacao-visitas
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java#L52-L64
    version: aefaf7f
    extraction: extracted
---

# A tela do tutor nunca falha por causa do histórico de visitas
Se a busca do histórico de visitas (`visits-service`) falhar ou ficar lenta, o `api-gateway` exibe o tutor e seus pets normalmente, apenas com a lista de visitas vazia — em vez de falhar a tela inteira. Implementado via `ReactiveCircuitBreakerFactory` com fallback `emptyVisitsForPets()`.

## Onde está implementada
- `spring-petclinic-api-gateway` — `ApiGatewayController.getOwnerDetails`

## Conflito
O mesmo tratamento **não existe** para a chamada a `customers-service` no mesmo método — se ela falhar, não há fallback e o comportamento observado pelo usuário não foi confirmado nas fontes lidas. **A confirmar com o arquiteto** se essa assimetria é intencional (ex.: "sem tutor não há o que mostrar mesmo") ou uma lacuna.
