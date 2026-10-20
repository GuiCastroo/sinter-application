---
id: cmp-publisher-admin
kind: component
subject: component:publisher-service:publisher-admin
camada: 5
status: proposed
realiza: [sys-publisher-service]
realizado-por: [res-iot-core-realtime]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/6-publisher-service/code/publishToIOT.js; 01-appCore/template.yaml#L211-L243"
    version: 9d494a2
    extraction: extracted
---
# publisher-admin
Republica eventos de `OrderManager.*`, `OrderProcessor.*`, `Validator.*` e `ConfigService.*` no tópico MQTT do painel administrativo.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Regra EventBridge com 4 prefixos de `detail-type` |
| Entrada | Evento completo do EventBridge |
| Saída | Publica em `serverlesspresso-admin-{eventId}` via `iotdata.publish` (QoS 1) |
| Timeout / memória / concorrência | 3 s / 128 MB |

## Dependências
- AWS IoT Core (`iot:Connect`, `iot:Publish`) — endpoint vindo de `IoTRealtimeParameter` (SSM)

## Erros e retentativas
Falhas de publish são apenas logadas (`console.error`), sem retry nem DLQ — mensagem perdida silenciosamente em caso de erro do IoT Core.
