---
id: cmp-visits-visit-api
kind: component
subject: component:visits-service:visit-resource
camada: 5
status: proposed
realiza: [sys-visits-service]
realizado-por: [res-hsqldb-embedded, res-mysql-visits]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/src/main/java/org/springframework/samples/petclinic/visits/web/VisitResource.java
    version: aefaf7f
    extraction: extracted
---

# VisitResource
Endpoint REST para criar e consultar visitas (consultas veterinárias) de um pet.

| Campo | Valor |
|---|---|
| Tipo | endpoint (controller Spring MVC) |
| Gatilho | HTTP, rotas `owners/*/pets/{petId}/visits` e `pets/visits` |
| Entrada | corpo `Visit` (JSON) na criação; `petId` de path ou lista `petId` em query string |
| Saída | `Visit` criada, lista de `Visit`, ou `Visits` (wrapper `items`) na consulta em lote |
| Timeout / memória / concorrência | não configurado explicitamente |

## Dependências
- `VisitRepository` (Spring Data JPA) — métodos `findByPetId` e `findByPetIdIn`

## Erros e retentativas
- Nenhum tratamento de exceção específico identificado; falhas de validação (`@Valid`) retornam 400 pelo handler padrão do Spring.
- Sem fila de mensagens mortas.
