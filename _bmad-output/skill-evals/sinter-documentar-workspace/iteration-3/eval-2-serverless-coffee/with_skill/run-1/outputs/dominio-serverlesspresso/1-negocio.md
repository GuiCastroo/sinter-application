# Negócio: Serverlesspresso

> **Em resumo:** uma cafeteria de eventos (pop-up, tipo re:Invent) em que o cliente pede café pelo
> celular escaneando um QR code no balcão, e o barista prepara na ordem em que os pedidos chegam.
> O domínio controla quem pode pedir, quantos pedidos cabem ao mesmo tempo, e acompanha cada
> pedido do QR code até um recibo final — sem fila física e sem dinheiro trocando de mãos no
> sistema.

## Nesta página

| Seção |
|---|
| [Em uma frase](#em-uma-frase) |
| [Por que existe](#por-que-existe) |
| [Faz / Não faz / Não sabemos](#faz--não-faz--não-sabemos) |
| [A parede do domínio](#a-parede-do-domínio) |
| [Jornadas principais](#jornadas-principais) |
| [Quem orquestra](#quem-orquestra) |
| [Regras que mandam](#regras-que-mandam) |
| [Entra e sai](#entra-e-sai) |
| [Linguagem](#linguagem) |
| [Indicadores](#indicadores) |

## Em uma frase
Deixar visitantes de um evento pedirem café pelo celular sem fila física, enquanto o sistema
controla o ritmo de pedidos para o barista dar conta e mostra o andamento em tempo real para
cliente, barista e organização.

## Por que existe
Foi criado como demonstração pública da AWS (re:Invent 2021) de como orquestrar um processo longo,
com esperas humanas, usando serviços serverless — não é um produto comercial de verdade.
Classificação: **genérico/demonstração** *(a confirmar — não há indicação de que sirva a um
negócio real de vendas de café)*.

## Faz / Não faz / Não sabemos
| Faz | Não faz | Não sabemos |
|---|---|---|
| Libera o pedido por QR code, limitado por janela de tempo | Cobrança e pagamento | Se há plano de cobrar pelo café no futuro |
| Limita pedidos simultâneos para não afogar o barista | Controle de estoque de insumos | Quem decide o cardápio de cada evento (endpoint de edição não encontrado) |
| Acompanha o pedido do início ao recibo, em tempo real | Entrega/logística fora do balcão | Papéis e donos de cada serviço (sem `CODEOWNERS`) |
| Autentica cliente e barista por SMS (sem senha) | Cadastro de produto/preço fora do cardápio do evento | Se times reais rodam isto em produção ou só em workshops |

## A parede do domínio
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Admin | Abre a loja e publica o cardápio do evento | Loja configurada | Pedido só é aceito com a loja aberta |
| 2 | Cliente | Escaneia o QR code do balcão | Pedido iniciado | Só se houver token livre na janela de 5 min (10 por padrão) |
| 3 | Sistema | Confere se a loja está aberta e há vaga | Loja indisponível *ou* pedido aceito | No máx. 20 pedidos em andamento ao mesmo tempo |
| 4 | Cliente | Escolhe a bebida e envia | Pedido registrado com número | Expira em 5 min se não enviar; bebida precisa constar do cardápio |
| 5 | Barista | Assume, prepara e conclui (ou cancela) | Pedido em preparo → concluído *ou* cancelado | Expira em 15 min se o barista não agir; cliente é avisado na hora |
| 6 | Sistema | Fecha o pedido e monta o recibo | Pedido finalizado | Recibo em HTML com a trilha de eventos com `userId` |

🟥 Consulte as [dúvidas de contexto na Referência](6-referencia.md#dúvidas-de-contexto).

## Jornadas principais
| Jornada | Em uma linha | Link |
|---|---|---|
| Pedir um café | QR code → bebida → preparo → recibo | [4-jornadas.md → Pedir um café](./4-jornadas.md#pedir-um-café) |
| Configurar o evento | Admin abre a loja e define o cardápio | [4-jornadas.md → Configurar o evento](./4-jornadas.md#configurar-o-evento) |

## Quem orquestra
| Jornada | Quem manda | Como |
|---|---|---|
| Pedir um café | Duas máquinas de Step Functions cooperando | Uma toca o relógio do pedido e pausa esperando ação humana; a outra recebe a ação (via API) e "acorda" a primeira |
| Configurar o evento | Ninguém — coreografia por eventos | Mudança na tabela dispara evento, que se espalha sozinho para quem escuta |

## Regras que mandam
Os limites e exceções desta perspectiva estão consolidados na [Referência](6-referencia.md#regras-de-negócio); consulte também as [dúvidas](6-referencia.md#dúvidas-e-perguntas).

## Entra e sai
| Direção | O quê | Com quem |
|---|---|---|
| Entra | Login por número de telefone + código SMS | 🩷 Amazon SNS (via Cognito) |
| Entra | Pedido escaneado, escolha de bebida, ações do barista | Cliente e Barista (apps não incluídos neste repositório) |
| Entra | Abertura/fechamento da loja e cardápio | Admin (app não incluído) |
| Sai | Atualização de pedido em tempo real | 🩷 AWS IoT Core → apps do cliente, barista e admin |
| Sai | Recibo do pedido | 🩷 Amazon S3 + CloudFront |
| Sai | Métricas operacionais | 🩷 Amazon CloudWatch |

## Linguagem
Os termos têm uma definição única na [Referência](6-referencia.md#glossário); consulte também as [dúvidas](6-referencia.md#dúvidas-e-perguntas).

## Indicadores
*(a confirmar — nenhum indicador de negócio está documentado no repositório; o mais próximo é a
extensão opcional `WaitTimes`, que calcula tempo médio de espera por bebida, e o `metrics-service`,
que conta pedidos, cancelamentos e timeouts no CloudWatch.)*

**Fontes:** `01-appCore/initDB/initMenuState.JSON`, `backends/4-order-processing/statemachine/op.asl.json`,
`backends/5-order-manager/statemachine/om.asl.json`, `backends/9-validator/code/*.js`,
README raiz e de cada backend, `extensions/WaitTimes/README.md`. A classificação em "Por que
existe" e os itens de "Não sabemos" são dedução a partir da ausência de código de cobrança/estoque
e da origem do repositório (evento re:Invent), não afirmação explícita encontrada no texto.
