---
id: res-iot-core-realtime
kind: resource
subject: resource:iot-thing:serverlesspresso-realtime
camada: 6
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/template.yaml#L83-L114"
    version: 9d494a2
    extraction: extracted
---
# AWS IoT Core (realtime messaging)
| Campo | Valor |
|---|---|
| Tipo | cluster/serviço de mensageria (MQTT) |
| Tecnologia | AWS IoT Core (`AWS::IoT::Thing` + endpoint de dados descoberto via Custom Resource) |
| Ambientes | core (00-baseCore); endpoint publicado via SSM/Output para o `publisher-service` |
| Definido em | `00-baseCore/template.yaml` |

## Usado por
- publisher-service (as 3 lambdas publicam mensagens nos tópicos `serverlesspresso-admin-*`, `serverlesspresso-user-*`, `serverlesspresso-config-*`)
- Apps de front-end (assinam os tópicos via Identity Pool)
