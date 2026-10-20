---
id: cmp-vets-vet-api
kind: component
subject: component:vets-service:vet-resource
camada: 5
status: proposed
realiza: [sys-vets-service]
realizado-por: [res-hsqldb-embedded, res-mysql-vets]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-vets-service/src/main/java/org/springframework/samples/petclinic/vets/web/VetResource.java
    version: aefaf7f
    extraction: extracted
---

# VetResource
Endpoint REST único que lista veterinários com suas especialidades.

| Campo | Valor |
|---|---|
| Tipo | endpoint (controller Spring MVC) |
| Gatilho | HTTP GET `/vets` |
| Entrada | nenhuma (sem parâmetros) |
| Saída | lista de `Vet` (JSON), cada um com suas `specialties` |
| Timeout / memória / concorrência | não configurado explicitamente |

## Dependências
- `VetRepository` (Spring Data JPA)
- Cache Spring (`@Cacheable("vets")`), ativo apenas no perfil `production`

## Erros e retentativas
- Nenhum tratamento de erro específico identificado neste componente; falhas de banco propagam como erro 5xx padrão do Spring.
