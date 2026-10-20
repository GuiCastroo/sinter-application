# Negócio: Serverlesspresso

> **Em resumo:** cafeteria de eventos (pop-up, tipo re:Invent). O cliente escaneia um QR code no
> balcão, pede pelo celular e acompanha o pedido em tempo real; qualquer barista disponível assume,
> prepara e conclui. O sistema controla quem pode pedir (QR com cota por janela), quantos pedidos
> cabem ao mesmo tempo e cancela pedidos parados. Não há pagamento. É uma demonstração pública da
> AWS de processo longo com esperas humanas, não um produto comercial.

## Nesta página

| Seção |
|---|
| [Faz / Não faz / Não sabemos](#faz--não-faz--não-sabemos) |
| [A parede do domínio](#a-parede-do-domínio) |
| [Jornadas principais](#jornadas-principais) |
| [Regras que mandam](#regras-que-mandam) |
| [Entra e sai](#entra-e-sai) |
| [Indicadores](#indicadores) |

## Faz / Não faz / Não sabemos
| Faz | Não faz | Não sabemos |
|---|---|---|
| Libera o pedido por QR code, limitado por janela de tempo | Cobrança e pagamento | Se há plano de cobrar pelo café no futuro |
| Limita pedidos simultâneos para não afogar o barista | Controle de estoque de insumos | Quem edita o cardápio e como ([Q10](6-referencia.md#pendências)) |
| Acompanha o pedido do início ao recibo, em tempo real | Entrega/logística fora do balcão | Papéis e donos de cada serviço (sem `CODEOWNERS`) |
| Autentica cliente e barista por SMS (sem senha) | Cadastro de produto/preço fora do cardápio do evento | Se times reais rodam isto em produção ou só em workshops |

## A parede do domínio
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Admin | Abre a loja (o cardápio já está na tabela de config) | Loja configurada | Pedido só é aceito com a loja aberta |
| 2 | Cliente | Escaneia o QR code do balcão | Pedido iniciado | Só se houver token livre na janela de 5 min (10 por padrão) |
| 3 | Sistema | Confere se a loja está aberta e há vaga | Loja indisponível *ou* pedido aceito | No máx. 20 pedidos em andamento ao mesmo tempo |
| 4 | Cliente | Escolhe a bebida e envia | Pedido registrado com número | Expira em 5 min se não enviar; bebida precisa constar do cardápio |
| 5 | Barista | Assume, prepara e conclui (ou cancela) | Pedido em preparo → concluído *ou* cancelado | Expira em 15 min se o barista não agir; cliente vê a mudança pelo app (tempo real, sem garantia de entrega) |
| 6 | Sistema | Fecha o pedido e monta o recibo | Pedido finalizado | Recibo em HTML com a trilha de eventos com `userId` |

## Jornadas principais
| Jornada | Em uma linha | Quem conduz |
|---|---|---|
| [Pedir um café](4-jornadas.md#pedir-um-café) | QR code → bebida → preparo → recibo | Dois workflows que esperam cliente e barista |
| [Configurar o evento](4-jornadas.md#configurar-o-evento) | Admin abre a loja e define o cardápio | Ninguém: a mudança na tabela se espalha por eventos |

## Regras que mandam
- **Pedido parado é cancelado sozinho** ([R03/R04](6-referencia.md#regras-de-negócio)): 5 minutos
  para o cliente escolher a bebida, 15 minutos para o barista concluir.
- **Capacidade é 20 pedidos em andamento** ([R01](6-referencia.md#regras-de-negócio)), fixa no
  workflow. O campo `maxOrdersInQueue` da configuração **não** muda isso ([Q05](6-referencia.md#pendências)).
- **Ordem de atendimento não é garantida pelo backend:** a API que lista pedidos ao barista ordena
  pelo identificador aleatório do pedido, não pela chegada (o app do barista, fora deste
  repositório, pode reordenar); qualquer barista pode assumir qualquer pedido. "Um pedido por cliente" existe só como valor de configuração ([Q03](6-referencia.md#pendências)).

Glossário e demais regras na [Referência](6-referencia.md#glossário).

## Entra e sai
| Direção | O quê | Com quem |
|---|---|---|
| Entra | Login por número de telefone + código SMS | 🩷 Amazon SNS (via Cognito) |
| Entra | Pedido escaneado, escolha de bebida, ações do barista | Cliente e Barista (apps não incluídos neste repositório) |
| Entra | Abertura/fechamento da loja e cardápio | Admin (app não incluído) |
| Sai | Atualização de pedido em tempo real | 🩷 AWS IoT Core → apps do cliente, barista e admin |
| Sai | Recibo do pedido | 🩷 Amazon S3 + CloudFront |
| Sai | Métricas operacionais | 🩷 Amazon CloudWatch |

## Indicadores
Nenhum indicador de negócio documentado. O mais próximo: a extensão opcional `WaitTimes` (tempo
médio de espera por bebida) e o `metrics-service` (pedidos, cancelamentos e timeouts no CloudWatch).

**Fontes:** `01-appCore/initDB/initMenuState.JSON`, `backends/4-order-processing/statemachine/op.asl.json`,
`backends/5-order-manager/statemachine/om.asl.json`, `backends/9-validator/code/*.js`,
README raiz e de cada backend, `extensions/WaitTimes/README.md`.
`backends/5-order-manager/RestAPIs/api.yaml` (ordenação da lista do barista).
