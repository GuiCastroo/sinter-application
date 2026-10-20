---
id: cmp-customers-owner-api
kind: component
subject: component:customers-service:owner-resource
camada: 5
status: proposed
realiza: [sys-customers-service]
realizado-por: [res-hsqldb-embedded, res-mysql-customers]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/OwnerResource.java
    version: aefaf7f
    extraction: extracted
---

# OwnerResource
Endpoint REST para criar, consultar e atualizar tutores (owners).

| Campo | Valor |
|---|---|
| Tipo | endpoint (controller Spring MVC) |
| Gatilho | HTTP, prefixo `/owners` |
| Entrada | `OwnerRequest` (JSON validado com Bean Validation) ou `ownerId` de path |
| Saída | entidade `Owner` (JSON) ou `204 No Content` na atualização |
| Timeout / memória / concorrência | não configurado explicitamente neste componente |

## Dependências
- `OwnerRepository` (Spring Data JPA) — leitura e escrita da tabela `owners`
- `OwnerEntityMapper` — mapeia `OwnerRequest` para a entidade `Owner`

## Erros e retentativas
- `findOwner` retorna `Optional<Owner>` — se vazio, o Spring serializa `null`/404 conforme configuração padrão (não há tratamento explícito neste método).
- `updateOwner` lança `ResourceNotFoundException` se o owner não existir.
- Sem fila de mensagens mortas — este componente não consome filas.
