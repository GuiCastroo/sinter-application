---
id: sub-configuracao-da-loja
kind: subdomain
subject: subdomain:configuracao-da-loja
camada: 3
status: proposed
realiza: [dom-serverlesspresso]
realizado-por: [sys-config-service]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/2-config-service"
    version: 9d494a2
    extraction: extracted
---
# Subdomínio Configuração da loja
Mantém o cardápio do evento, o estado "aberto/fechado" da loja e o limite de bebidas por token, e avisa o resto do sistema quando essa configuração muda.

## Sistemas
| Sistema | Papel |
|---|---|
| config-service | Fonte de verdade do cardápio e do estado da loja; publica `ConfigService.ConfigChanged` via DynamoDB Streams |

## Fluxos executados aqui
Não há um fluxo de ponta a ponta próprio; este subdomínio é consultado (leitura direta de `ConfigTable`) pelo `order-processing-service` (loja aberta?) e pelo `order-manager-service` (cardápio) durante o [pedido de café](../fluxos/pedido-de-cafe.sequencia.md).
