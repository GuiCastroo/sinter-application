---
id: cmp-customers-pet-api
kind: component
subject: component:customers-service:pet-resource
camada: 5
status: proposed
realiza: [sys-customers-service]
realizado-por: [res-hsqldb-embedded, res-mysql-customers]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java
    version: aefaf7f
    extraction: extracted
---

# PetResource
Endpoint REST para tipos de pet e para criar/consultar/atualizar pets de um tutor.

| Campo | Valor |
|---|---|
| Tipo | endpoint (controller Spring MVC) |
| Gatilho | HTTP, rotas `/petTypes` e `/owners/{ownerId}/pets/**` |
| Entrada | `PetRequest` (JSON) ou `ownerId`/`petId` de path |
| Saída | entidade `Pet`, `PetDetails` ou lista de `PetType` (JSON) |
| Timeout / memória / concorrência | não configurado explicitamente neste componente |

## Dependências
- `PetRepository` — leitura/escrita de `pets`, consulta de `types`
- `OwnerRepository` — para associar o pet criado ao tutor (`owner.addPet(pet)`)

## Erros e retentativas
- `processCreationForm` lança `ResourceNotFoundException` se o `ownerId` não existir.
- `findPetById` (usado por `findPet` e `processUpdateForm`) lança `ResourceNotFoundException` se o pet não existir.
- Sem fila de mensagens mortas.
