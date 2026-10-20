# Negócio: Serverlesspresso

> **Em resumo:** uma cafeteria de eventos em que o cliente pede pelo celular, escaneando um QR code no balcão, e o barista prepara na ordem da fila. O domínio controla quem pode pedir, quantos pedidos cabem ao mesmo tempo e o andamento de cada pedido até a entrega.

## Nesta página
| Seção | Em uma linha |
|---|---|
| [Em uma frase](#em-uma-frase) | O que é, para quem, por quê |
| [Por que existe](#por-que-existe) | O valor e a importância para o negócio |
| [Faz / Não faz / Não sabemos](#faz--não-faz--não-sabemos) | A fronteira do domínio |
| [A parede do domínio](#a-parede-do-domínio) | O que acontece, do QR code ao café na mão |
| [Jornadas principais](#jornadas-principais) | As histórias ponta a ponta |
| [Quem orquestra](#quem-orquestra) | Quem manda em cada jornada |
| [Regras que mandam](#regras-que-mandam) | As 4 regras que o negócio exige |
| [Entra e sai](#entra-e-sai) | O que o domínio avisa e recebe |
| [Linguagem](#linguagem) | Os termos que todo mundo usa igual |
| [Indicadores](#indicadores) | Como saber se está indo bem |

## Em uma frase
Permitir que visitantes de um evento **peçam café pelo celular sem fila física**, enquanto a loja controla o ritmo de pedidos para o barista dar conta.

## Por que existe
- Tira a fila do balcão: o cliente pede de onde estiver e é avisado quando o café fica pronto.
- Protege a operação: a loja nunca recebe mais pedidos do que o barista consegue fazer.
- **Classificação:** core (é o produto; sem ele não há venda). *(a confirmar)*

## Faz / Não faz / Não sabemos
| Faz | Não faz | Não sabemos |
|---|---|---|
| Libera o pedido por QR code do balcão | Cobrança e pagamento | Se haverá pagamento no futuro |
| Limita pedidos por janela de tempo e por fila | Cadastro de clientes com senha (entra só pelo celular) | Quem define o cardápio de cada evento |
| Controla a fila do barista (reivindicar, concluir, cancelar) | Estoque de insumos | O que acontece com o pedido cancelado pelo barista |
| Avisa o cliente do andamento em tempo real | Entrega na mesa | |
| Abre e fecha a loja e troca o cardápio | | |

## A parede do domínio
A linha do tempo de um pedido, no formato do Event Storming: 🟨 ator · 🟦 comando · 🟧 evento · 🟪 política · 🩷 sistema externo · 🟥 dúvida.

| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Cliente | Pede um código de acesso pelo celular | Código de acesso enviado | Entra por SMS 🩷 |
| 2 | Cliente | Escaneia o QR code do balcão | **Pedido iniciado** | Só se houver bebidas livres na janela de 5 min |
| 3 | Loja | Verifica se pode aceitar | **Loja indisponível** *ou* pedido aceito | Loja aberta e menos de 20 pedidos em andamento |
| 4 | Cliente | Monta e envia a bebida | **Pedido enviado** | Se passar de 5 min sem enviar → **Pedido expirado** |
| 5 | Loja | Dá um número e põe na fila | **Pedido na fila do barista** | — |
| 6 | Barista | Reivindica e prepara | **Pedido em preparo** | Se passar de 15 min → **Pedido expirado** |
| 7 | Barista | Conclui ou cancela | **Pedido pronto** *ou* **Pedido cancelado** | Cliente é avisado na hora |
| 8 | Cliente | Acompanha o status | **Jornada do pedido registrada** | — |

🟥 **Dúvidas na parede:** o evento final não diferencia "pronto" de "cancelado" para quem só escuta o fim do pedido; o barista cancela por quê?

## Jornadas principais
| Jornada | Em uma linha | Detalhe |
|---|---|---|
| Pedir um café | Do QR code do balcão ao café pronto, com avisos em tempo real | [4-jornadas.md#pedir-um-cafe](4-jornadas.md#pedir-um-cafe) |
| Operar a loja | Abrir, fechar, trocar o cardápio e ajustar o limite de bebidas | [4-jornadas.md#operar-a-loja](4-jornadas.md#operar-a-loja) |

## Quem orquestra
| Jornada | Quem manda | Como |
|---|---|---|
| Pedir um café | **Dois fluxos orquestrados** (AWS Step Functions): um cuida do pedido, outro da fila do barista | Conversam por eventos (EventBridge) e esperam a ação de pessoas (cliente e barista) |
| Operar a loja | Painel do operador, direto na configuração | Sem orquestração: cada mudança publica um aviso |

## Regras que mandam
| Regra | Valor atual |
|---|---|
| Pedidos simultâneos | no máximo **20** em andamento |
| Bebidas por janela | limite por QR code a cada **5 minutos** (configurável por evento) |
| Tempo para o cliente enviar | **5 minutos** depois de escanear |
| Tempo para o barista concluir | **15 minutos** depois de entrar na fila |

## Entra e sai
| Direção | O quê | Com quem |
|---|---|---|
| Entra | Login do cliente por SMS | Serviço de identidade 🩷 |
| Sai | Avisos de andamento do pedido | Celular do cliente e tela do barista (tempo real) |
| Sai | Métricas de pedidos | Painel de acompanhamento *(a confirmar quem consome)* |

## Linguagem
- **Pedido:** uma bebida pedida por um cliente, com número na fila.
- **Janela:** período de 5 minutos em que um QR code libera um número limitado de bebidas.
- **Reivindicar:** o barista assume um pedido da fila para prepará-lo.
- **Loja aberta/fechada:** se o balcão aceita pedidos agora.
- **Jornada do pedido:** o histórico visual de tudo que aconteceu com um pedido.

## Indicadores
- Pedidos por hora e tempo médio do QR code ao café pronto *(a confirmar com o negócio)*
- Taxa de pedidos expirados ou cancelados *(a confirmar)*

---
**Fontes:** fluxos de pedido e de fila (`order-processor`, `order-manager`); regras lidas na configuração dos fluxos e na tabela de configuração; eventos do barramento `Serverlesspresso`. O que está marcado *(a confirmar)* é dedução e precisa de validação do PM.
