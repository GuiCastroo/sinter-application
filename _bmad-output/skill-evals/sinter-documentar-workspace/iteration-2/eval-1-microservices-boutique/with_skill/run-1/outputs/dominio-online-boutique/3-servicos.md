# Serviços: Online Boutique

> **Em resumo:** 11 microsserviços (mais um 12º opcional, o assistente de compras) conversam quase
> só por gRPC síncrono, seguindo os contratos únicos de `protos/demo.proto`. Não há fila nem
> barramento de eventos: tudo é chamada-resposta. O `checkoutservice` é o único que chama vários
> outros serviços para completar uma ação de negócio (a compra); os demais são "folhas" que só
> respondem.

## Nesta página
| Serviço | Subdomínio | Em uma linha |
|---|---|---|
| [frontend](#frontend) | Experiência do cliente | Site que serve HTML e chama todos os outros serviços em nome do navegador |
| [cartservice](#cartservice) | Carrinho | Guarda os itens do carrinho de cada usuário em Redis |
| [productcatalogservice](#productcatalogservice) | Catálogo | Lista, busca e detalha produtos a partir de um arquivo JSON (ou AlloyDB opcional) |
| [currencyservice](#currencyservice) | Precificação | Converte valores monetários entre moedas usando taxas estáticas |
| [shippingservice](#shippingservice) | Frete | Cota o frete e "envia" o pedido (mock, sem transportadora real) |
| [checkoutservice](#checkoutservice) | Checkout | Orquestra carrinho, preço, frete, pagamento e email para fechar o pedido |
| [paymentservice](#paymentservice) | Pagamento | Valida o cartão e "cobra" (mock, sem gateway real) |
| [emailservice](#emailservice) | Notificação | Renderiza e "envia" o email de confirmação (mock, sem SMTP real) |
| [recommendationservice](#recommendationservice) | Descoberta | Sugere produtos aleatórios que não estão no carrinho |
| [adservice](#adservice) | Descoberta | Sugere anúncios estáticos por categoria |
| [shoppingassistantservice](#shoppingassistantservice-opcional) | Descoberta | Assistente com IA generativa (RAG) — opcional, via Kustomize |
| [loadgenerator](#loadgenerator) | Suporte | Gera tráfego sintético simulando clientes reais |

---

## frontend
> **Em resumo:** único serviço com porta HTTP pública; monta as páginas do site e chama todos os
> outros serviços via gRPC (e o assistente via HTTP) para montar cada tela.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Experiência do cliente | *(a confirmar, ver CODEOWNERS: time único para o repo)* | Go, `gorilla/mux`, templates HTML | `src/frontend/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `GET /` | HTTP | Home: lista de produtos, moedas, carrinho atual |
| `GET /product/{id}` | HTTP | Detalhe do produto + recomendações + anúncio |
| `GET /cart`, `POST /cart`, `POST /cart/empty` | HTTP | Ver, adicionar e esvaziar o carrinho |
| `POST /setCurrency` | HTTP | Troca a moeda de exibição |
| `POST /cart/checkout` | HTTP | Dispara a compra (chama `checkoutservice`) |
| `GET /logout` | HTTP | Encerra a sessão (novo `shop_session-id`) |
| `POST /bot` | HTTP | Encaminha pergunta ao `shoppingassistantservice` (se habilitado) |
| `GET /_healthz` | HTTP | Liveness/readiness |

### Consome
| Serviço | Contrato | Tipo |
|---|---|---|
| productcatalogservice | `ListProducts`, `GetProduct`, `SearchProducts` | gRPC |
| currencyservice | `GetSupportedCurrencies`, `Convert` | gRPC |
| cartservice | `GetCart`, `AddItem`, `EmptyCart` | gRPC |
| recommendationservice | `ListRecommendations` | gRPC |
| shippingservice | `GetQuote` | gRPC |
| checkoutservice | `PlaceOrder` | gRPC |
| adservice | `GetAds` (timeout de 100 ms) | gRPC |
| shoppingassistantservice | `POST /` | HTTP (não gRPC — chamada direta com `http.NewRequest`) |

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `handlers.go` | rotas HTTP | Lê/valida formulário, chama os serviços, renderiza template |
| `rpc.go` | chamado pelos handlers | Centraliza as chamadas gRPC a cada serviço dependente |
| `middleware.go` | todo request | Gera/lê cookie `shop_session-id`, injeta logger e request-id no contexto |
| `validator/validator.go` | `POST /cart/checkout` | Valida os campos do formulário de pagamento/endereço antes de chamar o checkout |

### Dados
Não persiste nada: sessão do usuário é um cookie (`shop_session-id`), sem sessão no servidor.

### Quando falha
Qualquer erro de uma dependência vira HTTP 500 (`renderHTTPError`), exceto `getAd`, que tem timeout
de 100 ms e é ignorado silenciosamente se falhar (a home carrega sem anúncio). Sem retentativas
nem circuit breaker aparentes no código *(a confirmar)*.

### Infra que usa
`Deployment`/`Service` `frontend` + `frontend-external` (LoadBalancer) — ver `5-infraestrutura.md`.

**Fontes:** `src/frontend/handlers.go`, `rpc.go`, `main.go`, `middleware.go`, `kubernetes-manifests/frontend.yaml`.

---

## cartservice
> **Em resumo:** guarda e devolve os itens do carrinho de cada usuário; se não houver Redis
> configurado, usa um armazenamento em memória do próprio processo (perde tudo ao reiniciar).

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Carrinho | *(a confirmar)* | C# / .NET, gRPC | `src/cartservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `AddItem(user_id, item)` | gRPC | Adiciona item ao carrinho do usuário |
| `GetCart(user_id)` | gRPC | Retorna os itens do carrinho |
| `EmptyCart(user_id)` | gRPC | Esvazia o carrinho (usado pelo checkout após a compra) |

### Consome
Nenhum outro serviço do domínio — só o próprio armazenamento (Redis).

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `services/CartService.cs` | chamada gRPC | Implementa os 3 métodos acima |
| `cartstore/RedisCartStore.cs` | padrão, se `REDIS_ADDR` setado | Lê/escreve carrinho serializado no Redis |
| `cartstore/SpannerCartStore.cs` | componente Kustomize `spanner` | Alternativa gerenciada ao Redis |
| `cartstore/AlloyDBCartStore.cs` | componente Kustomize `alloydb` | Alternativa gerenciada ao Redis (busca senha no Secret Manager) |

### Dados
Entidade única: `Cart { user_id, items[] { product_id, quantity } }`. Sem histórico — é sempre o
estado atual do carrinho.

### Quando falha
Se o Redis cair, as chamadas de carrinho falham e o `frontend`/`checkoutservice` propagam erro 500
ao usuário. Sem fila de retry nem fallback.

### Infra que usa
`Deployment`/`Service` `cartservice` + `redis-cart` (`emptyDir`, **sem persistência em disco** —
um restart do pod do Redis apaga todos os carrinhos). Ver `5-infraestrutura.md`.

**Fontes:** `src/cartservice/src/services/CartService.cs`, `Startup.cs`,
`src/cartservice/src/cartstore/*.cs`, `kubernetes-manifests/cartservice.yaml`.

---

## productcatalogservice
> **Em resumo:** fonte da verdade sobre os produtos; por padrão lê um JSON estático embutido na
> imagem, sem escrita — é só leitura.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Catálogo | *(a confirmar)* | Go, gRPC | `src/productcatalogservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `ListProducts(Empty)` | gRPC | Lista todos os produtos |
| `GetProduct(id)` | gRPC | Detalhe de um produto |
| `SearchProducts(query)` | gRPC | Busca por nome/descrição (substring, case-insensitive) |

### Consome
Nenhum outro serviço do domínio.

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `catalog_loader.go` | toda chamada (ou 1x se `reloadCatalog=false`) | Carrega `products.json` local, ou AlloyDB se `ALLOYDB_CLUSTER_NAME` setado |
| `product_catalog.go` | chamada gRPC | Implementa `ListProducts`/`GetProduct`/`SearchProducts` sobre o catálogo carregado |
| `EXTRA_LATENCY` (env) | toda chamada | Injeta atraso artificial configurável — usado para demonstrar latência em observabilidade |

### Dados
`Product { id, name, description, picture, price_usd, categories[] }`. Fonte: `products.json`
(catálogo fixo de ~9 produtos) ou tabela AlloyDB equivalente *(a confirmar: schema exato da tabela AlloyDB)*.

### Quando falha
`GetProduct` retorna gRPC `NotFound` se o id não existir; sem isso, erros de leitura do arquivo
derrubam a resposta (catálogo vazio).

### Infra que usa
`Deployment`/`Service` `productcatalogservice`; opcionalmente AlloyDB (componente Kustomize
`alloydb`). Ver `5-infraestrutura.md`.

**Fontes:** `src/productcatalogservice/product_catalog.go`, `catalog_loader.go`, `products.json`,
`kubernetes-manifests/productcatalogservice.yaml`.

---

## currencyservice
> **Em resumo:** converte valores entre moedas usando uma tabela de taxas fixa embutida na
> imagem — apesar do README dizer que usa "valores reais do Banco Central Europeu", o código lê um
> arquivo JSON estático, não busca nada em tempo real.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Precificação | *(a confirmar)* | Node.js, gRPC | `src/currencyservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `GetSupportedCurrencies(Empty)` | gRPC | Lista de códigos de moeda suportados |
| `Convert(from, to_code)` | gRPC | Converte um `Money` para outra moeda |

### Consome
Nenhum outro serviço do domínio.

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `server.js` → `_getCurrencyData` | toda chamada | Lê `data/currency_conversion.json` (taxas fixas em relação a EUR) |
| conversão | `Convert` | Passa pela taxa EUR como pivô: `origem → EUR → destino` |

### Dados
Tabela estática de taxas (arquivo, não banco). Sem estado por usuário.

### Quando falha
Moeda não suportada gera erro gRPC; não há atualização de taxas em produção, então valores ficam
desatualizados com o tempo *(a confirmar se isso é intencional para a demo)*.

### Infra que usa
`Deployment`/`Service` `currencyservice`. Ver `5-infraestrutura.md`.

**Fontes:** `src/currencyservice/server.js` (função `_getCurrencyData`),
`src/currencyservice/data/currency_conversion.json`, README do repositório (contradiz o código —
registrado em `6-referencia.md`).

---

## shippingservice
> **Em resumo:** calcula uma cotação de frete fixa e gera um código de rastreio aleatório — não
> existe integração real com transportadora.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Frete | *(a confirmar)* | Go, gRPC | `src/shippingservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `GetQuote(address, items)` | gRPC | Retorna custo de frete estimado |
| `ShipOrder(address, items)` | gRPC | "Despacha" o pedido e devolve um `tracking_id` |

### Consome
Nenhum outro serviço do domínio.

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `quote.go` | `GetQuote` | Regra fixa: US$ 8.99 se o carrinho tiver ao menos 1 item, senão US$ 0 |
| `tracker.go` | `ShipOrder` | Gera um `tracking_id` aleatório (mock, não integra transportadora) |

### Dados
Sem persistência — cálculo puro por requisição.

### Quando falha
Sem casos de erro relevantes no código (função determinística sem I/O externo).

### Infra que usa
`Deployment`/`Service` `shippingservice`. Ver `5-infraestrutura.md`.

**Fontes:** `src/shippingservice/quote.go`, `tracker.go`, `kubernetes-manifests/shippingservice.yaml`.

---

## checkoutservice
> **Em resumo:** o orquestrador da compra. Recebe o pedido do `frontend` e, em uma única chamada
> síncrona, busca o carrinho, precifica em moeda local, cota o frete, cobra o cartão, despacha o
> envio, esvazia o carrinho e dispara o email de confirmação.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Checkout | *(a confirmar)* | Go, gRPC | `src/checkoutservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `PlaceOrder(user_id, user_currency, address, email, credit_card)` | gRPC | Executa a saga completa da compra |

### Consome
| Serviço | Contrato | Tipo |
|---|---|---|
| cartservice | `GetCart`, `EmptyCart` | gRPC |
| productcatalogservice | `GetProduct` | gRPC |
| currencyservice | `Convert` | gRPC |
| shippingservice | `GetQuote`, `ShipOrder` | gRPC |
| paymentservice | `Charge` | gRPC |
| emailservice | `SendOrderConfirmation` | gRPC |

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `PlaceOrder` (`main.go`) | chamada gRPC do frontend | Passo a passo descrito em `4-jornadas.md` |
| `prepareOrderItemsAndShippingQuoteFromCart` | dentro de `PlaceOrder` | Busca carrinho, converte preços, cota frete |
| `chargeCard` / `shipOrder` / `sendOrderConfirmation` | dentro de `PlaceOrder` | Chamam pagamento, envio e email, nessa ordem |

### Dados
Não persiste o pedido — gera um `order_id` (UUID) na hora e devolve o `OrderResult` completo na
resposta; não há tabela de pedidos *(a confirmar: pedido não fica em lugar nenhum após a resposta)*.

### Quando falha
- Falha ao buscar carrinho, converter moeda ou cotar frete → erro `Internal`, nada é cobrado.
- Falha ao cobrar o cartão (`chargeCard`) → erro `Internal`, pedido não avança (frete e email não
  acontecem).
- Falha no envio (`shipOrder`) **depois de já ter cobrado** → erro `Unavailable`; **não há
  estorno automático** no código — risco relevante (ver `2-arquitetura.md` → Riscos técnicos).
- Falha ao esvaziar o carrinho ou ao enviar o email → é **ignorada** (log apenas); o pedido é
  considerado concluído mesmo assim.

### Infra que usa
`Deployment`/`Service` `checkoutservice`. Ver `5-infraestrutura.md`.

**Fontes:** `src/checkoutservice/main.go` (função `PlaceOrder` e auxiliares, lidas por completo).

---

## paymentservice
> **Em resumo:** valida o cartão (formato, bandeira, validade) e devolve um ID de transação
> aleatório — não cobra nada de verdade, não há gateway de pagamento real.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Pagamento | *(a confirmar)* | Node.js, gRPC | `src/paymentservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `Charge(amount, credit_card)` | gRPC | "Cobra" o cartão e devolve `transaction_id` |

### Consome
Nenhum outro serviço do domínio.

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `charge.js` | `Charge` | Valida número via `simple-card-validator`; aceita só Visa/Mastercard; valida vencimento > mês atual; gera `transaction_id` com `uuidv4()` |

### Dados
Sem persistência — nenhuma transação é guardada em nenhum lugar.

### Quando falha
Lança `InvalidCreditCard`, `UnacceptedCreditCard` (bandeira não aceita) ou `ExpiredCreditCard`
(cartão vencido) — o `checkoutservice` propaga isso como falha e interrompe a compra antes de
cotar frete/enviar email.

### Infra que usa
`Deployment`/`Service` `paymentservice`. Ver `5-infraestrutura.md`.

**Fontes:** `src/paymentservice/charge.js` (lido por completo).

---

## emailservice
> **Em resumo:** renderiza um HTML de confirmação de pedido com Jinja2 e loga que "enviaria" o
> email — não há envio real (sem SMTP/SendGrid configurado no código lido).

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Notificação | *(a confirmar)* | Python, gRPC | `src/emailservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `SendOrderConfirmation(email, order)` | gRPC | Renderiza e "envia" a confirmação do pedido |

### Consome
Nenhum outro serviço do domínio.

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `email_server.py` | `SendOrderConfirmation` | Carrega template `templates/confirmation.html` (Jinja2) e renderiza com os dados do pedido |

### Dados
Sem persistência.

### Quando falha
Erro de template (`TemplateError`) é capturado e logado; o `checkoutservice` trata qualquer falha
aqui como não bloqueante (só loga um aviso, o pedido segue "concluído" para o cliente).

### Infra que usa
`Deployment`/`Service` `emailservice` (porta serviço 5000 → container 8080). Ver `5-infraestrutura.md`.

**Fontes:** `src/emailservice/email_server.py`, `email_client.py`,
`kubernetes-manifests/emailservice.yaml`.

---

## recommendationservice
> **Em resumo:** sugere até 5 produtos do catálogo escolhidos aleatoriamente, excluindo os que já
> estão no carrinho — não é um motor de recomendação real (sem histórico, sem afinidade).

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Descoberta | *(a confirmar)* | Python, gRPC | `src/recommendationservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `ListRecommendations(user_id, product_ids)` | gRPC | Devolve até 5 ids de produto que não estão em `product_ids` |

### Consome
| Serviço | Contrato | Tipo |
|---|---|---|
| productcatalogservice | `ListProducts` | gRPC |

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `recommendation_server.py` → `ListRecommendations` | chamada gRPC | Busca todos os produtos, remove os já no carrinho, sorteia até 5 (`random.sample`) |

### Dados
Sem persistência, sem uso real de `user_id` na lógica de seleção.

### Quando falha
Se `productcatalogservice` estiver fora, a chamada propaga erro; o `frontend` trata isso deixando
a home/checkout sem a seção de recomendados.

### Infra que usa
`Deployment`/`Service` `recommendationservice`. Ver `5-infraestrutura.md`.

**Fontes:** `src/recommendationservice/recommendation_server.py` (função `ListRecommendations`).

---

## adservice
> **Em resumo:** devolve anúncios de texto estáticos, escolhidos por palavra-chave de categoria ou
> aleatoriamente — mapa de anúncios fixo no código, sem targeting real.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Descoberta | *(a confirmar)* | Java, gRPC | `src/adservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `GetAds(context_keys[])` | gRPC | Até 2 anúncios relacionados às categorias informadas, ou aleatórios |

### Consome
Nenhum outro serviço do domínio.

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `AdService.java` → `createAdsMap` | inicialização | Monta mapa fixo categoria → anúncios (clothing, accessories, footwear, hair, decor, kitchen) |
| `getAds` | chamada gRPC | Busca por categoria; se vazio, sorteia 2 anúncios quaisquer |

### Dados
Mapa estático em memória, sem persistência.

### Quando falha
Chamado pelo `frontend` com timeout de 100 ms; se falhar ou estourar o tempo, a página segue sem
anúncio (erro é apenas logado no frontend).

### Infra que usa
`Deployment`/`Service` `adservice`. Ver `5-infraestrutura.md`.

**Fontes:** `src/adservice/.../AdService.java` (lido por completo).

---

## shoppingassistantservice (opcional)
> **Em resumo:** assistente de compras com IA generativa — recebe uma foto de um ambiente, usa
> Gemini para descrever o estilo, busca produtos parecidos por similaridade vetorial no AlloyDB e
> pede ao Gemini uma recomendação final. Só existe quando o componente Kustomize
> `shopping-assistant` é aplicado; não faz parte do deploy padrão.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Descoberta | *(a confirmar)* | Python/Flask, LangChain + Gemini + AlloyDB | `src/shoppingassistantservice/` |

### Expõe
| Contrato | Tipo | Para quê |
|---|---|---|
| `POST /` | HTTP | Recebe `{message, image}`, devolve `{content}` com a recomendação em texto |

### Consome
| Serviço/Sistema | Contrato | Tipo |
|---|---|---|
| Gemini (`gemini-1.5-flash`, Google AI) 🩷 | API de chat/visão | HTTP (via SDK `langchain_google_genai`) |
| AlloyDB 🩷 | busca vetorial (`AlloyDBVectorStore`) | SQL/vetor |
| Secret Manager 🩷 | leitura da senha do AlloyDB | API |

### Por dentro
| Componente | Gatilho | O que faz |
|---|---|---|
| `talkToGemini` (`shoppingassistantservice.py`) | `POST /` | 1) Descreve a imagem com Gemini; 2) busca produtos similares no AlloyDB; 3) pede recomendação final ao Gemini com a lista de produtos |

### Dados
Tabela vetorial no AlloyDB com `id, name, categories, description` e embedding
(`models/embedding-001`) — populada fora deste serviço *(a confirmar: script/processo de carga dos embeddings)*.

### Quando falha
Sem tratamento de erro visível no handler (`talkToGemini`) — qualquer exceção do Gemini ou do
AlloyDB provavelmente vira erro 500 não tratado *(a confirmar)*. No `frontend`, o handler
`chatBotHandler` retorna 500 se a chamada HTTP falhar ou o corpo não for o JSON esperado.

### Infra que usa
`Deployment`/`Service` `shoppingassistantservice` (só quando o componente Kustomize é aplicado) +
AlloyDB gerenciado + credencial `GOOGLE_API_KEY` (placeholder no manifesto, precisa ser preenchida
antes do deploy — ver `6-referencia.md`). Ver `5-infraestrutura.md`.

**Fontes:** `src/shoppingassistantservice/shoppingassistantservice.py` (lido por completo),
`kustomize/components/shopping-assistant/shoppingassistantservice.yaml`,
`kustomize/components/shopping-assistant/README.md`, `src/frontend/handlers.go` (`chatBotHandler`).

---

## loadgenerator
> **Em resumo:** não faz parte do domínio de negócio — é uma ferramenta de suporte que simula
> clientes reais navegando, comprando e saindo, usada para gerar carga e tráfego de demonstração.

| Subdomínio | Dono | Stack | Repositório |
|---|---|---|---|
| Suporte (fora do domínio de negócio) | *(a confirmar)* | Python/Locust | `src/loadgenerator/` |

### Consome
| Serviço | Contrato | Tipo |
|---|---|---|
| frontend | `/`, `/setCurrency`, `/product/{id}`, `/cart`, `/cart/checkout`, `/logout` | HTTP |

### Por dentro
`locustfile.py` define os pesos das ações simuladas: navegar (10x), ver carrinho (3x), trocar
moeda (2x), adicionar ao carrinho (2x), finalizar compra (1x), abrir a home (1x). Um init-container
espera o `frontend` responder 200 antes de começar.

### Infra que usa
`Deployment` `loadgenerator` (sem `Service`, não recebe tráfego). Pode ser removido via componente
Kustomize `without-loadgenerator`. Ver `5-infraestrutura.md`.

**Fontes:** `src/loadgenerator/locustfile.py`, `kubernetes-manifests/loadgenerator.yaml`.
