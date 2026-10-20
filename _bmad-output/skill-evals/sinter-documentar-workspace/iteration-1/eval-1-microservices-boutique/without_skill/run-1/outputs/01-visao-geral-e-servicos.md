# 1. Visão Geral do Domínio

## 1.1 O que é

**Online Boutique** é uma loja virtual de demonstração (e-commerce) usada pelo
Google para mostrar modernização de aplicações em Kubernetes/GKE. O domínio de
negócio é simples e clássico de e-commerce: navegar catálogo, ver detalhes de
produto, adicionar ao carrinho, calcular frete/moeda, finalizar a compra
(checkout), pagar, enviar e confirmar por e-mail. Não há criação de conta,
login ou histórico de pedidos — cada visitante recebe um `session_id` anônimo
via cookie e esse identificador é a única "identidade" do usuário no sistema.

## 1.2 Catálogo de microsserviços

O domínio é implementado por **11 microsserviços de negócio** + 1 serviço de
carga sintética, cada um em uma linguagem diferente (propositalmente, para
demonstrar poliglotismo), todos se comunicando por **gRPC** usando um único
contrato compartilhado (`protos/demo.proto`).

| Serviço | Linguagem | Porta interna | Responsabilidade | Dependências de saída (gRPC) |
|---|---|---|---|---|
| `frontend` | Go | 8080 (HTTP) | Serve o site (HTML server-side), é o único serviço com Service `LoadBalancer`/ingress público; gera `session_id` por cookie | productcatalog, currency, cart, recommendation, shipping, checkout, ad, shoppingassistant (HTTP) |
| `cartservice` | C# (.NET) | 7070 | Guarda os itens do carrinho por `user_id` | Redis (`redis-cart:6379`) ou Spanner/AlloyDB conforme variante |
| `productcatalogservice` | Go | 3550 | Lista, busca e retorna produtos a partir de um JSON estático embarcado | nenhuma |
| `currencyservice` | Node.js | 7000 | Converte valores monetários entre moedas usando taxas fixas carregadas de um JSON (referência: BCE); é o serviço de **maior QPS** | nenhuma |
| `paymentservice` | Node.js | 50051 | "Cobra" um cartão de crédito (mock, não integra gateway real); valida número, bandeira (só aceita VISA/Mastercard) e validade | nenhuma |
| `shippingservice` | Go | 50051 | Calcula cotação de frete e "envia" o pedido gerando um `tracking_id` (mock) | nenhuma |
| `emailservice` | Python | 8080 (interno 5000 no manifest) | Envia (mock/log) e-mail de confirmação de pedido | nenhuma |
| `checkoutservice` | Go | 5050 | **Orquestrador do checkout**: busca carrinho, calcula preços, cobra pagamento, despacha envio, esvazia carrinho, dispara e-mail | cart, productcatalog, currency, shipping, payment, email |
| `recommendationservice` | Python | 8080 | Recomenda produtos a partir dos itens já vistos/no carrinho | productcatalog |
| `adservice` | Java | 9555 | Retorna anúncios textuais contextuais a partir de palavras-chave (categoria do produto) | nenhuma |
| `shoppingassistantservice` | Python (Flask) | 80 | Assistente de compras com IA generativa (Gemini via LangChain) sobre um vetor de produtos no AlloyDB (feature opcional) | AlloyDB, Gemini API (Google GenAI) |
| `loadgenerator` | Python/Locust | — | Não é serviço de negócio: simula usuários reais navegando/comprando, usado para gerar tráfego de teste/demo | frontend (HTTP) |

Fonte: tabela de serviços do `README.md` da raiz, cruzada com
`kubernetes-manifests/*.yaml` (portas e variáveis de ambiente reais) e o
código-fonte de cada serviço.

## 1.3 Papéis arquiteturais

- **Borda (edge):** `frontend` é o único ponto de entrada. Não existe API
  Gateway dedicado nem BFF separado — o próprio frontend em Go faz o papel de
  BFF, chamando os demais serviços via gRPC e renderizando HTML
  server-side (`html/template`).
- **Orquestrador de processo de negócio:** `checkoutservice` é o único
  serviço que orquestra uma transação de negócio de ponta a ponta (o
  checkout). Ele não tem estado próprio; cada chamada `PlaceOrder` é
  stateless e delega tudo a outros serviços.
- **Serviços de domínio "puro"/utilitário:** `productcatalogservice`,
  `currencyservice`, `shippingservice`, `paymentservice`, `adservice` — sem
  dependências de outros serviços internos, cada um resolve uma
  responsabilidade única e é fácil de testar isoladamente.
- **Serviço com estado (stateful):** `cartservice` é o único serviço de
  negócio com armazenamento persistente (Redis por padrão; Spanner ou AlloyDB
  como alternativas via Kustomize, ver documento 3).
- **Serviço de IA/experimental:** `shoppingassistantservice`, habilitado por
  flag (`ENABLE_ASSISTANT`), plugado à parte (feature opcional, não faz
  parte do fluxo padrão de checkout).
- **Geração de carga:** `loadgenerator` não participa do domínio de negócio;
  é uma ferramenta de teste que bate no `frontend` como um usuário real (ver
  `src/loadgenerator/locustfile.py`), útil como documentação viva do
  comportamento esperado do cliente (ver documento 4).

## 1.4 Modelo de dados compartilhado (contrato único)

Todos os serviços compilam o mesmo arquivo `protos/demo.proto` (pacote
`hipstershop`) para gerar seus stubs gRPC em cada linguagem. As principais
entidades de domínio, todas definidas nesse único contrato, são:

- `Product` (id, name, description, picture, `price_usd: Money`, categories)
- `Money` (currency_code ISO-4217, units, nanos — sem uso de `float`)
- `CartItem` / `Cart` (user_id + lista de CartItem)
- `Address` (street_address, city, state, country, zip_code)
- `CreditCardInfo` (number, cvv, mês/ano de expiração)
- `OrderItem` (CartItem + Money cost) e `OrderResult` (order_id,
  shipping_tracking_id, shipping_cost, shipping_address, items)
- `Ad` (redirect_url, text)

Não existe um "serviço de pedidos" com persistência própria: o `OrderResult`
é construído em memória pelo `checkoutservice` a cada `PlaceOrder` e nunca é
salvo em banco — o pedido "existe" apenas na resposta HTTP e no e-mail de
confirmação enviado.

## 1.5 O que este domínio NÃO tem (limites explícitos)

- Sem autenticação/login de usuário — identidade = cookie de sessão anônimo.
- Sem histórico de pedidos, sem tabela/DB de "orders".
- Sem mensageria assíncrona (fila, pub/sub, eventos) entre os 11 serviços —
  toda comunicação de negócio é **síncrona request/response via gRPC**
  (ver documento 2).
- Sem gateway de pagamento real, sem transportadora real — `paymentservice`
  e `shippingservice` são mocks determinísticos.
- Sem retries/circuit breaker explícitos no código de aplicação — a
  resiliência de rede, quando presente, vem da malha de serviço (Istio),
  não do código Go/C#/Python/Java em si (ver documento 2, seção de
  resiliência).
