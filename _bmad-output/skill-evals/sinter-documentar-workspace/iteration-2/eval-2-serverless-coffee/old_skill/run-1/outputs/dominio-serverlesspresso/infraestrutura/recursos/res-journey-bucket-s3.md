---
id: res-journey-bucket-s3
kind: resource
subject: resource:s3-bucket:serverlesspresso-order-journey
camada: 6
status: proposed
realiza: [sys-order-journey-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L60-L63"
    version: 9d494a2
    extraction: extracted
---
# S3 bucket "serverlesspresso-order-journey-{region}-{accountId}"
| Campo | Valor |
|---|---|
| Tipo | bucket |
| Tecnologia | Amazon S3, servido via CloudFront (não público diretamente) |
| Ambientes | consolidado (01-appCore) |
| Definido em | `01-appCore/template.yaml` |

## Usado por
- order-journey-service (`Save to S3` grava o HTML com `Acl: public-read`; `generate-html` referencia assets estáticos hospedados neste mesmo bucket, com nome de bucket **hardcoded** de uma implantação de exemplo — ver `RELATORIO.md`)
