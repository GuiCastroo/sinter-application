---
id: sys-publisher-service
kind: system
subject: system:publisher-service
camada: 4
status: proposed
realiza: [sub-pedido]
realizado-por: [cmp-publisher-admin, cmp-publisher-user, cmp-publisher-config, res-iot-core-realtime]
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L211-L312"
    version: 9d494a2
    extraction: extracted
---
# publisher-service
Ponte entre o EventBridge e o AWS IoT Core: republica os eventos de negócio como mensagens MQTT em tópicos que os três apps (cliente, barista, admin) assinam para atualização em tempo real.

| Campo | Valor |
|---|---|
| Subdomínio | Pedido |
| Dono | Não identificado |
| Stack | Node.js 14.x (Lambda) |
| Repositório | `backends/6-publisher-service/`; recursos em `01-appCore/template.yaml` |
| Criticidade | Média — afeta só a experiência em tempo real; o estado real do pedido já está gravado antes desta lambda rodar |

## Contêineres
```mermaid
flowchart LR
  BUS[[EventBridge Serverlesspresso]]
  subgraph publisher-service
    L1[publisher-admin]
    L2[publisher-user]
    L3[publisher-config]
  end
  BUS -->|OrderManager.*, OrderProcessor.*,<br/>Validator.*, ConfigService.*| L1
  BUS -->|OrderManager.*, OrderProcessor.*| L2
  BUS -->|ConfigService.*| L3
  L1 --> IOT[[AWS IoT Core]]
  L2 --> IOT
  L3 --> IOT
```

## Expõe
Nenhum contrato de API; publica em tópicos MQTT (não modelados como "contrato" formal por não terem schema declarado):
- `serverlesspresso-admin-{eventId}` (publisher-admin)
- `serverlesspresso-user-{userId}` (publisher-user)
- `serverlesspresso-config-{eventId}` (publisher-config)

## Consome
| Sistema | Contrato | Tipo |
|---|---|---|
| validator-service | `Validator.*` | Evento |
| order-processing-service | `OrderProcessor.*` | Evento |
| order-manager-service | `OrderManager.*` | Evento |
| config-service | `ConfigService.*` | Evento |

## Dados
Sem banco próprio; é um encaminhador stateless.

## Estados
N/A.

## Qualidade
- Timeout: 3 s em todas as 3 funções
- `publisher-admin` escuta 4 prefixos de evento numa única regra; `publisher-user` escuta 2 prefixos em duas regras separadas; `publisher-config` escuta 1 prefixo — assimetria não documentada, ver `RELATORIO.md`
