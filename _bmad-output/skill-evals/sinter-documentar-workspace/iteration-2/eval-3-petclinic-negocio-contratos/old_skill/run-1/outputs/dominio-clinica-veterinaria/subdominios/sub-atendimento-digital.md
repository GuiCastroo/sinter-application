---
id: sub-atendimento-digital
kind: subdomain
subject: subdomain:atendimento-digital
camada: 3
status: proposed
realiza: [dom-clinica-veterinaria]
realizado-por: [sys-api-gateway, sys-genai-service]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/; spring-petclinic-genai-service/
    version: aefaf7f
    extraction: extracted
---

# Subdomínio Atendimento Digital
Concentra os canais pelos quais tutores e equipe da clínica interagem com o sistema: a tela web (via `api-gateway`) e o assistente virtual (via `genai-service`). Não guarda dado mestre — agrega e orquestra os subdomínios de Cadastro, Corpo Clínico e Consultas.

## Sistemas
| Sistema | Papel |
|---|---|
| [api-gateway](../sistemas/api-gateway/ficha.md) | porta de entrada única; serve o frontend e roteia/agrega chamadas |
| [genai-service](../sistemas/genai-service/ficha.md) | assistente virtual com IA generativa, com ações sobre owners/pets/vets |

## Fluxos executados aqui
- [Consulta de histórico do tutor](../fluxos/flow-consulta-historico-tutor.sequencia.md) — o passo de agregação/orquestração acontece aqui
- [Atendimento via assistente virtual](../fluxos/flow-atendimento-assistente-virtual.sequencia.md) — executado inteiramente dentro deste subdomínio (com chamadas de saída para Cadastro e Corpo Clínico)
