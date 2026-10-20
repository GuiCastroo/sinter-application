---
id: res-journey-cloudfront
kind: resource
subject: resource:cloudfront-distribution:JourneyCloudFront
camada: 6
status: proposed
realiza: [sys-order-journey-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "01-appCore/template.yaml#L160-L191"
    version: 9d494a2
    extraction: extracted
---
# CloudFront "JourneyCloudFront"
| Campo | Valor |
|---|---|
| Tipo | cluster/CDN |
| Tecnologia | Amazon CloudFront, origem S3 via Origin Access Identity, `DefaultTTL: 5` segundos |
| Ambientes | consolidado (01-appCore) |
| Definido em | `01-appCore/template.yaml` |

## Usado por
- order-journey-service (serve a página HTML final ao cliente)
