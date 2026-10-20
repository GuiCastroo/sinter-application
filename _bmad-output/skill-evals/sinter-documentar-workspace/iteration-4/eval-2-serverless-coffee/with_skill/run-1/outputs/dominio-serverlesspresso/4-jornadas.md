# Jornadas: Serverlesspresso

> **Em resumo:** duas jornadas. A principal é **Pedir um café**: do QR code escaneado no balcão até
> o recibo em HTML, orquestrada por duas máquinas de Step Functions que se revezam via *task
> token*. A segunda é **Configurar o evento**: como o admin abre/fecha a loja e muda o cardápio, e
> como isso se propaga sem nenhum orquestrador — por coreografia de eventos.

## Nesta página

| Seção |
|---|
| [Pedir um café](#pedir-um-café) |
| [Configurar o evento](#configurar-o-evento) |

## Pedir um café

**Participantes:** `validator-service`, `config-service`, `order-processor`, `order-manager`, `publisher-service`, `order-journey-service`, `metrics-service`

> **Em resumo:** o cliente escaneia um QR code liberado pelo balcão, escolhe a bebida, o barista
> prepara e conclui, e um recibo é gerado no fim. O pedido nunca fica "girando": ele existe como
> duas pausas de uma máquina de estados, acordadas por eventos quando alguém age.

### Em linguagem de negócio
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Cliente | Pede o código no balcão e escaneia o QR | Pedido iniciado | Só se houver token livre na janela de 5 min (10 por padrão) |
| 2 | Sistema | Confere se a loja está aberta e há vaga | Loja indisponível *ou* pedido aceito | Aceita só com loja aberta e menos de 20 pedidos em andamento |
| 3 | Cliente | Escolhe a bebida e envia | Pedido registrado com número | Expira em 5 min se não enviar; bebida precisa existir no cardápio do evento |
| 4 | Barista | Assume o pedido | Pedido em preparo | Qualquer barista autenticado pode assumir ou devolver (unmake) |
| 5 | Barista | Conclui ou cancela | Pedido concluído *ou* cancelado | Expira em 15 min se o barista não agir; app do cliente é atualizado por MQTT (falha de publicação só é logada) |
| 6 | Sistema | Fecha o pedido e monta o recibo | Pedido finalizado | Recibo em HTML publicado com a trilha de eventos com `userId` |

### Quem orquestra
Duas máquinas do Step Functions cooperam: **order-processor** é o dono do relógio (abre/fecha o
pedido, controla os dois tempos-limite), mas não fala com ninguém diretamente — ele publica um
evento com um `TaskToken` e **pausa**. Quem "acorda" ele é a segunda máquina, **order-manager**,
disparada via API Gateway sempre que o cliente ou o barista fazem uma ação; ela lê o token
salvo no DynamoDB e chama `SendTaskSuccess`. Não há coreografia aqui: sem uma ação humana passando
pelo order-manager, o order-processor fica parado até o timeout.

### Passo a passo técnico
```mermaid
sequenceDiagram
  participant A as Admin/display
  participant C as Cliente
  participant V as validator-service
  participant EB as EventBridge
  participant OP as order-processor (SFN)
  participant OM as order-manager (SFN + API)
  participant B as Barista
  participant PUB as publisher-service (IoT)

  A->>V: GET /qr-code (admin mostra QR no balcão)
  C->>V: POST /qr-code (escaneia código + token)
  alt sem tokens na janela de 5 min
    V-->>C: 200 "No tokens remaining"
  else código válido
    V-)EB: Validator.NewOrder
    EB-)OP: inicia execução
    alt loja fechada ou 20+ pedidos em andamento
      OP-)EB: OrderProcessor.ShopUnavailable
      EB-)PUB: publica no IoT (cliente é avisado)
    else loja aberta e com vaga
      OP-)EB: OrderProcessor.WorkflowStarted (aguarda até 5 min)
      EB-)OM: grava 1º TaskToken no pedido
      EB-)PUB: publica no IoT
      C->>OM: PUT /orders/{id} (bebida escolhida)
      OM->>OM: valida bebida no cardápio (sanitize)
      OM-->>OP: SendTaskSuccess (1º token)
      OP->>OP: gera o número do pedido
      OP-)EB: OrderProcessor.WaitingCompletion (aguarda até 15 min)
      EB-)OM: grava 2º TaskToken + número do pedido
      EB-)PUB: publica no IoT
      B->>OM: PUT /orders/{id}?action=make (assume)
      OM-)EB: OrderManager.MakeOrder
      EB-)PUB: publica no IoT
      B->>OM: PUT /orders/{id}?action=complete (ou cancel)
      OM-)EB: OrderManager.Order{eventId}-COMPLETED (ou CANCELLED)
      OM-->>OP: SendTaskSuccess (2º token)
      OP-)EB: OrderProcessor.orderFinished
      EB-)PUB: publica no IoT
    end
  end
```

Caminho de erro por timeout (fora do diagrama, para não poluir): se ninguém agir dentro dos 5 min
(cliente) ou 15 min (barista) de cada pausa, o `order-processor` emite `OrderProcessor.OrderTimeOut`
por conta própria e encerra o pedido como cancelado — o `order-manager` também consome o evento de timeout para atualizar o pedido.

### Regras que mudam o resultado
Capacidade de 20 fixa no ASL: [R01](6-referencia.md#regras-de-negócio). Cota de QR por janela:
[R02](6-referencia.md#regras-de-negócio). Timeouts de 5 e 15 minutos: [R03/R04](6-referencia.md#regras-de-negócio).
Cancelamento manual sem motivo estruturado: [Q09](6-referencia.md#pendências).

## Configurar o evento

**Participantes:** `config-service`, `publisher-service`

> **Em resumo:** o admin abre/fecha a loja e ajusta o cardápio direto na tabela de configuração;
> qualquer mudança se propaga sozinha para quem precisar saber, sem ninguém "chamando" ninguém.

### Em linguagem de negócio
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Admin | Abre ou fecha a loja / muda o cardápio | Configuração alterada | Toda mudança na tabela de config dispara aviso para os apps |

### Quem orquestra
Ninguém: é coreografia pura. A mudança acontece direto no DynamoDB (via API Gateway sem lambda no
meio), o DynamoDB Streams dispara `configChanged.js`, que publica `ConfigService.ConfigChanged` no
bus, e o `publisher-service` encaminha para o tópico IoT `serverlesspresso-config-{eventId}`. Não
há um serviço "dono" desse fluxo de ponta a ponta.

### Passo a passo técnico
```mermaid
sequenceDiagram
  participant A as Admin
  participant CFG as config-service
  participant DDB as ConfigTable (Streams)
  participant EB as EventBridge
  participant PUB as publisher-service

  A->>CFG: PUT /store (abre/fecha) ou edição direta do cardápio
  CFG->>DDB: UpdateItem
  DDB-)CFG: Stream (NewImage)
  CFG-)EB: ConfigService.ConfigChanged
  EB-)PUB: publica no tópico IoT de config
```

### Regras que mudam o resultado
A API só altera `storeOpen`; o cardápio é editado direto na `ConfigTable`, sem procedimento
documentado ([Q10](6-referencia.md#pendências)).

**Fontes:** `backends/4-order-processing/statemachine/op.asl.json`,
`backends/5-order-manager/statemachine/om.asl.json`, `backends/9-validator/code/*.js`,
`backends/5-order-manager/functions/*/app.js`, `backends/2-config-service/code/configChanged.js`,
`backends/2-config-service/RestAPIs/api.yaml`, `01-appCore/template.yaml`,
`01-appCore/initDB/initMenuState.JSON`. Ver também [3-servicos.md](./3-servicos.md).
