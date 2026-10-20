---
id: cmp-order-manager-rest-api-orders
kind: component
subject: component:order-manager-service:rest-api-orders
camada: 5
status: proposed
realiza: [sys-order-manager-service]
realizado-por: [res-ddb-order-table, cmp-order-manager-state-machine, res-rest-api-order-manager]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/RestAPIs/api.yaml"
    version: 9d494a2
    extraction: extracted
---
# rest-api-orders
As 3 rotas da API de pedidos usadas pelos apps de cliente e barista. **Nenhuma delas passa por uma lambda** — são integrações diretas do API Gateway (`x-amazon-apigateway-integration type: aws`) com DynamoDB e Step Functions, usando Velocity Template Language (VTL) para montar a requisição.

| Campo | Valor |
|---|---|
| Tipo | endpoint (API Gateway REST, integração direta, sem lambda) |
| Gatilho | `GET /orders`, `GET /orders/{id}`, `PUT /orders/{id}` — autenticação Cognito User Pools (`ServerlespressoAuth`) |
| Entrada | `GET /orders`: query `state`, `eventId`, `maxItems` (monta uma Query no GSI `GSI-status`). `GET /orders/{id}`: path `id` (GetItem por `PK=orders`/`SK=id`). `PUT /orders/{id}`: path `id`, query `action`/`eventId`, corpo do pedido, `sub` do JWT como `baristaUserId` — inicia a `order-manager-state-machine` |
| Saída | `GET /orders`: lista de pedidos do estado pedido. `GET /orders/{id}`: `{orderId, drinkOrder, orderState, TS}`. `PUT /orders/{id}`: `200` vazio (execução do SFN é assíncrona) |
| Timeout / memória / concorrência | N/A (sem lambda; limites padrão do API Gateway) |

## Dependências
- `serverlesspresso-order-table` — via role `RESTApiRole` (`dynamodb:GetItem`, `dynamodb:Query`)
- `order-manager-state-machine` — via `states:StartExecution` na mesma role

## Erros e retentativas
Sem lambda, então sem retry de aplicação; erros de VTL ou de permissão aparecem como erro genérico do API Gateway (5xx) sem tratamento customizado observado no `api.yaml`.
