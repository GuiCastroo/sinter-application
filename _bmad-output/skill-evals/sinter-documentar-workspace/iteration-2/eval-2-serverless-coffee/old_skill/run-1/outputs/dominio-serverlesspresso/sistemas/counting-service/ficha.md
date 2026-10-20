---
id: sys-counting-service
kind: system
subject: system:counting-service
camada: 4
status: proposed
realiza: [sub-pedido]
realizado-por: [res-ddb-counting-table]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/1-counting-service/code/; 01-appCore/template.yaml#L196-L206; backends/4-order-processing/statemachine/op.asl.json#L114-L137"
    version: 9d494a2
    extraction: extracted
---
# counting-service
**Sistema parcialmente órfão.** A tabela `CountingTable` (`serverlesspresso-counting-table`) é real e usada — mas na pilha consolidada (`01-appCore`) quem incrementa o contador é um state (`Generate Order Number`) direto dentro do `order-processing-service`, não as lambdas deste diretório.

| Campo | Valor |
|---|---|
| Subdomínio | Pedido |
| Dono | Não identificado |
| Stack | Node.js (Lambda) — mas sem `template.yaml` próprio |
| Repositório | `backends/1-counting-service/code/` |
| Criticidade | Baixa como está hoje (código não implantado); a **função** que ele cumpre (gerar `orderNumber`) é crítica e está embutida no `order-processing-service` |

## Contêineres
```mermaid
flowchart LR
  subgraph counting-service["counting-service (código não referenciado por nenhum template.yaml)"]
    L1[get-order-id]
    L2[reset-order-id]
  end
  L1 -.não usado.-> CNT[(CountingTable)]
  L2 -.não usado.-> CNT
  OPS[order-processing-service] -->|UpdateItem direto, incrementa IDvalue| CNT
```

## Expõe
Nenhum contrato ativo.

## Consome
Nenhum.

## Dados
```mermaid
erDiagram
  COUNTER {
    string PK "orderID-eventId"
    number IDvalue
  }
```
Tabela `serverlesspresso-counting-table`, populada inicialmente por `01-appCore/initDB/initCountingState.JSON`.

## Estados
N/A.

## Qualidade
- Nenhum `template.yaml` em `backends/1-counting-service/` referencia `getOrderId.js`/`resetOrderId.js` como função Lambda — **achado a confirmar com o tech lead** (ver `RELATORIO.md`)
