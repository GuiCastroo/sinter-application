# Arquitetura: Serverlesspresso

> **Em resumo:** o pedido é coordenado por dois workflows de Step Functions (`order-processor` e
> `order-manager`) que cooperam por *task token* e `SendTaskSuccess`. Os demais serviços reagem a
> eventos no bus `Serverlesspresso` do EventBridge; configuração e estado também são lidos
> **diretamente** nas tabelas DynamoDB. A entrada é REST (API Gateway + Cognito) e a atualização dos
> apps usa MQTT (IoT Core). Os três frontends ficam fora deste repositório.

## Nesta página

| Seção |
|---|
| [Contexto](#contexto) |
| [Subdomínios](#subdomínios) |
| [Mapa dos serviços](#mapa-dos-serviços) |
| [Estilo de integração](#estilo-de-integração) |
| [Decisões que moldam](#decisões-que-moldam) |
| [Riscos técnicos](#riscos-técnicos) |

## Contexto

```mermaid
flowchart LR
  Cliente((Cliente)) --> SP[Domínio Serverlesspresso]
  Barista((Barista)) --> SP
  Admin((Admin)) --> SP
  SP --> SMS[🩷 SNS/SMS via Cognito]
  SP --> IOT[🩷 AWS IoT Core]
  SP --> CDN[🩷 CloudFront/S3 - recibo]
  SP --> CW[🩷 CloudWatch metrics]
```

Os 3 frontends (app do cliente, app do barista, painel admin) **não estão neste repositório**
(README raiz); eles só aparecem aqui como consumidores das APIs REST e do tópico IoT.

## Subdomínios

| Subdomínio | Responsabilidade | Serviços |
|---|---|---|
| Plataforma | Event bus, login por SMS, endpoint de tempo real | `00-baseCore` |
| Validação do pedido | Portão de entrada: QR code com token limitado por janela | `validator-service` |
| Configuração do evento | Cardápio, limites e loja aberta/fechada | `config-service` |
| Processamento do pedido | Relógio do pedido: capacidade, timeouts, task tokens | `order-processor` |
| Gestão do pedido | Ações do cliente e do barista sobre um pedido | `order-manager` |
| Tempo real | Espelha eventos de negócio nos 3 frontends | `publisher-service` |
| Recibo do pedido | Trilha de eventos + HTML final | `order-journey-service` |
| Métricas | CloudWatch customizado | `metrics-service` |
| Extensões | Simulação e analytics opcionais, desacoplados | `EventPlayer`, `OrderRobotExtension`, `PersistOrderMetricsToDynamoDB`, `WaitTimes` |

## Mapa dos serviços

<!-- MAPA-PRINCIPAL -->

O mapa mostra as dependências declaradas em [Serviços](3-servicos.md): a seta vai do consumidor ao
fornecedor; o rótulo diz se é evento, acesso a dado, callback ou chamada. **Não é cronologia** — a
ordem do pedido está na [jornada](4-jornadas.md#pedir-um-café). Tabelas como `CountingTable` aparecem
como destino "externo" só porque não são serviços; são recursos do próprio domínio, listados em
[Infraestrutura](5-infraestrutura.md).

## Estilo de integração

| De → Para | Estilo | Observação |
|---|---|---|
| Frontends → validator/config/order-manager | Síncrono (REST via API Gateway, auth Cognito) | Único ponto síncrono externo |
| validator-service → order-processor | Assíncrono (evento `Validator.NewOrder` inicia a Step Function) | Coreografia |
| order-processor ⇄ order-manager | **Orquestração cruzada** via *task token* persistido no DynamoDB + `SendTaskSuccess` | Não é nem puro evento nem chamada direta — um workflow pausa e o outro o resume |
| order-processor/order-manager → publisher-service, order-journey-service, metrics-service | Assíncrono (EventBridge, roteado por `detail-type`) | Coreografia pura, várias regras de rota por prefixo |
| publisher-service → frontends | Assíncrono (MQTT via IoT Core) | Sem confirmação de entrega tratada pelo domínio |
| config-service (mudança na tabela) → resto do domínio | Assíncrono (DynamoDB Streams → EventBridge) | Não há API para mudar o cardápio, só a tabela `storeOpen` |
| Workflows e lambdas → tabelas DynamoDB (config, pedidos, contagem) | Síncrono, acesso direto a dado | Estado compartilhado: vários serviços leem as mesmas tabelas |

## Decisões que moldam

Nenhum ADR existe no repositório; as decisões abaixo foram **reconstruídas a partir do código**.

| Decisão | Consequência | Fonte |
|---|---|---|
| Duas máquinas de Step Functions: uma pausa com `waitForTaskToken`, a outra recebe a ação via API e retoma a primeira com `SendTaskSuccess`, usando o DynamoDB como elo | Nenhuma função fica "viva" durante a espera humana; em troca, as máquinas ficam acopladas pela linha do pedido e um token perdido deixa o pedido preso até o timeout | `op.asl.json`, `om.asl.json` |
| IoT Core (MQTT) para tempo real, alimentado por lambdas "publisher" que escutam o bus por prefixo de `detail-type` | Sem polling nos apps; um evento novo só chega ao app se algum publisher já escutar aquele prefixo | `backends/6-publisher-service/template.yaml` |
| Uma tabela de config por `config-{eventId}`, propagada por DynamoDB Streams | Todo serviço lê a mesma tabela direto em vez de manter cópia; não há API para editar o cardápio, só `storeOpen` | `backends/2-config-service/`, `01-appCore/initDB/initMenuState.JSON` |

## Riscos técnicos

- **Limite de 20 pedidos simultâneos fixo no ASL** (não vem da config `maxOrdersInQueue`): mudar a
  capacidade do evento exige editar e reimplantar a máquina de estados, não só a config ([Q05](6-referencia.md#pendências)).
- **Task token perdido = pedido preso até o timeout.** O elo entre as duas Step Functions é um
  campo (`TaskToken`) numa linha do DynamoDB; se essa linha for sobrescrita, apagada ou o
  `ConditionExpression` falhar, o `order-processor` só sai da pausa quando o timeout (5 ou 15 min)
  estourar — não há alarme nem retry visível para esse caso.
- **`publisher-service` engole erro de IoT silenciosamente** (`try/catch` só loga): um frontend
  pode parar de receber atualização em tempo real sem que nada no backend acuse falha.
- **`order-journey-service` escuta *todo* evento do bus** (sem filtro de `detail-type`): qualquer
  novo tipo de evento adicionado ao domínio passa a ser processado por ele também, ainda que não
  pertença a um pedido — o primeiro `Choice` descarta o que não tem `userId`, mas isso significa
  reprocessar tudo o tempo todo.
- **Código inativo convivendo com o ativo:** risco de editar o caminho errado achando que é o que
  está no ar. Lista em [Infraestrutura](5-infraestrutura.md#código-encontrado-mas-não-implantado-a-confirmar).

**Fontes:** todos os `template.yaml`/`*.asl.json` e handlers citados em
[3-servicos.md](./3-servicos.md) e [5-infraestrutura.md](./5-infraestrutura.md); README raiz para
os frontends externos.
