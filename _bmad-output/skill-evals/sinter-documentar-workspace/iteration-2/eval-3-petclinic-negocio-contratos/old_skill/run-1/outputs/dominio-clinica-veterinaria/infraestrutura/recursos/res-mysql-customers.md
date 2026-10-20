---
id: res-mysql-customers
kind: resource
subject: resource:mysql-customers
camada: 6
status: proposed
realiza: [sys-customers-service]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/resources/db/mysql/schema.sql
    version: aefaf7f
    extraction: extracted
---

# Banco MySQL — customers-service
| Campo | Valor |
|---|---|
| Tipo | banco (relacional) |
| Tecnologia | MySQL (banco lógico `petclinic`, tabelas `owners`, `pets`, `types`) |
| Ambientes | produção (inferido — a conexão real não está neste repositório) |
| Definido em | `spring-petclinic-customers-service/src/main/resources/db/mysql/schema.sql` e `data.sql` |

O schema e a massa de dados MySQL existem no código (driver `mysql-connector-j` no `pom.xml`), mas **nenhum arquivo deste repositório define host, credenciais ou string de conexão** para MySQL em produção — nem em `docker-compose.yml` (que não sobe um container MySQL), nem em `application.yml`. O Config Server aponta para um repositório Git externo (`spring-petclinic-microservices-config`) que provavelmente contém essas propriedades por ambiente. **Inferido**, a confirmar com o time de infraestrutura (ver RELATORIO.md).

## Usado por
- `sys-customers-service` — leitura e escrita
