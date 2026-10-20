---
id: cmp-order-manager-state-machine
kind: component
subject: component:order-manager-service:order-manager-state-machine
camada: 5
status: proposed
realiza: [sys-order-manager-service]
realizado-por: [cmp-order-manager-sanitize-order, res-ddb-order-table]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/statemachine/om.asl.json"
    version: 9d494a2
    extraction: extracted
---
# order-manager-state-machine
Decide, pelo campo `action` recebido, se está tratando o envio do pedido pelo cliente, a reivindicação/liberação pelo barista, ou a conclusão/cancelamento — e em qualquer um dos últimos dois casos, acorda o `order-processing-service` com `SendTaskSuccess`.

| Campo | Valor |
|---|---|
| Tipo | job (Step Functions Standard Workflow) |
| Gatilho | `PUT /orders/{id}` via API Gateway → `states:StartExecution` **direto** (sem lambda); a rota é compartilhada entre cliente (monta pedido) e barista (make/unmake/complete/cancel), diferenciados pelo campo `action` no corpo |
| Entrada | `{action, eventId, body, orderId, baristaUserId}` (montado pelo VTL da API Gateway a partir do path, query string e corpo) |
| Saída | Nenhuma direta ao chamador (API Gateway não espera o resultado do SFN); efeitos são via DynamoDB e `events:putEvents`/`SendTaskSuccess` |
| Timeout / memória / concorrência | Sem timeout global definido no ASL |

## Dependências
- `serverlesspresso-order-table` — leitura/escrita do estado do pedido
- `ConfigTable` — leitura do cardápio (`get menu`)
- Lambda `sanitize-order` — valida a bebida/modificadores
- EventBridge `Serverlesspresso` — publica os 3 eventos `OrderManager.*`
- `order-processing-service` — `states:SendTaskSuccess` (retoma a execução do cliente e depois a do barista)

## Erros e retentativas
- Pedido fora do cardápio: termina em `Succeed` sem propagar erro nem notificar ninguém (ver `RELATORIO.md`)
- Chamada à lambda `sanitize-order`: retry de 6 tentativas, backoff x2, 2 s inicial, para `Lambda.ServiceException`/`AWSLambdaException`/`SdkClientException`
