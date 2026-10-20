# Revisão de qualidade do PRD — Sinter: Catálogo, passo 1 (Domínio)

- **PRD:** `docs/prd-dominio-2026-10-17/prd.md` (com Apêndice A)
- **Também lidos:** `addendum.md`, `.memlog.md`, `exemplo-catalogo/` (29 arquivos), `ARCHITECTURE-SPINE.md` (AD-18 a AD-24)
- **Rubrica:** `~/.claude/skills/bmad-prd/assets/prd-validation-checklist.md`
- **Data:** 2026-10-17
- **Nota sugerida (critério do validate.md):** *Fair* (nenhuma dimensão quebrada, mas há achados `high`)

## Veredito geral

O PRD tem uma tese clara (dar à IA um mapa do domínio do geral para o detalhe, com "não sabemos" explícito para ela não inventar), um modelo de dados coerente e um Apêndice A que já serve de contrato. Ele está próximo de pronto para implementar. O que trava é a borda entre o contrato e o uso. O exemplo, apresentado como "completo e válido", não passa nas regras do próprio PRD: há 23 problemas, 7 deles de schema. O caminho único de escrita (FR-18) não diz como se gravam itens embutidos e itens da raiz. E a hierarquia é escrita em três lugares, o que contraria o Princípio 1. Isso precisa ser fechado antes do núcleo (schemas + validação), porque o próprio addendum usa o exemplo como teste principal.

---

## 1. Pronto para decidir — adequada

As decisões aparecem como decisões, não como "considerações": área é rótulo e não nível (Glossário, FR-3), lifecycle vive só na aplicação (FR-8), o panorama de modernização é calculado (FR-5) e a jornada aponta para o subdomínio e não para a aplicação (FR-12). O §6 (fora do escopo) faz trabalho real. Falta dizer o que se abriu mão em algumas escolhas. Por exemplo, aplicações embutidas no subdomínio reduzem o número de arquivos, mas tornam a escrita de uma única aplicação dependente de reescrever o subdomínio inteiro (ver §4).

As questões em aberto (§9) são, na maioria, abertas de verdade. Duas, porém, já estão respondidas na prática. A Q4 (chaves em inglês ou português) já foi decidida pelo Apêndice A e pelo addendum ("Chaves em inglês"). A Q6 lista tipos de documento de um modelo anterior ("regulação, padrão, decisão, … nota"), que contradiz o enum atual (`negocio | ata | pauta | runbook | arquitetura | gerado | link`).

### Quais questões em aberto bloqueiam o início da implementação

| # | Questão | Bloqueia? | Por quê |
|---|---|---|---|
| Q1 | `event`/`job`/`data` no passo | **Não** | Campo novo e opcional é aditivo |
| Q2 | Herança com exceção | **Não** | O §6 já tira do escopo; a pergunta é para o futuro |
| Q3 | Objetivo de modernização por aplicação | **Não** | Aditivo; `modernized_by` cobre o passo 1 |
| Q4 | Chaves em inglês ou português | **SIM (fechar já)** | Define todos os nomes dos modelos Pydantic e do JSON Schema, que são o 1º passo da ordem de construção. A resposta de fato já é "inglês"; basta registrar |
| Q5 | Quem aprova | **Não** | O `[ASSUMPTION]` do FR-18 já dá um padrão funcional |
| Q6 | Tipos de documento | **Parcial** | O enum é fechado no schema, mas acrescentar um tipo é compatível. Corrigir a lista desatualizada para não induzir erro |

**Bloqueadores que não estão no §9 (adicionar):**
- **B1.** Como `apply` grava itens da raiz (`organization.yaml`, `repositories.yaml`, `regulations/`, `standards/`) e itens embutidos (aplicação, dado). Ver achado 2.
- **B2.** O que o `validate` faz com referências a `dom-`, `ext-`, `evt-` e `agenda-` que não têm arquivo no catálogo. Ver achado 4.
- **B3.** Qual é a fonte da verdade da hierarquia (`spec.parent` ou `Domain.spec.subdomains`). Ver achado 3.
- **B4.** O bloco `<EVIDÊNCIA>` é usado em Rule e Decision, mas só é definido dentro de Relation, e sem `contentHash`. Ver achado 7.

