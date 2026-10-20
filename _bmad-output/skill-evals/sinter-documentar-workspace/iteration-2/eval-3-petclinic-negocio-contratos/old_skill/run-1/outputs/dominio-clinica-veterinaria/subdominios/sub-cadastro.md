---
id: sub-cadastro
kind: subdomain
subject: subdomain:cadastro-clientes-pets
camada: 3
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [sys-customers-service]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/
    version: aefaf7f
    extraction: extracted
---

# Subdomínio Cadastro de Clientes e Pets
Mantém o cadastro mestre de tutores e seus pets — é a fonte de verdade referenciada por todos os demais subdomínios (consultas referenciam `pet_id`; o assistente virtual lê e escreve owners/pets).

## Sistemas
| Sistema | Papel |
|---|---|
| [customers-service](../sistemas/customers-service/ficha.md) | único sistema do subdomínio; expõe CRUD de owners e pets, e leitura de tipos de pet |

## Fluxos executados aqui
- [Cadastro de tutor e pet](../fluxos/flow-cadastro-tutor-pet.sequencia.md) — executado inteiramente dentro deste subdomínio
- [Consulta de histórico do tutor](../fluxos/flow-consulta-historico-tutor.sequencia.md) — este subdomínio fornece o passo de leitura do owner/pets
