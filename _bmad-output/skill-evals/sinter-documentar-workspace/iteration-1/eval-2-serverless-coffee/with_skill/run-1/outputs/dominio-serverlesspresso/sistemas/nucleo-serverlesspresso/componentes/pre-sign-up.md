---
id: cmp-nucleo-pre-sign-up
kind: component
subject: component:nucleo-serverlesspresso:pre-sign-up
camada: 5
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: [res-user-pool-cognito]
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/cognito-triggers/pre-sign-up.js"
    version: 9d494a2
    extraction: extracted
---
# pre-sign-up
Confirma automaticamente o cadastro do cliente por telefone, sem exigir verificação manual.

| Campo | Valor |
|---|---|
| Tipo | lambda (Cognito trigger `PreSignUp`) |
| Gatilho | Tentativa de cadastro no User Pool |
| Entrada | Evento padrão do trigger `PreSignUp` do Cognito |
| Saída | `autoConfirmUser: true`, `autoVerifyPhone: true` |
| Timeout / memória / concorrência | Não definido explicitamente no template (padrão SAM) |

## Dependências
- Cognito User Pool (invocado por ele; sem chamada de saída)

## Erros e retentativas
Sem tratamento de erro; qualquer exceção falha o cadastro (comportamento padrão do Cognito).
