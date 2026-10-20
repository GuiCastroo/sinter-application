---
id: cmp-publisher-config
kind: component
subject: component:publisher-service:publisher-config
camada: 5
status: proposed
realiza: [sys-publisher-service]
realizado-por: [res-iot-core-realtime]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/6-publisher-service/code/publishToIOTconfig.js; 01-appCore/template.yaml#L283-L312"
    version: 9d494a2
    extraction: extracted
---
# publisher-config
Republica `ConfigService.ConfigChanged` no tópico MQTT de configuração, avisando os apps quando o cardápio ou o status da loja mudam.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Regra EventBridge (`ConfigService.*`) |
| Entrada | Evento completo do EventBridge |
| Saída | Publica em `serverlesspresso-config-{eventId}` (o `eventId` é extraído de `event.detail.NewImage.PK.S`, ex.: `config-ABC` → `ABC`) |
| Timeout / memória / concorrência | 3 s / 128 MB |

## Dependências
- AWS IoT Core (`iot:Connect`, `iot:Publish`)

## Erros e retentativas
Mesma limitação: erro só logado, sem retry/DLQ.
