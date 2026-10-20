---
id: sub-consultas
kind: subdomain
subject: subdomain:consultas
camada: 3
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [sys-visits-service]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-visits-service/
    version: aefaf7f
    extraction: extracted
---

# Subdomínio Consultas
Registra e consulta o histórico de visitas (consultas veterinárias) de cada pet.

## Sistemas
| Sistema | Papel |
|---|---|
| [visits-service](../sistemas/visits-service/ficha.md) | único sistema do subdomínio; expõe registro e consulta de visitas |

## Fluxos executados aqui
- [Registro de consulta veterinária](../fluxos/flow-registro-consulta.sequencia.md) — executado inteiramente dentro deste subdomínio
- [Consulta de histórico do tutor](../fluxos/flow-consulta-historico-tutor.sequencia.md) — este subdomínio fornece o passo de leitura das visitas
