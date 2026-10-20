# Relatório de documentação — Domínio Online Boutique

Documentação gerada a partir do repositório `microservices-demo` (Google Cloud, demo "Online Boutique"), commit `38e7348eb289eb5b87c0c6e8cb19ced0449dc389` (2026-09-18), lido em modo somente leitura. Repositório do domínio: `dominio-online-boutique/`, seguindo o Padrão de Documentação do Sinter (6 camadas + gavetas transversais). Todo item nasceu com `status: proposed` — precisa de aprovação humana antes de virar `approved`.

## Cobertura

**51 arquivos Markdown**, cobrindo os 12 sistemas do repositório (11 microsserviços de negócio + `loadgenerator`), o contrato gRPC compartilhado, a infraestrutura Kubernetes/GKE e o fluxo de compra ponta a ponta.

### Itens por camada

| Camada | Itens |
|---|---|
| 1. Negócio (capacidades, fluxo macro) | 4 |
| 2. Domínio (README, mapa, eventos) | 3 |
| 3. Subdomínio (4 subdomínios + sequência técnica do checkout) | 5 |
| 4. Sistema (12 sistemas + índice) | 13 |
| 5. Componente (PlaceOrder, Charge — aprofundamento seletivo) | 2 |
| 6. Infraestrutura (7 recursos + 2 ambientes) | 9 |
| Transversal (glossário, regras, decisões, padrões) | 15 |

### Extraído vs. inferido

Das ~59 entradas de proveniência registradas: **54 extracted** (lidas literalmente do código/manifestos/proto) e **5 inferred** (deduzidas — principalmente as capacidades de negócio da camada 1, que quase nunca estão explícitas no código-fonte, conforme esperado pelo padrão). Nenhum item de camada 4–6 (sistema/componente/infraestrutura) ficou como inferido sem uma leitura de código correspondente.

## Decisão de amplitude vs. profundidade

Priorizei **mapa completo e raso** sobre poucos sistemas detalhados, como recomendado no padrão: todos os 12 sistemas têm ficha completa (contratos, dependências, dados, qualidade), mas apenas 2 componentes foram detalhados a fundo (`checkoutservice.PlaceOrder` e `paymentservice.Charge` — as duas peças com mais regra de negócio). Os demais serviços gRPC têm 1–3 métodos cada e foram documentados na própria ficha do sistema (seção "Expõe"), sem um arquivo de componente por RPC, para não fragmentar em ~25 arquivos quase idênticos. Se for necessário aprofundar componente a componente (ex.: para os squads donos de `frontend` ou `cartservice`), a estrutura de pastas já está pronta (`sistemas/<s>/componentes/`, hoje vazias nesses casos).

## Conflitos encontrados

1. **Origem dos dados de câmbio** (`regras-de-negocio/moedas-suportadas.md`, `conflito: true`): o `README.md` da raiz do repositório-fonte diz que o `currencyservice` usa "real values fetched from European Central Bank" (tempo real); o código (`src/currencyservice/server.js`) carrega um JSON estático embutido na imagem, sem nenhuma chamada de rede em runtime. Registrei as duas versões e uma hipótese de explicação, sem resolver sozinho.

## Segredos encontrados

Nenhum valor de segredo (chave, token, senha, connection string com credencial) foi encontrado em texto plano no código ou nos manifestos. Um ponto a observar, sem valor exposto:
- `src/shoppingassistantservice/shoppingassistantservice.py#L33-L39` — o serviço busca a senha do AlloyDB em runtime via Google Secret Manager (`ALLOYDB_SECRET_NAME`); o nome do segredo está em variável de ambiente, o valor nunca aparece no repositório. Registrado em `infraestrutura/recursos/secret-manager.md`.
- Os manifestos Kustomize (`kustomize/components/spanner`, `.../alloydb`) têm placeholders (`SPANNER_DB_USER_GSA_ID`, `REDIS_CONNECTION_STRING`) que precisam ser preenchidos por quem for ativar essas variantes — não são segredos, são valores de configuração pendentes.

## Riscos técnicos identificados (não são segredos, mas vale destacar)

- **Cobrança sem pedido**: se `ShipOrder` falhar depois de `Charge` ter sido aprovado, o `checkoutservice` devolve erro ao cliente sem estornar a cobrança nem registrar o pedido (ver `regras-de-negocio/falha-pos-cobranca-nao-reverte-pedido.md` e o "Caminho de erro" em `fluxos/compra-do-cliente.sequencia.md`).
- **Sem persistência de pedido**: não existe uma tabela ou log de pedidos em lugar nenhum do domínio — `OrderResult` só existe na resposta da chamada. Qualquer necessidade de auditoria, histórico de compras ou relatório de vendas não é suportada hoje pelo código.
- **Carrinho não durável no ambiente padrão**: `redis-cart` usa `emptyDir`; um restart do pod apaga todos os carrinhos ativos.

## Perguntas para as pessoas

### Para o PM
1. A capacidade "Vender produtos online" e o fluxo "Compra do cliente" (`capacidades/`, `fluxos/`) descrevem corretamente a intenção de negócio, ou há nomes/objetivos oficiais diferentes?
2. É aceitável, do ponto de vista de negócio, que uma falha de frete pós-cobrança deixe o cliente pago sem um pedido registrado (ver risco acima)? Deveria existir estorno automático?
3. Existem indicadores de negócio (conversão, ticket médio, abandono de carrinho) definidos em outro lugar que deveriam aparecer na seção "Indicadores" do fluxo macro?
4. Quem é o dono/responsável de cada sistema (nenhum `CODEOWNERS` foi encontrado)?

### Para o arquiteto
5. Existe algum outro domínio de negócio real (fora desta demo) com o qual este domínio deveria se relacionar? Hoje não há evidência de nenhum.
6. Qual combinação de overlays Kustomize (`infraestrutura/ambientes/variantes-kustomize.md`) representa a produção real, se este repositório for adaptado além de demo — Redis in-cluster, Memorystore, Spanner ou AlloyDB para o carrinho? Istio/Service Mesh ligado ou não?
7. A ausência de mensageria assíncrona é uma escolha deliberada permanente, ou algo a introduzir se o domínio precisar notificar sistemas externos (ex.: um data warehouse) sobre pedidos concluídos?

### Para o tech lead
8. O conflito sobre a origem dos dados de câmbio (README vs. código) — o arquivo `currency_conversion.json` é atualizado manualmente a partir do BCE de tempos em tempos, ou o README está desatualizado?
9. Faz sentido propagar os erros específicos de `paymentservice` (`InvalidCreditCard`, `UnacceptedCreditCard`, `ExpiredCreditCard`) até o cliente, em vez do genérico "falha ao completar o pedido" que ele vê hoje?
10. Vale a pena aprofundar a documentação de componente a componente para `frontend` e `cartservice` (os dois sistemas com mais lógica própria além do simples proxy gRPC)?

## Como continuar esta documentação

- Estrutura e convenções: ver `README.md` na raiz deste repositório de domínio.
- Para atualizar depois de uma mudança no código-fonte: releia o item afetado (ele já tem `provenance` apontando pro arquivo/linha), atualize o corpo e adicione uma nova entrada de `provenance` com o novo commit — não crie um arquivo duplicado.
