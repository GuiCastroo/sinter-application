# Referência: Online Boutique

> **Em resumo:** definições únicas do domínio — glossário, regras com ID, padrões, como rodar e
> testar uma mudança, e um só registro de pendências. Decisões de arquitetura ficam em
> [Arquitetura](2-arquitetura.md#decisões-que-moldam).

## Nesta página

| Seção |
|---|
| [Glossário](#glossário) |
| [Regras de negócio](#regras-de-negócio) |
| [Padrões](#padrões) |
| [Como começar](#como-começar) |
| [Pendências](#pendências) |

## Glossário
| Termo | Definição |
|---|---|
| `user_id` / sessão | Identificador do cliente, gerado como cookie `shop_session-id`, sem cadastro |
| `Money` | Tipo comum (`currency_code`, `units`, `nanos`) usado em todo o `.proto` para valores monetários |
| `OrderResult` | Estrutura devolvida pelo checkout: id do pedido, rastreio, frete, endereço e itens |
| `ExtraLatency` | Atraso artificial configurável no `productcatalogservice`, usado para demonstrar observabilidade |
| Componente Kustomize | Pedaço opcional de configuração (`kustomize/components/*`) que soma-se ao deploy padrão |
| Golden user journey | Termo do próprio repositório (`docs/product-requirements.md`) para a jornada mínima que sempre precisa funcionar: visitar, adicionar ao carrinho, checkout pré-preenchido, concluir |
| Carrinho | Lista de produtos e quantidades que um cliente pretende comprar, associada à sessão |
| Pedido | O resultado de uma compra concluída: itens, frete, endereço e rastreio — existe só na resposta, não é guardado |
| Cotação de frete | Valor estimado de envio, calculado antes da compra ser confirmada |
| Moeda de exibição | A moeda em que os preços aparecem para o cliente, independente da moeda de cobrança |
| Recomendação | Produtos sugeridos ao cliente, sorteados entre os que não estão no carrinho |

## Regras de negócio
| ID | Regra | Valor atual | Onde está implementada |
|---|---|---|---|
| R01 | Bandeiras de cartão aceitas | Visa e Mastercard | `src/paymentservice/charge.js` |
| R02 | Cartão vencido é recusado | Validade ≥ mês/ano atual (o mês atual é aceito) | `src/paymentservice/charge.js` |
| R03 | Custo de frete | US$ 8.99 fixo (US$ 0 se carrinho vazio) | `src/shippingservice/quote.go` |
| R04 | Timeout de anúncio | 100 ms | `src/frontend/rpc.go` (`getAd`) |
| R05 | Máximo de recomendações mostradas | 4 (na home/produto) / 5 (retornadas pelo serviço) | `src/frontend/rpc.go` / `src/recommendationservice/recommendation_server.py` |
| R06 | Máximo de anúncios por resposta | 2 | `src/adservice/.../AdService.java` (`MAX_ADS_TO_SERVE`) |
| R07 | Falha ao esvaziar carrinho ou enviar email | Não bloqueia o pedido (apenas logada) | `src/checkoutservice/main.go` (`PlaceOrder`, após envio) |
| R08 | Identidade do cliente | Um cookie de sessão — não existe conta nem senha | `src/frontend/middleware.go` (`shop_session-id`) |
| R09 | Pagamento antes do envio, sem compensação | Falha em `ShipOrder` após `Charge` aprovado retorna `Unavailable`; nada é revertido | `src/checkoutservice/main.go` (`PlaceOrder`) |

R04 é regra técnica com efeito visível: se o anúncio não responder em 100 ms, a página abre sem anúncio.

## Padrões
- **Um serviço por linguagem "canônica" da tecnologia que demonstra**: Go para serviços simples,
  Node.js para os dois de I/O leve (`currencyservice`, `paymentservice`), Python para os que usam
  bibliotecas de ML/IA (`recommendationservice`, `emailservice`, `shoppingassistantservice`), C#
  para `cartservice`, Java para `adservice` — decisão pedagógica do repositório, não técnica
  *(a confirmar)*.
- **Health check gRPC padrão** (`grpc.health.v1`) em todos os serviços gRPC, usado pelas probes do
  Kubernetes.
- **Toggle por variável de ambiente** para tracing/profiler (`ENABLE_TRACING`, `DISABLE_PROFILER`)
  em quase todos os serviços.
- **Guia oficial para adicionar um serviço novo**: `docs/adding-new-microservice.md` (não lido em
  detalhe nesta rodada — consultar diretamente antes de propor um serviço novo).

## Como começar
- **Rodar localmente:** `skaffold dev` sobre um cluster local (`kind`/minikube) ou
  `kubectl apply -f release/kubernetes-manifests.yaml` num cluster existente. Guia completo em
  `docs/development-guide.md`.
- **Testar uma mudança (exemplo real):** o frete fixo (R03) é coberto por
  `src/shippingservice/shippingservice_test.go` (`TestGetQuote`). Em `src/shippingservice`, rode
  `go test`; o resultado esperado é `PASS`, com cotação de `8.99`. O CI executa o mesmo para
  `shippingservice`, `productcatalogservice` e `frontend/validator`, e `dotnet test src/cartservice/`
  para o carrinho (`.github/workflows/ci-pr.yaml`). Não há teste automatizado do checkout completo;
  para ele, rode a aplicação e use o `loadgenerator` ou o navegador. *Comandos não executados nesta revisão.*
- **Onde fica cada coisa:** contrato em `protos/demo.proto`; código em `src/<serviço>/`; deploy
  padrão em `kubernetes-manifests/`; variações em `kustomize/components/*`; cluster GKE em
  `terraform/`; documentação do repositório em `docs/`.
- **Mudanças mais comuns** (dedução pela estrutura, não por histórico de commits):
  1. **Alterar um serviço:** código em `src/<serviço>/`; se o contrato mudar, editar
     `protos/demo.proto` e rodar `genproto.sh` em **cada** serviço que usa a mensagem; atualizar o
     `Deployment` em `kubernetes-manifests/` se env/porta mudar.
  2. **Novo campo no produto:** `src/productcatalogservice/products.json` → mensagem `Product` em
     `protos/demo.proto` → `genproto.sh` no catálogo e no `frontend` (e nos demais consumidores do
     `Product`, como checkout e recomendação, se precisarem do campo) → exibir em
     `src/frontend/templates/product.html`/`home.html`.
  3. **Novo serviço:** seguir `docs/adding-new-microservice.md`.
  4. **Nova variação de infraestrutura:** novo componente em `kustomize/components/`, com `README.md`.
- **Publicar:** `cloudbuild.yaml` gera as imagens; `release/kubernetes-manifests.yaml` é o manifest
  pronto. O gatilho exato de CD não foi confirmado.

## Pendências
Registro único de perguntas em aberto e conflitos entre fontes. Fatos confirmados não entram aqui.

| ID | Tipo | Assunto | Pergunta ou conflito | Impacto | Evidência | Quem responde |
|---|---|---|---|---|---|---|
| Q01 | Produto | Destino do domínio | Continua vitrine técnica ou será base de loja real? | Define se vale resolver estoque, persistência de pedido e compensação | `docs/purpose.md` | Mantenedores |
| Q02 | Produto | Indicadores | Indicadores de negócio (conversão, ticket médio) estão fora de escopo por definição? | Sem pedidos persistidos não há como medir | `docs/product-requirements.md` | Mantenedores |
| Q03 | Arquitetura | Integrações reais | Quando um mock virar integração real, mantém gRPC síncrono ou introduz eventos? | Falha de terceiro passa a travar o checkout inteiro | `src/checkoutservice/main.go` | Arquitetura |
| Q04 | Arquitetura | Persistência do pedido | Pedido sem persistência é permanente ou falta um serviço de pedidos? | Impede "meus pedidos" e auditoria | `PlaceOrder` devolve e descarta `OrderResult` | Arquitetura |
| Q05 | Organização | Donos por subdomínio | Quem é dono de cada serviço? | `CODEOWNERS` só define donos genéricos | `.github/CODEOWNERS` | Tech lead |
| Q06 | Produto/arquitetura | Compensação | Como desfazer o pagamento quando o envio falha depois dele (R09)? | Obrigatório antes de qualquer pagamento real | `PlaceOrder` | Produto + arquitetura |
| Q07 | Conflito | Câmbio | README diz que `currencyservice` usa cotações do Banco Central Europeu; o código lê tabela estática (`data/currency_conversion.json`) | Preços convertidos podem estar desatualizados | `src/currencyservice/server.js` | Mantenedores |
| Q08 | Conflito | Modelo de embedding | Scripts geram embeddings com `textembedding-gecko@003`; o assistente consulta com `models/embedding-001` | Busca por similaridade pode retornar resultados ruins | `scripts/2_create_populate_alloydb_tables.sh`, `shoppingassistantservice.py` | Mantenedores |
| Q09 | Técnica | Falhas do assistente | Como o assistente reage a erro do Gemini/AlloyDB? | Sem tratamento visível; provável 500 | `shoppingassistantservice.py` | Dev |
| Q10 | Produto | Estoque | Ausência de estoque e de limite de quantidade é intencional? | Nada impede comprar quantidades arbitrárias | Nenhuma regra no código | Mantenedores |

**Segredos (só localização, nenhum valor copiado):** `GOOGLE_API_KEY` tem placeholder em
`kustomize/components/shopping-assistant/shoppingassistantservice.yaml`; a senha do AlloyDB vem do
Secret Manager (`ALLOYDB_SECRET_NAME`) em `AlloyDBCartStore.cs` e `shoppingassistantservice.py`.

**Fontes:** páginas anteriores deste domínio; `.github/CODEOWNERS`; `.github/workflows/ci-pr.yaml`;
`docs/adding-new-microservice.md` e `docs/development-guide.md` (citados, não lidos por completo).
