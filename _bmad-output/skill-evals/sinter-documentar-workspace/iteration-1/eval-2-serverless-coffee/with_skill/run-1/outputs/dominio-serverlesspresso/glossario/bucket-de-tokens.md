---
id: term-bucket-de-tokens
kind: term
subject: term:bucket-de-tokens
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/9-validator/code/getCode.js"
    version: 9d494a2
    extraction: extracted
---
# Bucket (de tokens)
Registro em `serverlesspresso-validator` que representa uma janela de tempo fixa (5 minutos, `TIME_INTERVAL`) durante a qual um único código (`last_code`) é válido e um número limitado de bebidas (`availableTokens`, vindo do cardápio) pode ser resgatado. "Bucket" aqui não é um S3 bucket — é um termo de "time bucketing"/janela deslizante.

Não confundir com: `JourneyBucket` (esse sim um bucket S3, do `order-journey-service`).
