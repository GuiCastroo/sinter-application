---
id: pad-metricas-timed
kind: standard
subject: standard:metricas-timed
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/OwnerResource.java#L40; PetResource.java#L37; spring-petclinic-visits-service/src/main/java/org/springframework/samples/petclinic/visits/web/VisitResource.java#L44
    version: aefaf7f
    extraction: extracted
---

# Controllers anotados com @Timed("petclinic.<recurso>")
Cada controller REST de negócio é anotado com `@Timed` do Micrometer, usando o padrão de nome `petclinic.<recurso>` (`petclinic.owner`, `petclinic.pet`, `petclinic.visit`), exportado ao Prometheus.

## Exemplo
```java
@RequestMapping("/owners")
@RestController
@Timed("petclinic.owner")
class OwnerResource { ... }
```

## Onde se aplica
- `customers-service` (`OwnerResource`, `PetResource`)
- `visits-service` (`VisitResource`)
- `vets-service` não segue este padrão — `VetResource` não tem `@Timed` (**inferido**: inconsistência a confirmar com o time).
