---
id: res-tracing-server
kind: resource
subject: resource:tracing-server-zipkin
camada: 6
status: proposed
realiza: [sub-plataforma]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: docker-compose.yml#L100-L108
    version: aefaf7f
    extraction: extracted
---

# Servidor de tracing distribuído (Zipkin)
| Campo | Valor |
|---|---|
| Tipo | cluster/servidor de observabilidade (tracing distribuído) |
| Tecnologia | Zipkin (`openzipkin/zipkin`), via Micrometer Tracing nos serviços |
| Ambientes | local via `docker-compose.yml`, porta `9411` |
| Definido em | `docker-compose.yml` (serviço `tracing-server`) |

## Usado por
- Todos os sistemas Spring Boot do domínio publicam traces aqui (Micrometer Tracing é citado no README do repositório); não há evidência de qual exportador exato é usado em cada serviço além da menção no README raiz — **inferido**.
