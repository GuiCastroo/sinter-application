# Referência: Online Boutique

> **Em resumo:** glossário, regras e decisões consolidadas das outras páginas, mais um guia rápido
> para rodar o projeto localmente e uma lista de dúvidas por papel — a maior parte delas existe
> porque este é um repositório de demonstração técnica (não um produto com donos de negócio
> declarados), então informações de negócio muitas vezes precisam ser confirmadas com quem mantém
> o repositório.

## Nesta página
| Seção | Em uma linha |
|---|---|
| [Glossário](#glossário) | Termos técnicos e de negócio, uma definição cada |
| [Regras de negócio](#regras-de-negócio) | Onde cada regra vive no código |
| [Decisões](#decisões) | Por que o desenho é assim |
| [Padrões](#padrões) | Convenções que se repetem em todos os serviços |
| [Como começar](#como-começar) | Rodar local, testar, mudanças comuns, publicar |
| [Dúvidas e perguntas](#dúvidas-e-perguntas) | Conflitos, segredos e perguntas por papel |

## Glossário
| Termo | Definição |
|---|---|
| `user_id` / sessão | Identificador do cliente, gerado como cookie `shop_session-id`, sem cadastro |
| `Money` | Tipo comum (`currency_code`, `units`, `nanos`) usado em todo o `.proto` para valores monetários |
| `OrderResult` | Estrutura devolvida pelo checkout: id do pedido, rastreio, frete, endereço e itens |
| `ExtraLatency` | Atraso artificial configurável no `productcatalogservice`, usado para demonstrar observabilidade |
| Componente Kustomize | Pedaço opcional de configuração (`kustomize/components/*`) que soma-se ao deploy padrão |
| BOAT | Categoria de motor de processo de negócio (Camunda, Pega, Appian...) — **não usada** neste domínio |
| Golden user journey | Termo do próprio repositório (`docs/product-requirements.md`) para a jornada mínima que sempre precisa funcionar: visitar, adicionar ao carrinho, checkout pré-preenchido, concluir |

## Regras de negócio
| Regra | Valor atual | Onde está implementada |
|---|---|---|
| Bandeiras de cartão aceitas | Visa e Mastercard | `src/paymentservice/charge.js` |
| Cartão vencido é recusado | Validade > mês/ano atual | `src/paymentservice/charge.js` |
| Custo de frete | US$ 8.99 fixo (US$ 0 se carrinho vazio) | `src/shippingservice/quote.go` |
| Timeout de anúncio | 100 ms | `src/frontend/rpc.go` (`getAd`) |
| Máximo de recomendações mostradas | 4 (na home/produto) / 5 (retornadas pelo serviço) | `src/frontend/rpc.go` / `src/recommendationservice/recommendation_server.py` |
| Máximo de anúncios por resposta | 2 | `src/adservice/.../AdService.java` (`MAX_ADS_TO_SERVE`) |

## Decisões
Nenhum ADR formal foi encontrado (`docs/adr` ou `decisions/` não existem no repositório). As
decisões abaixo foram **reconstruídas** a partir do código e da documentação existente:

| Contexto | Escolha | Consequência |
|---|---|---|
| Preservar a "golden user journey" para iniciantes em Kubernetes (`docs/product-requirements.md`) | Nenhuma integração gerenciada (banco externo, service mesh, IA) entra no deploy padrão | Tudo isso vira componente opcional do Kustomize, nunca ligado por padrão |
| Um único contrato gRPC compartilhado (`protos/demo.proto`) | Todos os serviços geram seu client/server a partir do mesmo `.proto` (`genproto.sh` em cada serviço) | Contratos nunca divergem, mas qualquer mudança no `.proto` exige regenerar código em todas as linguagens |
| Serviços mock para pagamento, frete e email | Sem integração externa real nesses três | Domínio 100% autocontido, seguro para rodar em qualquer lugar sem custo/risco externo |
| Checkout orquestrado em código, não em eventos | `checkoutservice.PlaceOrder` faz tudo em uma chamada síncrona | Simples de entender e depurar; sem compensação automática se um passo falhar depois de outro ter sucedido |

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
- **Rodar localmente:** `skaffold dev` (usa `skaffold.yaml`) sobre um cluster local (`kind`/
  minikube) ou `kubectl apply -f release/kubernetes-manifests.yaml` num cluster já existente. Guia
  completo em `docs/development-guide.md` e `docs/cloudshell-tutorial.md`.
- **Testes:** cada serviço tem os seus (ex.: `product_catalog_test.go`,
  `shippingservice_test.go`) — rodar com a ferramenta nativa da linguagem (`go test`, etc.); não há
  um runner único para todo o domínio *(a confirmar)*.
- **Onde fica cada coisa:**
  - Contrato entre serviços: `protos/demo.proto`
  - Código de cada serviço: `src/<nome-do-serviço>/`
  - Deploy padrão: `kubernetes-manifests/`
  - Variações de deploy: `kustomize/components/*`
  - Terraform (cluster GKE): `terraform/`
  - Documentação do próprio repositório: `docs/`
- **As 3 mudanças mais comuns** (dedução a partir da estrutura do repo, não de um histórico de
  commits analisado):
  1. Alterar um serviço existente → mudar o código em `src/<serviço>/`, regenerar proto se o
     contrato mudou (`genproto.sh` de cada serviço), atualizar o `Deployment` correspondente em
     `kubernetes-manifests/` se a env/porta mudar.
  2. Adicionar um serviço novo → seguir `docs/adding-new-microservice.md`.
  3. Adicionar uma variação de infraestrutura → criar um novo componente em
     `kustomize/components/`, com seu próprio `README.md`, seguindo o padrão dos existentes.
- **Como publicar:** `cloudbuild.yaml` builda e publica as imagens; `release/` guarda os manifests
  "prontos" para consumo direto (`release/kubernetes-manifests.yaml`) — o gatilho exato de CI/CD
  não foi confirmado nesta rodada.

## Dúvidas e perguntas

**Conflitos entre fontes:**
- `README.md` do repositório diz que o `currencyservice` "usa valores reais buscados do Banco
  Central Europeu"; o código (`src/currencyservice/server.js` + `data/currency_conversion.json`)
  lê uma tabela estática embutida na imagem, sem chamada externa. Registrado também em
  `3-servicos.md` e `2-arquitetura.md`.

**Segredos (só localização, nenhum valor copiado):**
- `kustomize/components/shopping-assistant/shoppingassistantservice.yaml` linha ~51: variável
  `GOOGLE_API_KEY` com valor placeholder `GOOGLE_API_KEY_VAL` — precisa ser preenchida por quem
  fizer o deploy desse componente; não é uma chave real vazada, mas fica registrado o local.
- `src/cartservice/src/cartstore/AlloyDBCartStore.cs` e
  `src/shoppingassistantservice/shoppingassistantservice.py`: senha do AlloyDB é buscada em tempo
  de execução via Google Secret Manager (`ALLOYDB_SECRET_NAME`), nunca aparece em texto no
  repositório.

**Perguntas por papel:**

*Para o PM/dono de produto:*
- Este domínio deve ser tratado como base para uma loja real algum dia, ou permanece só como
  vitrine técnica? Isso muda se vale a pena resolver as lacunas abaixo (estoque, persistência de
  pedido, estorno).
- Faz sentido ter indicadores de negócio (conversão, ticket médio) ou isso está fora de escopo por
  definição?

*Para o arquiteto:*
- Quando um serviço mock (pagamento, frete, email) precisar virar integração real, o padrão
  esperado é manter tudo síncrono/gRPC ou introduzir eventos/filas para desacoplar o
  `checkoutservice` das falhas de terceiros?
- A ausência de persistência do pedido é aceitável permanentemente, ou existe um serviço de
  "orders" planejado que ainda não foi escrito?

*Para o tech lead:*
- Qual é o dono real de cada subdomínio (squad)? Este documento marcou todos como
  *(a confirmar)* porque o `CODEOWNERS` só define donos genéricos para o repositório inteiro.
  Nenhum times por serviço.
- Existe um plano para compensar (estornar) uma cobrança quando o envio falha depois do pagamento
  aprovado (ver `4-jornadas.md` → "Comprar um produto")?

**Fontes:** todas as páginas anteriores deste domínio; `.github/CODEOWNERS`;
`docs/adding-new-microservice.md`, `docs/development-guide.md`, `docs/cloudshell-tutorial.md`
(citados, não lidos por completo nesta rodada).
