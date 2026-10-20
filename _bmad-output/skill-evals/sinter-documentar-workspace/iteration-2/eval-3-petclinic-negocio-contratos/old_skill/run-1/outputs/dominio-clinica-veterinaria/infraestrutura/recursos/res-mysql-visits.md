---
id: res-mysql-visits
kind: resource
subject: resource:mysql-visits
camada: 6
status: proposed
realiza: [sys-visits-service]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/src/main/resources/db/mysql/schema.sql
    version: aefaf7f
    extraction: extracted
---

# Banco MySQL — visits-service
| Campo | Valor |
|---|---|
| Tipo | banco (relacional) |
| Tecnologia | MySQL (banco lógico `petclinic`, tabela `visits`) |
| Ambientes | produção (inferido — mesma ressalva de `res-mysql-customers`) |
| Definido em | `spring-petclinic-visits-service/src/main/resources/db/mysql/schema.sql` e `data.sql` |

A tabela `visits` declara `FOREIGN KEY (pet_id) REFERENCES pets(id)`, mas `pets` vive no banco do `customers-service`. Em uma topologia de um banco MySQL por serviço, essa FK não pode ser aplicada pelo próprio MySQL entre schemas separados — **inferido** que a integridade referencial entre `visits.pet_id` e o pet real é garantida apenas pela aplicação (via chamada HTTP), não pelo banco. A confirmar com o arquiteto.

## Usado por
- `sys-visits-service` — leitura e escrita
