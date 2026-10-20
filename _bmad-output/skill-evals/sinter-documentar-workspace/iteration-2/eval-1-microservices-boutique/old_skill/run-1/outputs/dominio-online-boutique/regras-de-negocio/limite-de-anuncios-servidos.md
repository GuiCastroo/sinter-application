---
id: rule-limite-de-anuncios-servidos
kind: rule
subject: rule:limite-de-anuncios-servidos
camada: 0
status: proposed
realiza: []
realizado-por: [sys-adservice]
provenance:
  - source: repo:microservices-demo
    locator: src/adservice/src/main/java/hipstershop/AdService.java#L46
    version: 38e7348
    extraction: extracted
---

# Limite de anúncios servidos

No máximo `MAX_ADS_TO_SERVE = 2` anúncios são devolvidos por chamada, tanto no caso de correspondência por categoria quanto no fallback aleatório. O `frontend` chama esse serviço com timeout de 100 ms e ignora silenciosamente qualquer falha/estouro de tempo. `[extracted]`

## Onde está implementada
- `src/adservice/src/main/java/hipstershop/AdService.java#L46`
- `src/frontend/rpc.go#L119-L124` (timeout de 100 ms)
