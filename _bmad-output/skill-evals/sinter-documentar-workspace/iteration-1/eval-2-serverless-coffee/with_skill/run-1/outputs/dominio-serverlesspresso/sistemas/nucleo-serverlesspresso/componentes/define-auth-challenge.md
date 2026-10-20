---
id: cmp-nucleo-define-auth-challenge
kind: component
subject: component:nucleo-serverlesspresso:define-auth-challenge
camada: 5
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: [res-user-pool-cognito]
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/cognito-triggers/define-auth-challenge.js"
    version: 9d494a2
    extraction: extracted
---
# define-auth-challenge
Decide o próximo passo do login sem senha: emitir o desafio customizado, aceitar, ou falhar após tentativas demais.

| Campo | Valor |
|---|---|
| Tipo | lambda (Cognito trigger `DefineAuthChallenge`) |
| Gatilho | Cada etapa do fluxo de login customizado |
| Entrada | `event.request.session` (histórico de desafios da sessão) |
| Saída | `event.response.{issueTokens, failAuthentication, challengeName}` |
| Timeout / memória / concorrência | Não definido explicitamente |

## Dependências
- Nenhuma chamada externa

## Erros e retentativas
Falha a autenticação após 3 respostas erradas (`session.length >= 4` com o último resultado falso); contorna um bug conhecido do SDK iOS da AWS que envia `SRP_A` no primeiro desafio customizado (comentário no próprio código).