### Achados
- **medium** Q4 está decidida, mas aparece como aberta (§9 Q4; addendum "Notas de formato") — Quem implementar pode esperar a resposta ou, pior, começar em português. *Correção:* mover para decisão: "chaves em inglês, valores no idioma da empresa".
- **medium** Q6 contradiz o enum (§9 Q6 × Apêndice A, bloco DOC) — A lista ainda cita "regulação, padrão, decisão, nota", que deixaram de ser tipos de doc (`.memlog` linha 21). *Correção:* reescrever a pergunta sobre o enum atual ("faltam `contrato` e `politica`?").
- **high** Bloqueadores reais ficaram fora do §9 — B1 a B4 acima. *Correção:* incluí-los no §9, marcados como bloqueadores, ou resolvê-los antes de começar.

## 2. Substância em vez de enfeite — forte

Não há enfeite. Há um único protagonista (Rafael), e a jornada UJ-1 conduz requisitos concretos (`validate` que acha o subdomínio errado, `get --level 1`, "isso ninguém sabe ainda"). Os NFRs têm números (300 e 2.000 tokens, 3 s, determinismo byte a byte) e não são genéricos. As contra-métricas SM-C1 e SM-C2 são específicas do produto e boas.

### Achados
- **low** NFR-3 "numa máquina comum" e NFR-1 "~300 tokens" sem tokenizador definido (§7) — Os limites existem, mas a medida é ambígua. *Correção:* fixar o tokenizador (o de `core/context.count_tokens`, pela espinha) e uma máquina de referência (ex.: o CI).

## 3. Coerência estratégica — forte

A tese ("sem estrutura, a IA chuta", §1) leva aos princípios (§4), e os princípios explicam os FRs. A SM-2 valida a tese diretamente (a IA entende e não inventa), e não mede atividade. O escopo é do tipo "resolver o problema", com cortes coerentes (§6). O único desvio da tese é o envelope do domínio carregar campos obrigatórios de passos futuros (`nextTaskNumber`, `delivery`), comentado no §5.

## 4. Clareza do que é "pronto" — fraca

Esta é a dimensão mais fraca, e a que as histórias vão usar mais. Vários FRs têm critérios bons e testáveis: FR-1 (idempotente com aviso), FR-3, FR-12 (todo `next` existe), FR-17 e FR-18 ("rascunho com erro não é gravado, nem em parte"). Outros prometem comportamento que nenhum comando, campo ou regra entrega.

### Achados
- **high** O exemplo "completo e válido" falha nas regras do próprio PRD (§0, SM-1, addendum "tests/fixtures/exemplo-catalogo") — Um script de checagem contra o Apêndice A encontrou **23 problemas**:
  - **Schema (7):**
    - `organization.yaml` escreve `spec.domains`, que é `(calc)`. O addendum diz que o `validate` acusa campo calc escrito.
    - `repositories.yaml` não tem `metadata.name` nem `metadata.status`, que são `(obr)` no envelope.
    - As duas relações não têm `metadata.name`.
    - As duas relações usam `evidence[].contentHash`, que não existe no A.7.
  - **Referências (4):**
    - `repo-pagv-libs-comuns` e `repo-pagv-infra` não estão em `repositories.yaml`.
    - `jor-pagv-estornar-pagamento` não tem arquivo.
    - O `variantOf: jor-camb-enviar-moeda` aponta para uma jornada que não existe.
  - **Docs (12):** caminhos `path:` para `.md` que não existem (ex.: `docs/checkout/regras-parcelamento.md`, `docs/conciliacao/conc0100.md`, `docs/boletagem/runbook.md`).
  - **Fora da checagem:** nenhuma regra (`rule-*`), decisão (`ADR-*`) ou padrão (`std-*`) tem arquivo. Assim, os três formatos novos do Apêndice A (A.5, A.6 e `Standard`) não têm nenhum exemplo executável.

  *Correção:* dar ao exemplo duas camadas. Primeira: um núcleo que passa no `validate` com zero erros, criando os `.md` como stubs, os repos, a jornada base e pelo menos 1 Rule, 1 Decision e 1 Standard. Segunda: casos de erro propositais numa pasta separada (`tests/fixtures/invalid/`), com o erro esperado de cada um.
