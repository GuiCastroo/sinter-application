---
id: rule-moedas-suportadas
kind: rule
subject: rule:moedas-suportadas
camada: 0
status: proposed
realiza: []
realizado-por: [cmp-frontend-handlers, sys-currencyservice]
provenance:
  - source: repo:microservices-demo
    locator: src/frontend/rpc.go#L30-L41
    version: 38e7348
    extraction: extracted
---

# Moedas suportadas para exibição

O `currencyservice` conhece um conjunto de códigos de moeda (arquivo `data/currency_conversion.json`), mas o `frontend` filtra essa lista por uma whitelist própria (`whitelistedCurrencies`) antes de oferecer ao cliente — ou seja, a moeda tem que estar presente nas duas listas para aparecer no seletor. `[extracted]`

## Onde está implementada
- `src/frontend/rpc.go#L30-L41` (filtro `whitelistedCurrencies`)
- `src/currencyservice/data/currency_conversion.json` (fonte dos códigos e taxas)

## Conflito
O `README.md` do repositório (raiz, tabela de arquitetura) descreve o `currencyservice` como usando "real values fetched from European Central Bank" (em tempo real). O código (`src/currencyservice/server.js#L106-L115`) carrega um arquivo JSON estático embutido na imagem, sem nenhuma chamada de rede em runtime. `conflito: true` — duas fontes dizem coisas diferentes:
- **Fonte A (README.md#L14, extracted):** conversão usa valores reais buscados do BCE.
- **Fonte B (src/currencyservice/server.js#L106-L172, extracted):** conversão é 100% local, a partir de um arquivo estático versionado no repositório; não há client HTTP no serviço.

Provável explicação: o arquivo é gerado/atualizado manualmente de tempos em tempos a partir do BCE, e o README descreve a *origem* dos dados, não o comportamento em runtime — mas isso não está confirmado. `[pergunta para o tech lead do currencyservice]`
