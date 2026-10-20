---
id: dom-online-boutique-relacoes
kind: domain
subject: domain:online-boutique:relacoes
camada: 2
status: proposed
realiza: [dom-online-boutique]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: README.md#L1-L30
    version: 38e7348
    extraction: inferred
---

# Relações com outros domínios

O repositório documenta um único domínio autocontido (demo de referência); não há outro domínio de negócio (ex.: "Estoque", "Contabilidade", "Marketing") no mesmo repositório ou citado em documentação para relacionar. `[inferred — repositório é um monorepo de demonstração isolado]`

As únicas fronteiras externas observadas são técnicas, não de domínio de negócio:

| Fronteira externa | Natureza | Sistema que a implementa |
|---|---|---|
| Envio de e-mail | Simulado (loga e retorna sucesso; não integra provedor real) | [emailservice](../sistemas/emailservice/ficha.md) |
| Cobrança de cartão | Simulado (valida formato/bandeira/validade e devolve um UUID como "transação") | [paymentservice](../sistemas/paymentservice/ficha.md) |
| Cotação de câmbio | Dados estáticos embutidos (`currency_conversion.json`, rotulado como vindo do Banco Central Europeu) | [currencyservice](../sistemas/currencyservice/ficha.md) |
| Frete | Simulado (cálculo determinístico por quantidade de itens; não integra transportadora) | [shippingservice](../sistemas/shippingservice/ficha.md) |
| Assistente de compras (IA) | Real, se habilitado: usa Gemini (Google Generative AI) e AlloyDB como vector store | [shoppingassistantservice](../sistemas/shoppingassistantservice/ficha.md) |

## Pergunta em aberto

Se este domínio for integrado a outros domínios de negócio da empresa (ex.: um domínio real de Pagamentos ou de Logística), qual será o mecanismo de integração — chamada síncrona adicional ou introdução de um barramento de eventos? Hoje nada no código sustenta essa integração. `[pergunta para arquiteto]`