- **high** FR-18 não cobre os casos reais de escrita (FR-18; addendum "O que acontece num `sinter apply`", passo 6) — O passo 6 grava em `domains/<d>/<pasta do kind>/<id>.yaml`, o que não serve para Organization, RepositoryList, Regulation e Standard, que moram na raiz. O `sinter new` também não tem esses kinds, e o FR-2 ("manter as listas da organização") fica sem caminho. Para itens embutidos não está definido se o rascunho de "adicionar uma aplicação" é o subdomínio inteiro (substituição) ou um fragmento (merge). Por fim, "edição manual só vale depois de passar pelo mesmo caminho" não tem como ser verificado no passo 1: o mecanismo da espinha, `validate --ci` com trailers (AD-23), é do passo 8. *Correção:* (a) uma tabela "kind → caminho canônico" que inclua a raiz; (b) declarar que o rascunho é sempre o manifesto inteiro e que `apply` substitui o arquivo, com o diff no resumo; (c) incluir `organization`, `regulation`, `standard` e `relation` no `sinter new`, ou dizer que são só edição manual + `apply`; (d) rebaixar a frase sobre edição manual a "convenção" no passo 1, ou trazer o `validate --ci` para o escopo.
- **medium** O diagrama da jornada é gerado, mas por quem? (FR-12, critério 2) — Nenhum comando do addendum gera diagrama, e o `get` não promete isso. *Correção:* incluir `sinter get <jor> --format mermaid` (ou equivalente) com o critério "a saída é determinística e contém um participante por subdomínio/externo", ou mover o critério para o passo seguinte.
- **medium** "Herda a regulação de proteção de dados" não pode ser verificado (FR-19) — Nada no schema diz qual regulação é de proteção de dados: Regulation não tem categoria. *Correção:* acrescentar `Regulation.spec.category: data-protection | …`, ou um campo em `organization.yaml` (`dataProtectionRegulation: reg-lgpd`), e o critério "dado com `personalData: true` mostra essa regulação, marcada, no `get`".
- **medium** FR-6 promete conhecimento na aplicação e no repo, mas o Apêndice A só permite `docs` (FR-6 × A.3; bloco CONHECIMENTO "presente em domínio, subdomínio, jornada") — *Correção:* restringir o FR-6 ("aplicação e repo: só docs") ou acrescentar `regulations/standards/decisions` à aplicação.
- **medium** "Uma ata pode ser promovida a decisão" não tem mecanismo (FR-14) — Não há comando nem campo. A ligação existe só se a Decision tiver `evidence` apontando para o doc da ata. *Correção:* critério explícito: "`sinter new decision --from doc-<id>` cria a decisão com `evidence[0].source = doc-<id>`", ou "promover = criar Decision cuja evidência aponta para a ata; `get` da ata mostra a decisão".
- **low** FR-4 "Faz (3 a 5 itens)": isso é erro ou aviso? — O exemplo tem subdomínio com 1 e com 2 itens (o FR-4 vale só para domínio, mas o Apêndice A.3 diz "como no domínio"). *Correção:* dizer "aviso, não erro" e se vale também para subdomínio.
- **low** FR-13 sem critério (FR-13) — *Correção:* "a partir de um passo, `get <sub> --level 1` lista as aplicações; `get <app>` lista os repos e os docs; cada resposta cita o id do próximo nível".

## 5. Escopo honesto — adequada

O §6 é explícito e útil. Os `[ASSUMPTION]` estão em linha e quase todos aparecem no índice. A densidade de itens abertos (6 questões + 8 suposições) é razoável para um PRD interno. Duas coisas de escopo ficam implícitas. A primeira são os campos obrigatórios de funcionalidades fora do escopo: `nextTaskNumber` é do passo 7 (tarefas, espinha linha 136) e `delivery: pr` só faz sentido com push/PR (passo 8, §6). A segunda são as referências a domínios ainda não catalogados.

