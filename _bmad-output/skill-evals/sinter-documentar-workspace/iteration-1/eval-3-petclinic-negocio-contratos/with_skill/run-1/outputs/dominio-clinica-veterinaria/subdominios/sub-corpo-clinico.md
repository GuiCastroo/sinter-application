---
id: sub-corpo-clinico
kind: subdomain
subject: subdomain:corpo-clinico
camada: 3
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [sys-vets-service]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-vets-service/
    version: aefaf7f
    extraction: extracted
---

# Subdomínio Corpo Clínico
Mantém o cadastro (somente leitura via API) de veterinários e suas especialidades.

## Sistemas
| Sistema | Papel |
|---|---|
| [vets-service](../sistemas/vets-service/ficha.md) | único sistema do subdomínio; expõe a lista de veterinários e especialidades |

## Fluxos executados aqui
Nenhum fluxo de negócio de ponta a ponta tem seu passo principal aqui — o `vets-service` é consultado como dado de apoio pelo `api-gateway` (tela de veterinários) e pelo `genai-service` (busca semântica de veterinários). Não há fluxo macro dedicado a "gerir corpo clínico" documentado nesta versão — **pergunta ao PM** (ver RELATORIO.md): existe um fluxo de contratação/cadastro de veterinário que não está neste código?
