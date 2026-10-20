---
id: rule-limite-de-tokens-por-janela
kind: rule
subject: rule:limite-de-tokens-por-janela
camada: 0
status: proposed
realiza: [flow-pedido-de-cafe]
realizado-por: [cmp-validator-get-qr-code, cmp-validator-verify-qr-code]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/9-validator/code/getCode.js#L8; ConfigTable.drinksPerBarcode"
    version: 9d494a2
    extraction: extracted
---
# Limite de tokens por janela de tempo
A cada janela de 5 minutos, só um número limitado de bebidas pode ser resgatado por token (`ConfigTable.drinksPerBarcode`, valor configurável por evento). Isso limita quantos clientes podem escanear o QR code do balcão e iniciar um pedido dentro da mesma janela.

## Onde está implementada
- `backends/9-validator/code/getCode.js` (cria o bucket com `availableTokens = drinksPerBarcode`)
- `backends/9-validator/code/verifyCode.js` (decrementa a cada resgate válido)

## Conflito
Não identificado.
