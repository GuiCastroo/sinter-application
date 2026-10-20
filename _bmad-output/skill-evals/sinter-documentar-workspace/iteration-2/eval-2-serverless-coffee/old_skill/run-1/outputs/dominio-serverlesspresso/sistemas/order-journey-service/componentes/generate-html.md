---
id: cmp-order-journey-generate-html
kind: component
subject: component:order-journey-service:generate-html
camada: 5
status: proposed
realiza: [sys-order-journey-service]
realizado-por: [res-journey-bucket-s3]
provenance:
  - source: repo:serverless-coffee
    locator: "backends/8-order-journey/functions/GenerateHtml/app.js"
    version: 9d494a2
    extraction: extracted
---
# generate-html
Monta o HTML da linha do tempo do pedido (imagens, mensagens amigáveis de cada evento, botão de compartilhar no Twitter/X).

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Invocação direta (`lambda:invoke`) pela `order-journey-state-machine`, só quando o pedido termina |
| Entrada | `{dbResults, EndTime, orderId}` (resultado da Query na tabela de jornada) |
| Saída | `{html, fileName}` — devolvido ao SFN, que grava em S3 |
| Timeout / memória / concorrência | 3 s / 128 MB |

## Dependências
- Nenhuma chamada externa dentro da própria função (o `S3.putObject` está comentado no código-fonte — quem grava é o state seguinte do SFN, `Save to S3`, direto)

## Erros e retentativas
Sem `try/catch`; se `dbResults.Items` vier vazio, `dbResults.Items[0].PK.S` lança e a função falha (coberta pelo retry do SFN chamador).
