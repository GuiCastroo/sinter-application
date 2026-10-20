---
id: res-hsqldb-embedded
kind: resource
subject: resource:hsqldb-embedded
camada: 6
status: proposed
realiza: [sys-customers-service, sys-vets-service, sys-visits-service]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/pom.xml#hsqldb-dependency; spring-petclinic-customers-service/src/main/resources/db/hsqldb/schema.sql
    version: aefaf7f
    extraction: extracted
---

# Banco HSQLDB embutido (dev/teste)
| Campo | Valor |
|---|---|
| Tipo | banco (relacional, em memória) |
| Tecnologia | HSQLDB, uma instância por serviço, embutida no processo Java |
| Ambientes | desenvolvimento local (perfil padrão) e testes automatizados (perfil `test`) |
| Definido em | `pom.xml` de cada serviço (dependência `org.hsqldb:hsqldb`), scripts `src/main/resources/db/hsqldb/schema.sql` e `data.sql` de cada serviço |

Cada serviço de dados (`customers-service`, `vets-service`, `visits-service`) inicializa seu próprio banco HSQLDB em memória ao subir, populado com dados de exemplo (`data.sql`). Não é compartilhado entre serviços nem entre instâncias — é recriado a cada start. Não há configuração explícita de `spring.datasource` neste repositório: a escolha do banco (HSQLDB vs. MySQL) depende de qual driver e schema o ambiente de execução ativa, o que não é decidido dentro deste repositório (ver `res-mysql-customers` e RELATORIO.md).

## Usado por
- `sys-customers-service` — leitura e escrita das tabelas `owners`, `pets`, `types`
- `sys-vets-service` — leitura das tabelas `vets`, `specialties`, `vet_specialties`
- `sys-visits-service` — leitura e escrita da tabela `visits`
