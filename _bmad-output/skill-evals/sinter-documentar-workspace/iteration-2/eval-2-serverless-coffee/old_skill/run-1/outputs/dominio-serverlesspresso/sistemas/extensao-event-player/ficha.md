---
id: sys-ext-event-player
kind: system
subject: system:extensao-event-player
camada: 4
status: proposed
realiza: [sub-extensoes]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "extensions/EventPlayer/template.yaml; extensions/EventPlayer/statemachines/player.asl.json"
    version: 9d494a2
    extraction: extracted
---
# extensao-event-player
Step Functions que reproduz uma sequência gravada de eventos reais do Serverlesspresso (um em cada ~5 s, ao longo de ~15 minutos), útil para testar extensões e dashboards sem precisar operar o balcão de verdade.

| Campo | Valor |
|---|---|
| Subdomínio | Extensões |
| Dono | Não identificado |
| Stack | Step Functions (AWS SAM) |
| Repositório | `extensions/EventPlayer/` |
| Criticidade | Nenhuma (ferramenta de teste/demo) |

## Contêineres
```mermaid
flowchart LR
  SFN[EventPlayer state machine] -->|events:PutEvents| BUS[[EventBridge Serverlesspresso]]
```

## Expõe
Nenhum contrato de negócio; entrada manual `{"eventId":"ABC"}` via console do Step Functions.

## Consome
Nenhuma.

## Dados / Estados
N/A.

## Qualidade
Implantado e removido de forma independente do core (regra da pasta `extensions/`, ver `subdominios/extensoes.md`); recria seu próprio `AWS::Events::EventBus` chamado `Serverlesspresso` no template — **pode colidir com o bus já criado por `00-baseCore`** se implantado na mesma conta/região sem ajuste (ver `RELATORIO.md`).
