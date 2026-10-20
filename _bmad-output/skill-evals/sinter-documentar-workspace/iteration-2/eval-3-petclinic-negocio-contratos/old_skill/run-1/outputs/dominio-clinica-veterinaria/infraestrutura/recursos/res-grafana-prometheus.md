---
id: res-grafana-prometheus
kind: resource
subject: resource:grafana-prometheus
camada: 6
status: proposed
realiza: [sub-plataforma]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: docker-compose.yml#L110-L130; docker/grafana; docker/prometheus
    version: aefaf7f
    extraction: extracted
---

# Grafana + Prometheus (métricas)
| Campo | Valor |
|---|---|
| Tipo | cluster/servidor de observabilidade (métricas e dashboards) |
| Tecnologia | Prometheus (scrape) + Grafana (dashboards), imagens customizadas em `docker/grafana` e `docker/prometheus` |
| Ambientes | local via `docker-compose.yml`, portas `3030` (Grafana) e `9091` (Prometheus) |
| Definido em | `docker-compose.yml` (serviços `grafana-server`, `prometheus-server`) |

Todos os serviços Spring Boot do domínio expõem métricas via `micrometer-registry-prometheus` (dependência presente nos `pom.xml`), consumidas pelo Prometheus e visualizadas no Grafana (há um dashboard de exemplo em `docs/grafana-custom-metrics-dashboard.png`).

## Usado por
- `sys-customers-service`, `sys-vets-service`, `sys-visits-service`, `sys-api-gateway`, `sys-genai-service` — expõem métricas Micrometer/Prometheus
