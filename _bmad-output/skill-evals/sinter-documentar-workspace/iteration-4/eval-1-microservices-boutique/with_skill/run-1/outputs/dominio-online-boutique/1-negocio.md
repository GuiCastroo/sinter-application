# Negócio: Online Boutique

> **Em resumo:** loja online de demonstração. Qualquer visitante, sem cadastro, navega o catálogo,
> monta um carrinho e finaliza a compra com endereço e cartão, em um só passo. Pagamento, frete e
> email são **simulados**: nenhum dinheiro é cobrado e nada é enviado. O repositório existe para
> mostrar como construir e operar um e-commerce em microsserviços no Kubernetes, não para vender.

## Nesta página

| Seção |
|---|
| [Por que existe](#por-que-existe) |
| [Faz / Não faz / Não sabemos](#faz--não-faz--não-sabemos) |
| [A parede do domínio](#a-parede-do-domínio) |
| [Jornadas principais](#jornadas-principais) |
| [Regras que mandam](#regras-que-mandam) |
| [Entra e sai](#entra-e-sai) |
| [Indicadores](#indicadores) |

## Por que existe
O próprio repositório declara o propósito (`docs/purpose.md`): demonstrar Kubernetes,
observabilidade e malha de serviço de forma acessível. Mudanças que compliquem a jornada de compra
do iniciante são desencorajadas. Esse é um fato documentado, não uma hipótese.

## Faz / Não faz / Não sabemos
| Faz | Não faz | Não sabemos |
|---|---|---|
| Mostra e busca catálogo de produtos | Login ou conta de cliente | Se há plano de autenticação |
| Monta carrinho por sessão (cookie) | Gestão de estoque | Se a falta de estoque é intencional |
| Simula cobrança, frete e confirmação em um fluxo só | Cobrança e frete reais | Se algum dia haverá gateway/transportadora reais ([Q01](6-referencia.md#pendências)) |
| Converte preços entre moedas | Câmbio em tempo real (README sugere, código usa tabela fixa) | — (conflito registrado em [Q07](6-referencia.md#pendências)) |
| Sugere produtos e anúncios | Histórico ou "meus pedidos" | Se o pedido é descartado de propósito ([Q04](6-referencia.md#pendências)) |

## A parede do domínio
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Cliente | Abre a loja | Sessão iniciada | Sem login; identidade é só um cookie |
| 2 | Cliente | Navega, busca e escolhe um produto | Produto visualizado | Recomendações e anúncio aparecem junto |
| 3 | Cliente | Adiciona o produto ao carrinho | Item adicionado ao carrinho | Sem checagem de estoque |
| 4 | Cliente | Informa endereço, email e cartão e confirma | Pedido solicitado | Formulário validado antes de prosseguir |
| 5 | Loja | Calcula o preço total na moeda do cliente (produtos + frete) | Preço do pedido calculado | Frete é fixo (US$ 8.99 se houver item, senão zero) |
| 6 | Loja | Valida o cartão (cobrança simulada) | Pagamento aprovado *ou* recusado | Só aceita Visa/Mastercard não vencido |
| 7 | Loja | Despacha o pedido (simulado) | Pedido enviado (rastreio gerado) | Só acontece se o pagamento foi aprovado |
| 8 | Loja | Esvazia o carrinho e avisa o cliente por email | Pedido confirmado | Falha no aviso não desfaz a compra |

## Jornadas principais
| Jornada | Em uma linha | Quem conduz |
|---|---|---|
| [Comprar um produto](4-jornadas.md#comprar-um-produto) | Do carrinho ao pedido confirmado | `checkoutservice`, em sequência dentro de uma requisição |
| [Navegar e montar o carrinho](4-jornadas.md#navegar-e-montar-o-carrinho) | Ver, buscar e adicionar produtos | Cada tela do `frontend` busca o que precisa |
| [Pedir ajuda ao assistente](4-jornadas.md#pedir-ajuda-ao-assistente-de-compras-opcional) | Sugestão a partir de uma foto (opcional) | `shoppingassistantservice`, sozinho |

## Regras que mandam
- **Pagamento antes do envio, sem desfazer** ([R09](6-referencia.md#regras-de-negócio)): se o
  envio falha depois do pagamento aprovado, a compra termina com erro e nada é revertido. Hoje isso
  não custa dinheiro porque tudo é simulado; vira decisão obrigatória se pagamento real entrar
  ([Q06](6-referencia.md#pendências)).
- **Aviso não bloqueia a compra** ([R07](6-referencia.md#regras-de-negócio)): falha ao esvaziar o
  carrinho ou enviar o email é só registrada em log.
- **Pedido não fica guardado:** existe apenas na tela de confirmação; não há "meus pedidos".

Demais regras (bandeiras, frete, limites de anúncio e recomendação) e o glossário estão na
[Referência](6-referencia.md#regras-de-negócio).

## Entra e sai
| Direção | O quê | Com quem |
|---|---|---|
| Entra | Navegação, escolha de produtos, dados de endereço/cartão | Cliente (navegador) |
| Entra | Tráfego sintético para testes/demo | 🩷 `loadgenerator` |
| Sai | Preço final, confirmação do pedido, rastreio | Cliente (navegador) |
| Sai *(opcional)* | Foto do ambiente e pergunta | 🩷 Gemini (Google AI) — só se o assistente estiver habilitado |
| Sai *(opcional)* | Métricas, traces e profiling | 🩷 Google Cloud Operations — só se habilitado |

Nenhum parceiro de negócio externo: pagamento, frete e email são serviços internos simulados.

## Indicadores
Nenhum indicador de negócio (conversão, ticket médio) existe no repositório, o que é coerente com
uma demo que não guarda pedidos. O mais próximo é operacional: latência e erros por serviço, via
tracing e profiling opcionais. Não há motivo para inventar metas ([Q02](6-referencia.md#pendências)).

**Fontes:** `docs/purpose.md`, `docs/product-requirements.md`, `README.md`,
`src/loadgenerator/locustfile.py`, `src/checkoutservice/main.go`, `src/paymentservice/charge.js`,
`src/shippingservice/quote.go`.
