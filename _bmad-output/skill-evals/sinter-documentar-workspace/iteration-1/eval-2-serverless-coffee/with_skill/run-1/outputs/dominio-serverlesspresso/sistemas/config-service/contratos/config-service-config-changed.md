---
id: ctr-config-service-config-changed
kind: contract
subject: contract:event:ConfigService.ConfigChanged
camada: 4
status: proposed
realiza: [sys-config-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/2-config-service/code/configChanged.js"
    version: 9d494a2
    extraction: extracted
---
# ConfigService.ConfigChanged
| Campo | Valor |
|---|---|
| Tipo | evento (EventBridge) |
| Produtor | config-service (`config-changed`) |
| Consumidores | publisher-service (tópico IoT `serverlesspresso-config`), order-journey-service |
| Especificação | Sem AsyncAPI formal |

## Exemplo
```json
{
  "NewImage": {
    "PK": { "S": "config-ABC" },
    "storeOpen": { "BOOL": true }
  }
}
```
