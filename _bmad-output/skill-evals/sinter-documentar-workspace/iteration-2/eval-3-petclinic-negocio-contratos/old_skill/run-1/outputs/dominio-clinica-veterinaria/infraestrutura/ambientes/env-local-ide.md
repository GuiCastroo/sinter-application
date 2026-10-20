---
id: env-local-ide
kind: environment
subject: environment:local-ide
camada: 6
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: README.md#Starting-services-locally-without-Docker
    version: aefaf7f
    extraction: extracted
---

# Ambiente local via IDE / Maven
Cada microsserviço roda como processo Java independente (`../mvnw spring-boot:run` ou execução pela IDE), sem containers. `config-server` e `discovery-server` precisam subir antes dos demais. Tracing (Zipkin), Admin Server, Grafana e Prometheus são opcionais nesse modo. Usa banco HSQLDB embutido por padrão (ver `res-hsqldb-embedded`).

## Implantação
```mermaid
flowchart TB
  subgraph local["Processos Java locais"]
    CFG[config-server] --> DISC[discovery-server]
    DISC --> CUST[customers-service]
    DISC --> VIS[visits-service]
    DISC --> VET[vets-service]
    DISC --> GW["api-gateway :8080"]
  end
```

Portas de negócio não são fixadas em `application.yml` neste modo (nenhum `server.port` explícito nos serviços de negócio) — o README instrui checar a porta real pelo painel do Eureka. **Inferido**: a porta efetiva provavelmente vem de variável de ambiente `SERVER_PORT`, cuja origem (perfil, config externo) não está neste repositório.
