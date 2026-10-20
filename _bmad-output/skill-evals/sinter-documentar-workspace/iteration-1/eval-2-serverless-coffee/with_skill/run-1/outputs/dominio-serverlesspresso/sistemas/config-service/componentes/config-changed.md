---
id: cmp-config-changed
kind: component
subject: component:config-service:config-changed
camada: 5
status: proposed
realiza: [sys-config-service]
realizado-por: [res-ddb-config-table, res-event-bus-serverlesspresso]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/2-config-service/code/configChanged.js"
    version: 9d494a2
    extraction: extracted
---
# config-changed
Republica no EventBridge qualquer alteração gravada em `ConfigTable` (cardápio, loja aberta/fechada).

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | DynamoDB Streams de `ConfigTable` (`BatchSize: 1`, `StartingPosition: TRIM_HORIZON`) |
| Entrada | `event.Records[0].dynamodb.NewImage` |
| Saída | Publica `ConfigService.ConfigChanged` com a imagem nova do item |
| Timeout / memória / concorrência | 15 s / 128 MB |

## Dependências
- EventBridge `Serverlesspresso` — `events:PutEvents`

## Erros e retentativas
Sem `Retry`/DLQ próprios; falhas de stream seguem o comportamento padrão de retry do DynamoDB Streams + Lambda (retenção de 24h, sem bisect configurado).
