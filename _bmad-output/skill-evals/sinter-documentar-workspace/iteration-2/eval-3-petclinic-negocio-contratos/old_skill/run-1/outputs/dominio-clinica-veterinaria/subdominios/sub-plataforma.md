---
id: sub-plataforma
kind: subdomain
subject: subdomain:plataforma
camada: 3
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [sys-config-server, sys-discovery-server, sys-admin-server]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-config-server/; spring-petclinic-discovery-server/; spring-petclinic-admin-server/; docker-compose.yml
    version: aefaf7f
    extraction: extracted
---

# Subdomínio Plataforma
Serviços de suporte técnico (configuração centralizada, service discovery, administração e observabilidade) que sustentam todos os demais subdomínios, mas não implementam nenhuma capacidade de negócio da clínica veterinária.

## Sistemas
| Sistema | Papel |
|---|---|
| [config-server](../sistemas/config-server/ficha.md) | configuração centralizada, ponto de partida obrigatório da subida |
| [discovery-server](../sistemas/discovery-server/ficha.md) | registro/descoberta de serviços (Eureka) |
| [admin-server](../sistemas/admin-server/ficha.md) | console de observabilidade (opcional) |

Zipkin (`res-tracing-server`), Grafana e Prometheus (`res-grafana-prometheus`) também pertencem a este subdomínio, mas são tratados como recursos de infraestrutura (não têm código-fonte próprio neste repositório).

## Fluxos executados aqui
Nenhum fluxo de negócio tem passo principal aqui — este subdomínio é atravessado implicitamente por todos os fluxos (toda chamada entre sistemas depende de `discovery-server` para resolver o endereço, e toda subida de serviço depende de `config-server`).
