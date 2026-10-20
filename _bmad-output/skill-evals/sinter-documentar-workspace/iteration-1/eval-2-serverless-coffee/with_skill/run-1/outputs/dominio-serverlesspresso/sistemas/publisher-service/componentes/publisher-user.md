---
id: cmp-publisher-user
kind: component
subject: component:publisher-service:publisher-user
camada: 5
status: proposed
realiza: [sys-publisher-service]
realizado-por: [res-iot-core-realtime]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/6-publisher-service/code/publishToIOTuserTopic.js; 01-appCore/template.yaml#L244-L282"
    version: 9d494a2
    extraction: extracted
---
# publisher-user
Republica eventos de `OrderManager.*` e `OrderProcessor.*` no tópico MQTT pessoal do cliente dono do pedido.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Duas regras EventBridge (`OrderManager.*`, `OrderProcessor.*`) |
| Entrada | Evento completo do EventBridge |
| Saída | Publica em `serverlesspresso-user-{userId}` via `iotdata.publish` (QoS 1) |
| Timeout / memória / concorrência | 3 s / 128 MB |

## Dependências
- AWS IoT Core (`iot:Connect`, `iot:Publish`)

## Erros e retentativas
Mesma limitação do `publisher-admin`: erro só logado, sem retry/DLQ.
