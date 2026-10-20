---
id: res-event-bus-serverlesspresso
kind: resource
subject: resource:eventbridge-bus:Serverlesspresso
camada: 6
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/template.yaml#L15-L18"
    version: 9d494a2
    extraction: extracted
---
# EventBridge bus "Serverlesspresso"
| Campo | Valor |
|---|---|
| Tipo | tópico (barramento de eventos) |
| Tecnologia | Amazon EventBridge (custom event bus) |
| Ambientes | core (00-baseCore); recriado também nos templates standalone de `extensions/EventPlayer` (mesmo nome — risco de colisão, ver RELATORIO.md) |
| Definido em | `00-baseCore/template.yaml` |

## Usado por
- Todos os sistemas do domínio publicam e/ou consomem eventos neste bus (`source: awsserverlessda.serverlesspresso`)
- Uma regra (`LogsRule`) encaminha todos os eventos do source para um CloudWatch Log Group, para depuração
