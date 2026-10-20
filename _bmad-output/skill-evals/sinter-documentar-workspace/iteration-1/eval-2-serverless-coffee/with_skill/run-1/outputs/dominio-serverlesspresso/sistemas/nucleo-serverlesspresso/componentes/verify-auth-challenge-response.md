---
id: cmp-nucleo-verify-auth-challenge
kind: component
subject: component:nucleo-serverlesspresso:verify-auth-challenge-response
camada: 5
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: [res-user-pool-cognito]
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/cognito-triggers/verify-auth-challenge-response.js"
    version: 9d494a2
    extraction: extracted
---
# verify-auth-challenge-response
Confere se o código de 6 dígitos digitado pelo usuário bate com o gerado.

| Campo | Valor |
|---|---|
| Tipo | lambda (Cognito trigger `VerifyAuthChallengeResponse`) |
| Gatilho | Usuário submete o código recebido por SMS |
| Entrada | `event.request.{challengeAnswer, privateChallengeParameters.passCode}` |
| Saída | `event.response.answerCorrect` |
| Timeout / memória / concorrência | Não definido explicitamente |

## Dependências
- Nenhuma chamada externa

## Erros e retentativas
Comparação simples de string; sem rate limiting próprio (depende do limite de tentativas do `define-auth-challenge`).
