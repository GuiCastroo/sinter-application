---
id: dom-online-boutique-eventos
kind: domain
subject: domain:online-boutique:eventos
camada: 2
status: proposed
realiza: [dom-online-boutique]
realizado-por: []
provenance:
  - source: repo:microservices-demo
    locator: "grep -ril 'kafka|pubsub|rabbitmq|amqp|sqs|sns' src/ --include=*.go --include=*.py --include=*.js --include=*.cs --include=*.java (sem resultados)"
    version: 38e7348
    extraction: extracted
  - source: repo:microservices-demo
    locator: protos/demo.proto#L1-L263
    version: 38e7348
    extraction: extracted
---

# Eventos de domínio

Este domínio **não publica nem consome eventos assíncronos**. Foi buscado por bibliotecas e padrões de mensageria (Kafka, Pub/Sub, RabbitMQ/AMQP, SQS, SNS) em todo o código-fonte dos 12 serviços e não foi encontrado nenhum produtor ou consumidor — apenas menções incidentais em `go.sum`/`package-lock.json` (dependências transitivas de bibliotecas de nuvem, não usadas para mensageria). `[extracted]`

Toda a integração entre sistemas é **síncrona, ponto a ponto, via gRPC**, definida em um único arquivo de contrato (`protos/demo.proto` no repositório-fonte), resumido em [sistemas/README.md](../sistemas/README.md). Não existe, portanto, tabela de "Evento | Produtor | Consumidores | Contrato" para preencher — cada chamada é uma requisição-resposta RPC documentada na ficha de cada sistema (seções "Expõe"/"Consome") e nas sequências em [fluxos/](../fluxos/).

## Implicação para o negócio

Como não há barramento de eventos, não existe hoje um jeito de outro sistema (ex.: um ERP, um data warehouse) "escutar" pedidos concluídos sem chamar diretamente o `checkoutservice` ou fazer polling. Isso é uma limitação arquitetural a registrar caso o domínio precise notificar sistemas externos no futuro. `[inferred]`
