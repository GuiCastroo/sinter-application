---
id: env-consolidado-01-appcore
kind: environment
subject: environment:consolidado-01-appcore
camada: 6
status: proposed
realiza: [sys-config-service, sys-validator-service, sys-order-processing-service, sys-order-manager-service, sys-publisher-service, sys-order-journey-service, sys-counting-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "README.md; 01-appCore/template.yaml"
    version: 9d494a2
    extraction: extracted
---
# Ambiente "consolidado" (pilha 01-appCore)
Segunda e última pilha do caminho de implantação documentado no README raiz ("Install microservices"). Reúne, em um único `template.yaml`, os recursos de **config-service, validator-service, order-processing-service, order-manager-service, publisher-service, order-journey-service** e a tabela de contagem — todos com `CodeUri` apontando de volta para `../backends/<n>-*/`. É este o ambiente que efetivamente implementa o [fluxo de pedido de café](../../fluxos/pedido-de-cafe.sequencia.md) segundo o caminho de instalação oficial.

## Implantação
```mermaid
flowchart TB
  subgraph appcore["Pilha serverlesspresso (01-appCore), região us-east-1"]
    CFG[config-service]
    VAL[validator-service]
    OPS[order-processing-service]
    OMS[order-manager-service]
    PUB[publisher-service]
    OJ[order-journey-service]
  end
  CORE[00-baseCore] -->|SSM: bus ARN, user pool| appcore
  VAL -->|Validator.NewOrder| OPS
  OPS -->|WorkflowStarted, WaitingCompletion| OMS
  OMS -->|SendTaskSuccess| OPS
  OPS -->|orderFinished| OJ
  PUB -.assina todos os eventos.-> appcore
```
**Nota:** `metrics-service` (backends/7) **não** está incluído neste `template.yaml` — ver `modulos-standalone-backends.md`.
