---
id: sys-adservice
kind: system
subject: system:adservice
camada: 4
status: proposed
realiza: [sub-catalogo-e-descoberta]
realizado-por: [cmp-adservice-grpc]
provenance:
  - source: repo:microservices-demo
    locator: src/adservice/src/main/java/hipstershop/AdService.java#L41-L135
    version: 38e7348
    extraction: extracted
---

# adservice

Devolve anúncios de texto associados a categorias de produto (contexto da página atual). `[extracted, README.md#L35]`

| Campo | Valor |
|---|---|
| Subdomínio | Catálogo e Descoberta |
| Dono | Não identificado `[a confirmar]` |
| Stack | Java |
| Repositório | `src/adservice/` |
| Criticidade | Baixa — frontend chama com timeout de 100 ms e ignora falha `[extracted, src/frontend/rpc.go#L119-L124]` |

## Expõe

| Contrato | Tipo | Detalhe |
|---|---|---|
| `AdService.GetAds` | gRPC | Se `context_keys` bater com uma categoria conhecida, devolve os anúncios daquela categoria; senão devolve até `MAX_ADS_TO_SERVE = 2` anúncios aleatórios |

`[extracted, protos/demo.proto#L243-L263; src/adservice/src/main/java/hipstershop/AdService.java#L46, #L101-L132]`

## Consome
- Nenhum outro sistema — catálogo de anúncios embutido em memória no próprio serviço.

## Regra de negócio
Ver [limite de anúncios servidos](../../regras-de-negocio/limite-de-anuncios-servidos.md).
