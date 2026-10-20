---
id: sub-catalogo-e-descoberta
kind: subdomain
subject: subdomain:catalogo-e-descoberta
camada: 3
status: proposed
realiza: [dom-online-boutique, cap-descobrir-e-recomendar-produtos]
realizado-por: [sys-productcatalogservice, sys-recommendationservice, sys-adservice]
provenance:
  - source: repo:microservices-demo
    locator: src/productcatalogservice/server.go#L1-L60
    version: 38e7348
    extraction: extracted
---

# Subdomínio Catálogo e Descoberta

Responsável por manter e expor o catálogo de produtos e por ajudar o cliente a descobrir itens além do que ele já procurou (recomendações e anúncios). `[extracted a partir das responsabilidades de cada serviço]`

## Sistemas

| Sistema | Papel |
|---|---|
| [productcatalogservice](../sistemas/productcatalogservice/ficha.md) | Fonte de verdade dos produtos (catálogo estático em JSON), busca e detalhe |
| [recommendationservice](../sistemas/recommendationservice/ficha.md) | Sugere produtos a partir dos itens do carrinho |
| [adservice](../sistemas/adservice/ficha.md) | Anúncios de texto por categoria/contexto |

## Fluxos executados aqui

Não há fluxo macro dedicado; este subdomínio é consumido dentro de [Compra do cliente](../fluxos/compra-do-cliente.sequencia.md) (passos 2 e 4) e por qualquer página que liste produtos.

## Observação

Nenhum dos três sistemas escreve dados — todos são consultas. Não há cache dedicado documentado no código (o catálogo é lido do arquivo JSON a cada `ListProducts`, salvo cache em memória — ver [ficha do productcatalogservice](../sistemas/productcatalogservice/ficha.md)). `[extracted]`
