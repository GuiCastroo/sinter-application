---
id: dec-001-integracoes-diretas-sem-lambda-glue
kind: decision
subject: decision:integracoes-diretas-sem-lambda-glue
camada: 0
status: proposed
realiza: []
realizado-por: [sys-order-manager-service, sys-config-service, sys-order-processing-service, sys-order-journey-service]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/RestAPIs/api.yaml; backends/2-config-service/RestAPIs/api.yaml; backends/4-order-processing/statemachine/op.asl.json; backends/8-order-journey/statemachine/StepFunction.asl.json"
    version: 9d494a2
    extraction: inferred
---
# ADR-001 Preferir integrações diretas de serviço a "lambdas de cola" (proposto, sem documento original)
Status: proposta (inferida do código; **não existe ADR no repositório** — este documento é uma reconstrução, marcado `inferred`) — Data: desconhecida

## Contexto
Várias rotas de API (`GET/PUT /orders`, `GET/PUT /config`, `PUT /store`) e vários passos das duas state machines (leitura/escrita no DynamoDB, `PutEvents`, `SendTaskSuccess`) são implementados como integrações diretas do API Gateway ou do Step Functions com o serviço AWS de destino, via VTL ou `Resource: arn:aws:states:::<serviço>:<ação>`, sem uma função Lambda no meio.

## Opções consideradas
- Lambda entre a API/o SFN e o serviço AWS (padrão mais comum, mais fácil de testar/depurar)
- Integração direta (menos código, menos cold start, mas lógica de mapeamento fica em VTL/ASL, mais difícil de testar unitariamente)

## Decisão
O código mostra a opção por integração direta na maior parte dos casos "CRUD simples" (ver arquivos em `provenance`), reservando lambdas para lógica de negócio real (`sanitize-order`, `generate-html`, os 3 publishers).

## Consequências
- Menos lambdas para manter, potencialmente menor custo/latência
- Lógica de mapeamento de request/response fica em VTL (API Gateway) ou ASL (Step Functions), mais difícil de testar isoladamente e sem tipagem
- Erros de integração aparecem como erros genéricos do API Gateway, sem tratamento customizado (ver componentes `rest-api-orders`, `rest-api-config`)

**Esta é uma reconstrução do padrão observado, não uma decisão documentada — perguntar ao arquiteto se isso foi deliberado e se deve continuar sendo seguido.**