### Achados
- **medium** O domínio exige campos de passos futuros (A.2: `nextTaskNumber (obr)`, `delivery (obr)`) — Isso obriga a modelar e validar o que o passo 1 não usa, e `delivery: pr` contradiz o FR-18 ("grava" = commit local). *Correção:* deixar opcionais com padrão (`nextTaskNumber: 1`, `delivery: direct`), ou declarar no FR-18 o que `delivery: pr` faz no passo 1 (sugestão: nada, é ignorado).
- **low** Suposições do log não marcadas no PRD — `ext- sem arquivo [ASSUMPTION]` (`.memlog` linha 25) aparece sem marcação no A.8. A lista fechada de áreas, `[ASSUMPTION]` no log (linha 9), aparece no FR-3 como certeza. *Correção:* marcar e indexar, ou registrar no log que deixaram de ser suposições.

## 6. Uso pelos passos seguintes — adequada

O PRD alimenta a espinha (AD-18 e AD-22 citam "PRD-catálogo FR-3..FR-9, Apêndice A") e as histórias. O glossário existe, e os termos centrais (Domínio, Subdomínio, Aplicação, Doc, Pendência) são usados do mesmo jeito em todo o texto. As lacunas são de completude.

### Achados
- **high** A hierarquia é escrita em três lugares, contra o Princípio 1 e a AD-18 (§4 Princípio 1; A.2 `subdomains (obr)`; A.3 `metadata.domain (obr)` + `spec.parent (obr)`; `organization.domains (calc)` × `Domain.spec.parent`) — A espinha diz que a contenção é "só por `spec.parent`". Com `Domain.spec.subdomains` obrigatório, criar um subdomínio exige mexer em dois arquivos (FR-7 e FR-18 não dizem isso), e os dois podem divergir. O mesmo vale, em menor grau, para `Subdomain.journeys` e `Domain.mainJourneys` contra o `capability` dos passos. *Correção:* tornar `Domain.spec.subdomains` `(calc)` a partir de `parent` (como já é `organization.domains`). Definir `metadata.domain` = `spec.parent` para subdomínio, ou remover um dos dois. Deixar `journeys` do subdomínio `(calc)`. `mainJourneys` pode continuar escrito, porque é uma curadoria ("principais").
- **medium** Referências externas sem regra de validação (FR-17 "toda referência existe"; A.2 `boundaries`; A.4 `calls`, `event`, `orchestrator`) — O exemplo cita `dom-risco`, `dom-vendas`, `dom-fiscal`, `dom-financeiro`, `dom-contas`, `dom-cliente` e `dom-contabilidade`, que não existem no catálogo, e `ext-*`, `evt-*` e `agenda-batch`, que não têm arquivo por definição. Do jeito que está escrito, o `validate` falha em qualquer catálogo real, ou ignora essas referências sem dizer nada. Além disso, `agenda-` não está na tabela A.8, e a lista de prefixos da AD-18 não traz `org-`, `area-`, `ext-` e `evt-`. *Correção:* uma regra explícita no FR-17. Sugestão: `dom-` inexistente gera **aviso** ("domínio ainda não catalogado"), e `ext-`/`evt-`/`agenda-` só têm o formato verificado. Acrescentar `agenda-` ao A.8 e alinhar a AD-18.
- **medium** O glossário não cobre os termos do Apêndice A (§3) — Faltam Etapa, Passo, Externo (`ext-`), Evento, Regra, Decisão (ADR), Relação, Padrão, Regulação e Evidência. *Correção:* uma linha para cada.
- **low** Duas versões do formato (envelope `apiVersion: sinter.dev/v1` × `organization.spec.schemaVersion: 1`; NFR-6) — Não está dito qual delas a CLI compara para recusar um catálogo mais novo. *Correção:* escolher uma (sugestão: `schemaVersion` decide a compatibilidade e `apiVersion` só identifica o formato) e citar no NFR-6.
- **low** `metadata.status` sem semântica no passo 1 (envelope A) — `new` gera `candidate` ou `approved`? O `apply` muda o status? *Correção:* uma frase no FR-18 ("no passo 1, `apply` grava `approved`; os demais status chegam com a importação").

## 7. Formato adequado — forte

O PRD é de uma ferramenta interna com um operador (arquiteto/tech lead) e um consumidor (o agente). Ter uma única jornada, com protagonista e clímax, é o tamanho certo. O Apêndice A como contrato é o formato certo para um PRD que vai direto para schemas. Não está formalizado demais nem de menos.

---

## Verificações pedidas além da rubrica

### A. PRD × Apêndice A × exemplo-catalogo (script Python)

