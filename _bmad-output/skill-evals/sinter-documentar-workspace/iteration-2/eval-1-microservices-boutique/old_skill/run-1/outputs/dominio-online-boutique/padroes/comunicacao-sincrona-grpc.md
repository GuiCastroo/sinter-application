---
id: std-comunicacao-sincrona-grpc
kind: standard
subject: standard:comunicacao-sincrona-grpc
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: protos/demo.proto#L1-L263
    version: 38e7348
    extraction: extracted
---

# Comunicação síncrona via gRPC, um contrato compartilhado

Todo sistema interno do domínio (exceto o `shoppingassistantservice`, HTTP/Flask) implementa um serviço gRPC gerado a partir do mesmo arquivo `protos/demo.proto`, versionado uma vez no monorepo e copiado (`genproto/`) para cada linguagem. Não há mensageria assíncrona (ver [eventos/README.md](../eventos/README.md)) — toda dependência entre sistemas é uma chamada bloqueante requisição-resposta.

## Exemplo
`checkoutservice` chama `pb.NewPaymentServiceClient(cs.paymentSvcConn).Charge(ctx, &pb.ChargeRequest{...})` — o mesmo padrão (`pb.New<Serviço>Client(conn).<Método>(ctx, &pb.<Request>{...})`) se repete em todos os clients gRPC do domínio, em todas as linguagens.

## Onde se aplica
Todas as chamadas entre `frontend`, `checkoutservice`, `cartservice`, `productcatalogservice`, `currencyservice`, `recommendationservice`, `adservice`, `shippingservice`, `paymentservice`, `emailservice`.
