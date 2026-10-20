---
id: sys-metrics-service
kind: system
subject: system:metrics-service
camada: 4
status: proposed
realiza: [sub-pedido]
realizado-por: [cmp-metrics-validator-new-order, cmp-metrics-order-manager-cancelled, cmp-metrics-order-processor-timeout, cmp-metrics-order-manager-waiting-completion]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/7-metrics-service/template.yaml"
    version: 9d494a2
    extraction: extracted
---
# metrics-service
Publica métricas customizadas no CloudWatch a partir de 4 eventos do domínio, para observar o funcionamento do balcão (quantos pedidos, quantos cancelados, quantos com timeout).

| Campo | Valor |
|---|---|
| Subdomínio | Pedido |
| Dono | Não identificado |
| Stack | Node.js 14.x (Lambda) |
| Repositório | `backends/7-metrics-service/` — **stack próprio, standalone, não referenciado por `01-appCore/template.yaml`** |
| Criticidade | Baixa — puramente observabilidade; sua ausência não afeta o pedido |

## Contêineres
```mermaid
flowchart LR
  BUS[[EventBridge Serverlesspresso]]
  subgraph metrics-service
    L1[validator-new-order-metric]
    L2[order-manager-order-cancelled-metric]
    L3[order-processor-order-timeout-metric]
    L4[order-manager-waiting-completion-metric]
  end
  BUS -->|Validator.NewOrder| L1
  BUS -->|OrderManager.OrderCancelled| L2
  BUS -->|OrderProcessor.OrderTimeOut| L3
  BUS -->|OrderManager.WaitingCompletion| L4
  L1 --> CW[(CloudWatch Metrics)]
  L2 --> CW
  L3 --> CW
  L4 --> CW
```

## Expõe
Nenhum contrato; só grava métricas no CloudWatch (`cloudwatch:PutMetricData` via `CloudWatchPutMetricPolicy`).

## Consome
| Sistema | Contrato | Tipo |
|---|---|---|
| validator-service | `Validator.NewOrder` | Evento |
| order-manager-service | `OrderManager.OrderCancelled`* | Evento |
| order-processing-service | `OrderProcessor.OrderTimeOut` | Evento |
| order-manager-service | `OrderManager.WaitingCompletion` | Evento |

\* O padrão real emitido pelo order-manager-state-machine é `OrderManager.Order{eventId}-CANCELLED` (com o `eventId` no meio do nome) — o prefixo `OrderManager.OrderCancelled` desta regra **não bate exatamente** com o que é publicado; ver `RELATORIO.md`.

## Dados
Nenhum banco próprio.

## Estados
N/A.

## Qualidade
- Timeout: 3 s em todas as funções
- **Este stack não é implantado pelo caminho documentado no README raiz** (que só manda subir `00-baseCore` e `01-appCore`) — ver `infraestrutura/ambientes/modulos-standalone-backends.md`
