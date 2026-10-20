---
id: flow-pedido-de-cafe
kind: flow
subject: flow:pedido-de-cafe
camada: 1
status: proposed
realiza: [cap-vender-cafe-sob-demanda]
realizado-por: [flow-pedido-de-cafe-sequencia]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/4-order-processing/statemachine/op.asl.json; backends/5-order-manager/statemachine/om.asl.json"
    version: 9d494a2
    extraction: inferred
---
# Pedido de café
Do momento em que o cliente escaneia o QR code no balcão até o barista entregar (ou cancelar) a bebida, mantendo o cliente informado em tempo real.

## Atores
- **Cliente** — pede a bebida pelo celular
- **Loja** (sistema automatizado: capacidade, cardápio, fila) — decide se aceita o pedido
- **Barista** — prepara e conclui ou cancela o pedido

## Etapas
| # | Etapa | Ator | Decisão ou resultado | Técnica |
|---|---|---|---|---|
| 1 | Cliente pede um código de acesso ao abrir o app | Cliente | — | [passo 1](./pedido-de-cafe.sequencia.md#passo-1) |
| 2 | Cliente escaneia o QR code físico do balcão e confirma | Cliente | Token válido? Ainda há tokens disponíveis na janela de tempo? | [passo 2](./pedido-de-cafe.sequencia.md#passo-2) |
| 3 | Loja verifica se está aberta e se há vaga na fila | Loja | Loja aberta? Fila com capacidade livre? | [passo 3](./pedido-de-cafe.sequencia.md#passo-3) |
| 4 | Cliente monta e envia o pedido de bebida | Cliente | O pedido está no cardápio vigente? | [passo 4](./pedido-de-cafe.sequencia.md#passo-4) |
| 5 | Pedido recebe um número e entra na fila do barista | Loja | — | [passo 5](./pedido-de-cafe.sequencia.md#passo-5) |
| 6 | Barista reivindica, prepara e conclui (ou cancela) o pedido | Barista | Concluído ou cancelado? | [passo 6](./pedido-de-cafe.sequencia.md#passo-6) |
| 7 | Cliente acompanha o status em tempo real e vê a jornada do pedido ao final | Cliente / Loja | — | [passo 7](./pedido-de-cafe.sequencia.md#passo-7) |

## Diagrama
```mermaid
flowchart LR
  subgraph Cliente
    A[Pede código de acesso] --> B[Escaneia QR code do balcão]
  end
  subgraph Loja
    B --> C{Loja aberta e<br/>com capacidade?}
    C -- não --> X[Pedido recusado]
    C -- sim --> D[Aguarda o cliente montar o pedido]
  end
  subgraph Cliente2[Cliente]
    D --> E[Monta e envia o pedido]
  end
  subgraph Loja2[Loja]
    E --> F{Pedido está<br/>no cardápio?}
    F -- não --> Y[Pedido rejeitado]
    F -- sim --> G[Pedido numerado, entra na fila]
  end
  subgraph Barista
    G --> H[Reivindica o pedido]
    H --> I{Concluído ou<br/>cancelado?}
  end
  I -- concluído --> J[Cliente recebe a bebida e a jornada do pedido]
  I -- cancelado --> K[Cliente é avisado do cancelamento]
```

## Indicadores
- Tempo médio entre pedido e entrega (a confirmar com o PM)
- Taxa de cancelamento de pedidos (a confirmar com o PM)
- Pedidos por barista / por janela de tempo (a confirmar com o PM)
- Utilização da capacidade máxima da fila (a confirmar com o PM)

## Regras que governam
- [Limite de tokens por janela de tempo](../regras-de-negocio/limite-de-tokens-por-janela.md)
- [Capacidade máxima de pedidos simultâneos](../regras-de-negocio/capacidade-maxima-concorrente.md)
- [Timeout do cliente para enviar o pedido](../regras-de-negocio/timeout-cliente-envio-pedido.md)
- [Timeout do barista para concluir o pedido](../regras-de-negocio/timeout-barista-preparo.md)