Um script checou o envelope, os campos permitidos e obrigatórios por kind, as listas embutidas (aplicação, repo da aplicação, dado, camada, etapa, passo, doc, evidência), os enums, o id igual ao nome do arquivo, o formato do `domainId`, `next`/`parallelWith`, e as referências a repo, área, camada, subdomínio, jornada, aplicação, `ref` de doc e `path` de doc.

**Resultado: 23 problemas.** Todos os campos usados no exemplo estão previstos no Apêndice A, **exceto** `evidence[].contentHash` (2 relações) e `organization.spec.domains` (previsto, mas como `(calc)`).

| Arquivo | Problema | Tipo |
|---|---|---|
| `organization.yaml` | `spec.domains` é `(calc)` e está escrito | schema |
| `repositories.yaml` | sem `metadata.name` e `metadata.status` (obr no envelope) | schema |
| `relations/rel-…pagv…yaml`, `relations/rel-…camb…yaml` | sem `metadata.name`; `evidence.contentHash` fora do A.7 | schema |
| `pagv/domain.yaml` | `repo-pagv-libs-comuns`, `repo-pagv-infra` fora de `repositories.yaml`; `jor-pagv-estornar-pagamento` sem arquivo; `docs/gerado/visao-geral.md` não existe | referência / doc |
| `camb/journeys/jor-camb-enviar-moeda-pf.yaml` | `variantOf: jor-camb-enviar-moeda` inexistente | referência |
| subdomínios PAGV e CAMB, jornada `pagar-pedido`, domínio CAMB | 11 `path:` para `.md`/`.drawio` inexistentes | doc |

**Outras divergências entre PRD, Apêndice A e exemplo (manuais):**
- **`contentHash`:** a AD-19 da espinha usa `contentHash` da evidência ("só volta se o `contentHash` da evidência mudar"), mas o A.7 não tem esse campo. Quem está atrás é o Apêndice, não o exemplo.
- **Bloco `<EVIDÊNCIA>`:** é usado em A.5 e A.6, mas só definido dentro de A.7. Deve virar bloco reutilizável junto de DOC e CONHECIMENTO.
- **Formato dos ids:** o log (linha 20) diz `app-<domínio>-<slug>`, o exemplo usa `app-pagv-…` e `sub-pagv-…`, e o A.3 diz só `app-<slug>`. Também não está dito se o slug de `dom-` é o `domainId` em minúsculas (pasta `domains/<id-domínio em minúsculas>/`).
- **`personalData: true` sem regulação ligada:** o dado `dat-camb-posicao-cambio` tem `personalData: true` e o domínio CAMB liga `reg-lgpd`. Funciona, mas só porque alguém lembrou de ligar (ver achado do FR-19).
- **README do exemplo desatualizado:** diz que `sub-pagv-autorizacao` "foi deixado de fora", mas o arquivo existe.
- **Contagens erradas nos comentários `$ sinter get dom-pagv --level 1`:** "Repos: 6", mas as aplicações somam 5 (7 com os compartilhados). "Conhecimento: … 2 negócio · 1 ata · 1 gerado" omite a pauta. Como os comentários ilustram o NFR-2 (determinismo), vale corrigir.
- **`[ASSUMPTION]` dentro de um valor:** em `jor-camb-enviar-moeda-pf.yaml`, o `onFailure` contém o texto `[ASSUMPTION]`. Isso é marcação de PRD dentro de dado, e a IA vai ler como fato. Usar `unknowns` em vez disso.

### B. PRD × `.memlog.md` (vale a entrada mais recente)

