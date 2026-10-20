---
id: sys-currencyservice
kind: system
subject: system:currencyservice
camada: 4
status: proposed
realiza: [sub-checkout-e-pagamento, sub-catalogo-e-descoberta]
realizado-por: [cmp-currencyservice-grpc]
provenance:
  - source: repo:microservices-demo
    locator: src/currencyservice/server.js#L106-L172
    version: 38e7348
    extraction: extracted
---

# currencyservice

Converte um valor monetário de uma moeda para outra. É o serviço de maior QPS do domínio segundo o README (chamado a cada preço exibido ou calculado). `[extracted, README.md#L30]`

| Campo | Valor |
|---|---|
| Subdomínio | Checkout e Pagamento (usado também por Catálogo/Frontend) |
| Dono | Não identificado `[a confirmar]` |
| Stack | Node.js |
| Repositório | `src/currencyservice/` |
| Criticidade | Alta — quase toda tela e o checkout dependem dele `[inferred]` |

## Contêineres

```mermaid
flowchart LR
  API[CurrencyService gRPC :7000] --> JSON[[data/currency_conversion.json]]
```
`[extracted, src/currencyservice/server.js#L106-L115]`

## Expõe

| Contrato | Tipo | Detalhe |
|---|---|---|
| `CurrencyService.GetSupportedCurrencies` | gRPC | Lista códigos ISO 4217 suportados |
| `CurrencyService.Convert` | gRPC | Converte `Money` de uma moeda para outra usando EUR como moeda-pivô |

`[extracted, protos/demo.proto#L140-L173; src/currencyservice/server.js#L138-L172]`

## Consome
- Nenhum outro sistema; dados de câmbio são estáticos, embutidos no arquivo `data/currency_conversion.json` — rotulado no README do projeto como originado do Banco Central Europeu, mas **não há chamada em runtime a nenhuma API externa** — são taxas fixas do momento em que o arquivo foi gerado. `[extracted — nenhum client HTTP encontrado em server.js; README.md#L14 afirma "Uses real values fetched from European Central Bank", o que é uma imprecisão/desatualização do README frente ao código atual — ver conflito registrado]`

## Dados
Tabela estática moeda → fator de conversão relativo ao EUR (arquivo JSON, não um banco).

## Qualidade
- Conversão feita em memória, sem I/O de rede — resposta rápida e sem dependência externa em runtime.
