---
id: flow-registro-consulta-sequencia
kind: flow
subject: flow:registro-consulta:sequencia
camada: 3
status: proposed
realiza: [flow-registro-consulta]
realizado-por: [ctr-visits-post-visit]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/src/main/java/org/springframework/samples/petclinic/visits/web/VisitResource.java#L51-L58; spring-petclinic-api-gateway/src/main/resources/application.yml
    version: aefaf7f
    extraction: extracted
---

# Registro de consulta veterinária: sequência técnica
Realiza as etapas do [fluxo macro](./flow-registro-consulta.md).

## Diagrama
```mermaid
sequenceDiagram
  participant UI as Frontend (AngularJS)
  participant GW as api-gateway
  participant VIS as visits-service

  UI->>GW: POST /api/visit/owners/{ownerId}/pets/{petId}/visits
  GW->>VIS: POST owners/*/pets/{petId}/visits (StripPrefix=2, lb://visits-service)
  alt sucesso
    VIS-->>GW: 201 Created (visita)
    GW-->>UI: 201 Created
  else visits-service indisponível
    GW-->>GW: CircuitBreaker/Retry (1x, só para 503)
    GW-->>UI: fallback (POST /fallback) ou erro
  end
```

## Passos
### Passo 1
`api-gateway` roteia `/api/visit/**` para `visits-service` via Eureka. `VisitResource.create` ignora o `petId` do corpo e usa o do path (`visit.setPetId(petId)`), garantindo consistência do vínculo. Ver [ctr-visits-post-visit](../sistemas/visits-service/contratos/ctr-visits-post-visit.md).

### Caminho de erro
- Se `visits-service` estiver fora do ar, o filtro padrão do Gateway (`CircuitBreaker` + `Retry` para `POST`/`503`) tenta 1 vez antes de cair no fallback genérico (`/fallback`, sempre `503`).
- `visits-service` **não valida** se o `petId` existe de fato em `customers-service` antes de gravar — uma visita pode ser registrada para um `petId` inexistente sem erro (ver nota em [sys-visits-service](../sistemas/visits-service/ficha.md)). **A confirmar com o arquiteto** se isso é aceitável ou se falta uma validação.