| Linha do log | Decisão | No PRD | Situação |
|---|---|---|---|
| 8 | Sigla = id-domínio; conflito com AD-18 | AD-18 atualizada (linha 27) | OK |
| 13 | `Domain.repositories`, `Subdomain.systems`, `knowledge` agrupado | trocado pelas linhas 19–21 | OK (as entradas novas vencem). O PRD não usa `knowledge:`, e a linha 21 implicitamente aposentou esse bloco. Seria bom registrar no log que `knowledge` deixou de existir |
| 15 | Passo com `system` | trocado pelas linhas 16 e 20 (`capability`, `application`) | OK |
| 19 | `sharedRepositories` [ASSUMPTION] | FR-4 [ASSUMPTION] | OK, mas **fora do índice §10** |
| 20 | ids `app-<domínio>-<slug>` | A.3 `app-<slug>` | **Diverge** |
| 24 | `data[]` **no subdomínio** | FR-19 + A.2 também no domínio ("se fizer sentido") | **PRD amplia sem registro no log** |
| 25 | `ext-` sem arquivo [ASSUMPTION] | A.8 sem marcação | **Suposição perdida** |
| 26 | Comandos `validate`, `catalog init`, `new`, `apply [--dry-run]`, `get --level`, `read`; `--json` e código de saída | só no addendum; os FRs não citam comandos (exceto UJ-1) | Aceitável (detalhe de implementação), mas o `--json` do FR-15 e os códigos de saída merecem um critério no FR-17 ("sai com 1 se houver erro") |
| 27 | Espinha atualizada | AD-23 admite edição manual oficializada por `validate --ci`; FR-18 diz "só vale depois de passar pelo mesmo caminho" | **Pequena divergência** (ver achado do FR-18) |

Nada no PRD contradiz a entrada mais recente do log, exceto o formato do id de aplicação (linha 20). Faltam no log a extensão de `data[]` ao domínio e a aposentadoria de `knowledge:`.

### C. Métricas mensuráveis?

- **SM-1 (cobertura do modelo, meta 100%):** **parcialmente mensurável.** "Sem gambiarra nem campo livre fora do schema" é subjetivo. *Correção:* "o exemplo passa no `sinter validate` com zero erros e zero campos desconhecidos; nenhum fato do domínio ficou só em comentário YAML". Hoje o exemplo falharia (23 erros, `contentHash`, `[ASSUMPTION]` dentro de um valor).
- **SM-2 (a IA entende, ≥ 9/10, zero invenções):** **ainda não mensurável.**
  - O questionário de 10 perguntas não existe.
  - "Resposta inventada" não tem critério de correção.
  - Não estão definidos o número de execuções nem o modelo e a versão.
  - A comparação "o mesmo agente recebendo só os repos" é impossível com o exemplo fictício, porque os repos não existem.

  *Correção:* incluir no addendum ou nos fixtures o questionário com gabarito, incluindo 2 perguntas cuja resposta certa é "pendência". Rodar N=5 vezes por modelo e exigir a meta na mediana. Trocar a linha de base por "o mesmo agente recebendo os docs `.md` e a wiki, sem o catálogo", ou adiar a comparação para o piloto real.
- **SM-3 (< 2 h para um domínio médio):** mensurável. Falta dizer quem modela (o Gui, já fluente no formato, enviesa) e se a skill pode ajudar (ela está fora do escopo). *Correção:* "pessoa que não escreveu o PRD, só com CLI + Apêndice A".
- **NFR-1/NFR-3:** mensuráveis depois de fixar o tokenizador e a máquina de referência (achado da §2).

---

## Notas mecânicas

- **Índice de suposições (§10):** falta o FR-4 (`sharedRepositories` `[ASSUMPTION]`). As demais entradas fecham nos dois sentidos.
- **Continuidade de ids:** o FR-9 é só um marcador ("incorporado ao FR-8") e o FR-19 fica entre o FR-8 e o FR-9. Funciona, mas confunde quem cria histórias por intervalo de FRs. Sugestão: deixar uma nota no FR-9 e mover o FR-19 para um §5.3.1, ou renumerar antes de gerar épicos.
- **Referências cruzadas:** `inputs` do frontmatter resolvem (todos os arquivos existem). A âncora `#apêndice-a--esqueleto-dos-arquivos` depende de como o renderizador trata acento e travessão; conferir no viewer usado.
- **Vocabulário:** `role` no A.3 inclui `infra`, mas o FR-8 lista "frontend, BFF, API, batch, lib" sem infra. Alinhar.
- **Prefixos:** `agenda-` (A.4 `orchestrator`) não está no A.8. `evt-` e `ext-` estão no A.8, mas não na AD-18.
- **UJ-1:** a jornada fala em "regulação de arranjos de pagamento só à Conciliação", e o exemplo usa `reg-bcb-arranjos-pagamento` sem arquivo. É coerente com o README ("deixadas de fora"), mas reforça o achado de que o exemplo não é "válido".
- **Seções obrigatórias:** todas presentes para um PRD interno de capacidade.
