---
id: res-mysql-vets
kind: resource
subject: resource:mysql-vets
camada: 6
status: proposed
realiza: [sys-vets-service]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-vets-service/src/main/resources/db/mysql/schema.sql
    version: aefaf7f
    extraction: extracted
---

# Banco MySQL — vets-service
| Campo | Valor |
|---|---|
| Tipo | banco (relacional) |
| Tecnologia | MySQL (banco lógico `petclinic`, tabelas `vets`, `specialties`, `vet_specialties`) |
| Ambientes | produção (inferido — mesma ressalva de `res-mysql-customers`) |
| Definido em | `spring-petclinic-vets-service/src/main/resources/db/mysql/schema.sql` e `data.sql` |

## Usado por
- `sys-vets-service` — leitura (o serviço não expõe escrita de veterinários; a carga inicial vem de `data.sql`)
