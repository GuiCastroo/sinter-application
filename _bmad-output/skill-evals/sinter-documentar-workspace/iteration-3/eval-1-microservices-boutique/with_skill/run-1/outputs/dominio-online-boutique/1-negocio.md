# Negócio: Online Boutique

> **Em resumo:** loja online de decoração e vestuário onde qualquer visitante, sem cadastro,
> navega o catálogo, monta um carrinho e finaliza a compra informando endereço e cartão. A loja
> precifica na moeda escolhida, cobra, organiza o envio e confirma por email, em um só passo.
> Existe como vitrine de referência para construir e-commerce em microsserviços, não para vender
> de verdade *(a confirmar — ver "Por que existe")*.

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
Permitir que qualquer visitante navegue por um catálogo de produtos, monte um carrinho e finalize
a compra em um único fluxo — sem login, sem cadastro, do jeito mais simples possível.

## Por que existe
Serve como aplicação de referência: mostra, de ponta a ponta, como uma loja com vários serviços
independentes pode ser construída e operada em Kubernetes. O próprio repositório declara isso
explicitamente (`docs/purpose.md`): a prioridade é demonstrar tecnologia de nuvem (Kubernetes,
observabilidade, malha de serviço) de forma acessível, e qualquer mudança que complique a jornada
de compra do usuário iniciante é desencorajada. Classificação: **domínio de suporte/genérico** para
quem o usa como está — não existe para gerar receita real *(a confirmar com quem mantém o
repositório, caso o uso pretendido seja outro)*.

## Faz / Não faz / Não sabemos
| Faz | Não faz | Não sabemos |
|---|---|---|
| Mostra e busca catálogo de produtos | Login ou conta de cliente | Se há plano de autenticação |
| Monta carrinho por sessão (cookie) | Gestão de estoque | Se a falta de estoque é intencional |
| Cobra, calcula frete e confirma o pedido em um fluxo só | Cobrança e frete reais (simulados) | Se algum dia plugam gateway/transportadora reais |
| Converte preços entre moedas | Câmbio em tempo real (README sugere, código não faz) | Por que README e código divergem |
| Sugere produtos e anúncios | Histórico ou "meus pedidos" | Se o pedido é descartado de propósito |

## A parede do domínio
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Cliente | Abre a loja | Sessão iniciada | Sem login; identidade é só um cookie |
| 2 | Cliente | Navega, busca e escolhe um produto | Produto visualizado | Recomendações e anúncio aparecem junto |
| 3 | Cliente | Adiciona o produto ao carrinho | Item adicionado ao carrinho | Sem checagem de estoque |
| 4 | Cliente | Informa endereço, email e cartão e confirma | Pedido solicitado | Formulário validado antes de prosseguir |
| 5 | Loja | Calcula o preço total na moeda do cliente (produtos + frete) | Preço do pedido calculado | Frete é fixo (US$ 8.99 se houver item, senão zero) |
| 6 | Loja | Cobra o cartão informado | Pagamento aprovado *ou* recusado | Só aceita Visa/Mastercard não vencido |
| 7 | Loja | Despacha o pedido | Pedido enviado (rastreio gerado) | Só acontece se o pagamento foi aprovado |
| 8 | Loja | Esvazia o carrinho e avisa o cliente por email | Pedido confirmado | Falha no aviso não desfaz a compra |

🟥 Consulte as [dúvidas de contexto na Referência](6-referencia.md#dúvidas-de-contexto).

## Jornadas principais
| Jornada | Em uma linha | Link |
|---|---|---|
| Comprar um produto | Do carrinho ao pedido confirmado, cobrança e envio inclusos | [4-jornadas.md#comprar-um-produto](4-jornadas.md#comprar-um-produto) |
| Navegar e montar o carrinho | Ver, buscar e adicionar produtos ao carrinho | [4-jornadas.md#navegar-e-montar-o-carrinho](4-jornadas.md#navegar-e-montar-o-carrinho) |
| Pedir ajuda ao assistente de compras | Sugestão de produtos a partir de uma foto (opcional) | [4-jornadas.md#pedir-ajuda-ao-assistente-de-compras-opcional](4-jornadas.md#pedir-ajuda-ao-assistente-de-compras-opcional) |

## Quem orquestra
| Jornada | Quem manda | Como |
|---|---|---|
| Comprar um produto | Um serviço orquestrador (`checkoutservice`) | Chama carrinho, catálogo, câmbio, frete, pagamento e email em sequência, dentro da mesma requisição — sem motor de processo nem fila |
| Navegar e montar o carrinho | Ninguém — coreografia simples | Cada tela do site busca só o que precisa, sem fluxo maior por trás |
| Pedir ajuda ao assistente | O próprio assistente (`shoppingassistantservice`) | Chama IA generativa e busca de produtos por conta própria, sem envolver o resto do domínio |

## Regras que mandam
Os limites e exceções desta perspectiva estão consolidados na [Referência](6-referencia.md#regras-de-negócio); consulte também as [dúvidas](6-referencia.md#dúvidas-e-perguntas).

## Entra e sai
| Direção | O quê | Com quem |
|---|---|---|
| Entra | Navegação, escolha de produtos, dados de endereço/cartão | Cliente (navegador) |
| Entra | Tráfego sintético para testes/demo | 🩷 `loadgenerator` |
| Sai | Preço final, confirmação do pedido, rastreio | Cliente (navegador) |
| Sai *(opcional)* | Foto do ambiente e pergunta | 🩷 Gemini (Google AI) — só se o assistente estiver habilitado |
| Sai *(opcional)* | Métricas, traces e profiling | 🩷 Google Cloud Operations — só se habilitado |

Este domínio não troca dado com nenhum outro domínio de negócio externo ao repositório: todos os
"parceiros" (pagamento, frete, email) são simulados internamente (ver `3-servicos.md`).

## Linguagem
Os termos têm uma definição única na [Referência](6-referencia.md#glossário); consulte também as [dúvidas](6-referencia.md#dúvidas-e-perguntas).

## Indicadores
Nenhum indicador de negócio (conversão, ticket médio, taxa de abandono) foi encontrado no
repositório — é esperado, já que o próprio domínio não persiste pedidos *(a confirmar com quem
decide o produto; hoje o indicador mais próximo é operacional: latência/erros por serviço, via
tracing e profiling opcionais)*.

**Fontes:** `docs/purpose.md`, `docs/product-requirements.md`, `README.md`,
`src/loadgenerator/locustfile.py` (jornada do cliente simulada), `src/checkoutservice/main.go`,
`src/paymentservice/charge.js`, `src/shippingservice/quote.go` — deduções de negócio marcadas
*(a confirmar)* porque o repositório é um projeto de demonstração técnica, não um produto real com
donos de negócio declarados.
