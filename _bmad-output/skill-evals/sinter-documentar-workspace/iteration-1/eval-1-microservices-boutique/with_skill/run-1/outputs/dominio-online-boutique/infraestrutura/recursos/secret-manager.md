---
id: res-secret-manager
kind: resource
subject: resource:secret-manager-alloydb
camada: 6
status: proposed
realiza: [sys-shoppingassistantservice]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: src/shoppingassistantservice/shoppingassistantservice.py#L33-L40
    version: 38e7348
    extraction: extracted
---

# Secret Manager (segredo do AlloyDB)

| Campo | Valor |
|---|---|
| Tipo | segredo (não é banco/fila, mas registrado aqui por ser um recurso de infra citado no código) |
| Tecnologia | Google Secret Manager |
| Ambientes | Só quando `shoppingassistantservice` está habilitado |
| Definido em | Nome do segredo vem da env `ALLOYDB_SECRET_NAME`; valor buscado em runtime via `secretmanager_v1.SecretManagerServiceClient` |

## Usado por
- shoppingassistantservice — senha do usuário `postgres` do AlloyDB

## Achado de segurança
Nenhum valor de segredo foi copiado para esta documentação — apenas o nome da variável que aponta para ele (`ALLOYDB_SECRET_NAME`), conforme registrado no [RELATORIO.md](../../RELATORIO.md).
