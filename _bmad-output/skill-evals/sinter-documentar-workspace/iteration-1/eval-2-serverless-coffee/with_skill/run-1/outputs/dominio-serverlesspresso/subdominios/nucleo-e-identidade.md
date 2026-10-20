---
id: sub-nucleo-e-identidade
kind: subdomain
subject: subdomain:nucleo-e-identidade
camada: 3
status: proposed
realiza: [dom-serverlesspresso]
realizado-por: [sys-nucleo-serverlesspresso]
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/template.yaml"
    version: 9d494a2
    extraction: extracted
---
# Subdomínio Núcleo e identidade
Recursos fundacionais que todos os outros subdomínios usam: o barramento de eventos, a autenticação sem senha do cliente (Cognito com desafio customizado via SMS) e o endpoint do AWS IoT Core usado para tempo real.

## Sistemas
| Sistema | Papel |
|---|---|
| nucleo-serverlesspresso | Bus de eventos `Serverlesspresso`, User Pool/Identity Pool do Cognito, fluxo de autenticação customizado, endpoint IoT |

## Fluxos executados aqui
Não orquestra um fluxo de negócio por si só; é infraestrutura compartilhada consumida por todos os fluxos do domínio (autenticação do cliente/barista, transporte de todos os eventos).
