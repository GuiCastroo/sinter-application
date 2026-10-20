---
id: cmp-admin-server-app
kind: component
subject: component:admin-server:app
camada: 5
status: proposed
realiza: [sys-admin-server]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-admin-server/src/main/java/org/springframework/samples/petclinic/admin/SpringBootAdminApplication.java
    version: aefaf7f
    extraction: extracted
---

# SpringBootAdminApplication
| Campo | Valor |
|---|---|
| Tipo | endpoint (UI + agregador Spring Boot Admin) |
| Gatilho | HTTP, acesso via navegador; polling nos endpoints Actuator dos serviços registrados no Eureka |
| Entrada | lista de instâncias do `discovery-server` |
| Saída | dashboard web de saúde/métricas |
| Timeout / memória / concorrência | não configurado explicitamente |

## Dependências
- `discovery-server` (para descobrir quais instâncias monitorar)

## Erros e retentativas
- Nada customizado identificado nas fontes lidas.
