---
id: cmp-nucleo-create-auth-challenge
kind: component
subject: component:nucleo-serverlesspresso:create-auth-challenge
camada: 5
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: [res-user-pool-cognito]
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/cognito-triggers/create-auth-challenge.js"
    version: 9d494a2
    extraction: extracted
---
# create-auth-challenge
Gera o código de 6 dígitos e envia por SMS via SNS.

| Campo | Valor |
|---|---|
| Tipo | lambda (Cognito trigger `CreateAuthChallenge`) |
| Gatilho | Início do desafio customizado (login por telefone) |
| Entrada | `event.request.userAttributes.phone_number`, `event.request.session` |
| Saída | `event.response.{publicChallengeParameters, privateChallengeParameters, challengeMetadata}`; efeito colateral: SMS via SNS |
| Timeout / memória / concorrência | Não definido explicitamente |

## Dependências
- Amazon SNS (`sns:*` — política ampla, ver `RELATORIO.md`) — envio do SMS com o código

## Erros e retentativas
Sem tratamento de erro explícito; falha do `sns.publish` propaga e falha o login.
