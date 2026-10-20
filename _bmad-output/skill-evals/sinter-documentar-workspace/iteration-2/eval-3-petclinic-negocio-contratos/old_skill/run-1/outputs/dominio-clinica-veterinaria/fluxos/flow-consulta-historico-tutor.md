---
id: flow-consulta-historico-tutor
kind: flow
subject: flow:consulta-historico-tutor
camada: 1
status: proposed
realiza: [cap-atendimento-omnicanal, cap-cadastro-clientes-pets]
realizado-por: [sys-api-gateway, sys-customers-service, sys-visits-service]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java
    version: aefaf7f
    extraction: inferred
---

# Consulta de histórico do tutor
Permitir que a clínica veja, numa única tela, o tutor, seus pets e o histórico de visitas de cada pet — sem precisar navegar por telas separadas para cada informação.

## Atores
- **Tutor / equipe clínica** — consulta os dados de um tutor específico
- **Sistema (clínica veterinária)** — agrega os dados vindos de Cadastro e Consultas

## Etapas
| # | Etapa | Ator | Decisão ou resultado | Técnica |
|---|---|---|---|---|
| 1 | Usuário seleciona um tutor | Tutor/equipe | dispara a consulta agregada | [passo 1](./flow-consulta-historico-tutor.sequencia.md#passo-1) |
| 2 | Sistema busca o tutor e seus pets | Sistema | dados do tutor e lista de pets | [passo 1](./flow-consulta-historico-tutor.sequencia.md#passo-1) |
| 3 | Sistema busca as visitas de todos os pets do tutor | Sistema | histórico de visitas por pet, **ou lista vazia se a busca falhar** | [passo 2](./flow-consulta-historico-tutor.sequencia.md#passo-2) |
| 4 | Sistema devolve tutor + pets + visitas numa única resposta | Sistema | tela exibida ao usuário | [passo 2](./flow-consulta-historico-tutor.sequencia.md#passo-2) |

## Diagrama
```mermaid
flowchart LR
  subgraph Usuário
    A[Seleciona um tutor] --> B[Visualiza tutor, pets e visitas]
  end
  subgraph Clínica
    A --> C[Busca tutor e pets]
    C --> D{Busca de visitas OK?}
    D -- sim --> E[Anexa visitas aos pets]
    D -- não/timeout --> F[Anexa lista de visitas vazia]
    E --> B
    F --> B
  end
```

## Indicadores
- Latência da consulta agregada, taxa de degradação (quantas vezes o histórico de visitas veio vazio por falha) — não encontrados no código; **a confirmar com o PM**.

## Regras que governam
- [Degradação graciosa quando o histórico de visitas falha](../regras-de-negocio/reg-degradacao-visitas.md)
