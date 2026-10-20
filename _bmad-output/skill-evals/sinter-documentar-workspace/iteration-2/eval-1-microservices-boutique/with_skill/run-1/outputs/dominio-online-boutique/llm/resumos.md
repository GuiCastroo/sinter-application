# Online Boutique: resumos

Degrau 1. Cada página e cada seção de serviço e de jornada em poucas linhas. Para o detalhe, abra a seção indicada.

## Negócio (1-negocio.md)
loja online de decoração e vestuário onde qualquer visitante, sem cadastro, navega o catálogo, monta um carrinho e finaliza a compra informando endereço e cartão. A loja precifica na moeda escolhida, cobra, organiza o envio e confirma por email, em um só passo. Existe como vitrine de referência para construir e-commerce em microsserviços, não para vender de verdade *(a confirmar — ver "Por que existe")*.

Parede do domínio:
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

## Arquitetura (2-arquitetura.md)
11 microsserviços poliglotas (Go, Java, Node.js, Python, C#) que conversam quase exclusivamente por gRPC síncrono, definidos em um único contrato compartilhado (`protos/demo.proto`). Não há barramento de eventos nem fila — a única "orquestração" é o `checkoutservice`, que chama os demais em sequência dentro de uma requisição. O `frontend` é o único ponto de entrada externo; tudo mais é interno ao cluster.

## Serviços (3-servicos.md)
11 microsserviços (mais um 12º opcional, o assistente de compras) conversam quase só por gRPC síncrono, seguindo os contratos únicos de `protos/demo.proto`. Não há fila nem barramento de eventos: tudo é chamada-resposta. O `checkoutservice` é o único que chama vários outros serviços para completar uma ação de negócio (a compra); os demais são "folhas" que só respondem.

- **frontend** (3-servicos.md#frontend): único serviço com porta HTTP pública; monta as páginas do site e chama todos os outros serviços via gRPC (e o assistente via HTTP) para montar cada tela.
- **cartservice** (3-servicos.md#cartservice): guarda e devolve os itens do carrinho de cada usuário; se não houver Redis configurado, usa um armazenamento em memória do próprio processo (perde tudo ao reiniciar).
- **productcatalogservice** (3-servicos.md#productcatalogservice): fonte da verdade sobre os produtos; por padrão lê um JSON estático embutido na imagem, sem escrita — é só leitura.
- **currencyservice** (3-servicos.md#currencyservice): converte valores entre moedas usando uma tabela de taxas fixa embutida na imagem — apesar do README dizer que usa "valores reais do Banco Central Europeu", o código lê um arquivo JSON estático, não busca nada em tempo real.
- **shippingservice** (3-servicos.md#shippingservice): calcula uma cotação de frete fixa e gera um código de rastreio aleatório — não existe integração real com transportadora.
- **checkoutservice** (3-servicos.md#checkoutservice): o orquestrador da compra. Recebe o pedido do `frontend` e, em uma única chamada síncrona, busca o carrinho, precifica em moeda local, cota o frete, cobra o cartão, despacha o envio, esvazia o carrinho e dispara o email de confirmação.
- **paymentservice** (3-servicos.md#paymentservice): valida o cartão (formato, bandeira, validade) e devolve um ID de transação aleatório — não cobra nada de verdade, não há gateway de pagamento real.
- **emailservice** (3-servicos.md#emailservice): renderiza um HTML de confirmação de pedido com Jinja2 e loga que "enviaria" o email — não há envio real (sem SMTP/SendGrid configurado no código lido).
- **recommendationservice** (3-servicos.md#recommendationservice): sugere até 5 produtos do catálogo escolhidos aleatoriamente, excluindo os que já estão no carrinho — não é um motor de recomendação real (sem histórico, sem afinidade).
- **adservice** (3-servicos.md#adservice): devolve anúncios de texto estáticos, escolhidos por palavra-chave de categoria ou aleatoriamente — mapa de anúncios fixo no código, sem targeting real.
- **shoppingassistantservice (opcional)** (3-servicos.md#shoppingassistantservice-opcional): assistente de compras com IA generativa — recebe uma foto de um ambiente, usa Gemini para descrever o estilo, busca produtos parecidos por similaridade vetorial no AlloyDB e pede ao Gemini uma recomendação final. Só existe quando o componente Kustomize `shopping-assistant` é aplicado; não faz parte do deploy padrão.
- **loadgenerator** (3-servicos.md#loadgenerator): não faz parte do domínio de negócio — é uma ferramenta de suporte que simula clientes reais navegando, comprando e saindo, usada para gerar carga e tráfego de demonstração.

## Jornadas (4-jornadas.md)
a jornada central é a compra: o cliente navega sem login, monta um carrinho e fecha o pedido em uma única chamada síncrona orquestrada pelo `checkoutservice` (cobra, envia e notifica em sequência, sem fila). Há também a navegação/descoberta (home, busca, recomendação, anúncio) e, opcionalmente, um assistente de compras com IA. Nenhuma jornada usa um motor de processo — o que existe é coreografia simples via HTTP/gRPC dentro de uma única requisição.

- **Comprar um produto** (4-jornadas.md#comprar-um-produto): o cliente preenche endereço e cartão na tela de checkout; uma única chamada gRPC ao `checkoutservice` busca o carrinho, precifica em moeda local, cobra o cartão, despacha o frete, esvazia o carrinho e dispara o email — tudo antes de responder ao navegador.
- **Navegar e montar o carrinho** (4-jornadas.md#navegar-e-montar-o-carrinho): da home ao carrinho, cada tela busca só o que precisa em paralelo lógico — sem orquestrador, sem estado de sessão no servidor além do cookie `shop_session-id`.
- **Pedir ajuda ao assistente de compras (opcional)** (4-jornadas.md#pedir-ajuda-ao-assistente-de-compras-opcional): só existe quando o componente Kustomize `shopping-assistant` está habilitado. Cliente envia uma foto do ambiente; o assistente descreve o estilo com Gemini, busca produtos parecidos por similaridade vetorial e devolve uma recomendação em texto.

## Infraestrutura (5-infraestrutura.md)
roda em qualquer cluster Kubernetes (o "golden path" é um `kind` local ou GKE Autopilot via Terraform). Cada serviço é um `Deployment` + `Service` ClusterIP simples, sem banco gerenciado por padrão: carrinho fica em um Redis dentro do próprio cluster (`emptyDir`, sem persistência) e catálogo é um arquivo JSON embutido na imagem. Variações (Spanner, AlloyDB, Memorystore, Istio, políticas de rede) existem como componentes opcionais do Kustomize, nunca ligados por padrão — é uma regra de produto do repositório (ver `docs/product-requirements.md`).

## Referência (6-referencia.md)
glossário, regras e decisões consolidadas das outras páginas, mais um guia rápido para rodar o projeto localmente e uma lista de dúvidas por papel — a maior parte delas existe porque este é um repositório de demonstração técnica (não um produto com donos de negócio declarados), então informações de negócio muitas vezes precisam ser confirmadas com quem mantém o repositório.

