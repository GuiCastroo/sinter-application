---
id: sys-admin-server
kind: system
subject: system:admin-server
camada: 4
status: proposed
realiza: [sub-plataforma]
realizado-por: [cmp-admin-server-app]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-admin-server/src/main/resources/application.yml
    version: aefaf7f
    extraction: extracted
---

# admin-server
Console de administração (Spring Boot Admin) para observar saúde, métricas e logs dos demais serviços. Não implementa capacidade de negócio.

| Campo | Valor |
|---|---|
| Subdomínio | [Plataforma](../../subdominios/sub-plataforma.md) |
| Dono | não informado — a confirmar |
| Stack | Java 17+, Spring Boot 4.0.1, Spring Boot Admin Server |
| Repositório | `spring-petclinic-admin-server/` |
| Criticidade | baixa (opcional — README indica que sua subida é opcional) |

## Contêineres
```mermaid
flowchart LR
  subgraph admin-server
    ADM[Spring Boot Admin UI :9090]
  end
  ADM -.monitora via Eureka.-> DISC[[discovery-server]]
```

## Expõe
| Contrato | Tipo | Detalhe |
|---|---|---|
| UI de administração (`/`) | interface web | não documentado neste repositório |

## Dados
Não possui banco; consulta os endpoints Actuator dos demais serviços em tempo real.
