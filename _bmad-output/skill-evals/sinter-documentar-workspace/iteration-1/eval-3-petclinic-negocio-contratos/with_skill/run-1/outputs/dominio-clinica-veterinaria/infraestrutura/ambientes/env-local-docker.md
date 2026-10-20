---
id: env-local-docker
kind: environment
subject: environment:local-docker
camada: 6
status: proposed
realiza: []
realizado-por: [res-tracing-server, res-grafana-prometheus]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: docker-compose.yml
    version: aefaf7f
    extraction: extracted
---

# Ambiente local via Docker Compose
Sobe toda a stack (serviços de negócio + plataforma + observabilidade) em containers na mesma máquina, para desenvolvimento e demonstração. Não há evidência neste repositório de um ambiente de homologação ou produção real (nuvem, Kubernetes, Terraform) — apenas este compose local. **A confirmar com o time de infraestrutura.**

## Implantação
```mermaid
flowchart TB
  subgraph docker["docker-compose (host local)"]
    CFG[config-server :8888] --> DISC[discovery-server :8761]
    DISC --> CUST[customers-service :8081]
    DISC --> VIS[visits-service :8082]
    DISC --> VET[vets-service :8083]
    DISC --> GEN[genai-service :8084]
    DISC --> GW[api-gateway :8080]
    DISC --> ADM[admin-server :9090]
    GW --> CUST
    GW --> VIS
    GW --> VET
    GW --> GEN
    TRACE[tracing-server :9411]
    GRAF[grafana-server :3030] --> PROM[prometheus-server :9091]
  end
```

Ordem de subida (via `depends_on` + `condition: service_healthy`): `config-server` → `discovery-server` → demais serviços. Cada serviço de negócio expõe uma porta fixa mapeada no host: `customers-service` 8081, `visits-service` 8082, `vets-service` 8083, `genai-service` 8084, `api-gateway` 8080, `admin-server` 9090, `discovery-server` 8761, `config-server` 8888. Todos os containers têm limite de memória de 512M (256M para Grafana/Prometheus).
