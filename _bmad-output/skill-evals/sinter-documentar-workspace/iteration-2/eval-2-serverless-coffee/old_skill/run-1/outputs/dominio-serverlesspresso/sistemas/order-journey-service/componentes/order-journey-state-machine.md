---
id: cmp-order-journey-state-machine
kind: component
subject: component:order-journey-service:order-journey-state-machine
camada: 5
status: proposed
realiza: [sys-order-journey-service]
realizado-por: [res-ddb-order-journey-events-table, cmp-order-journey-generate-html]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/8-order-journey/statemachine/StepFunction.asl.json"
    version: 9d494a2
    extraction: extracted
---
# order-journey-state-machine
Grava cada evento do domínio como uma linha na tabela de jornada; ao ver `OrderProcessor.orderFinished`, busca todo o histórico do pedido e manda montar a página HTML.

| Campo | Valor |
|---|---|
| Tipo | job (Step Functions Standard Workflow) |
| Gatilho | Regra EventBridge que casa **qualquer** evento com `source: awsserverlessda.serverlesspresso` (sem filtro de `detail-type`) |
| Entrada | Evento completo do EventBridge |
| Saída | `PutItem` em `OrderJourneyEventsTable`; ou, se `orderFinished`, arquivo HTML em S3 |
| Timeout / memória / concorrência | Sem timeout global |

## Dependências
- `OrderJourneyEventsTable` — `PutItem`/`Query` direto (sem lambda, via `${DDBPutItem}`/`${DDBQuery}`)
- Lambda `generate-html`
- `JourneyBucket` (S3) — `PutObject` direto (`${S3BucketPut}`), com `Acl: public-read`

## Erros e retentativas
- Chamada à lambda `Generate HTML`: retry de 6 tentativas, backoff x2, 2 s inicial
- Eventos sem `$.detail.userId` terminam cedo no state `Not a user event`, sem gravar nada
