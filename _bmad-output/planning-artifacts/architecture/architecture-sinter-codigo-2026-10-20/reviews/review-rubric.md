# Revisão por rubrica — Espinha "Sinter, código da fatia 1"

- **Alvo:** `ARCHITECTURE-SPINE.md` (altitude feature) + `GUIA-EXTENSAO.md`
- **Pai (restrições):** `architecture-harness_corp-2026-09-26/ARCHITECTURE-SPINE.md` (AD-1..AD-24)
- **Spec:** `docs/prd-dominio-2026-10-17/{prd,addendum,epics}.md`
- **Data:** 2026-10-20

## Veredito

A espinha é sólida no esqueleto (camadas, composição, registro de regras, formatador único, golden files) e cobre os Epics 1–4 no mapa, mas **ainda não está pronta para as histórias**: contradiz ACs literais do Epic 1 e 3 (códigos de saída, forma do JSON de findings, estrutura/entrypoint da Story 1.1), não reconcilia o AD-3 herdado com `init`/`fmt`/`skills install`, deixa sem decisão pontos onde duas histórias vão divergir (descoberta da raiz do catálogo, diff semântico, atomicidade do `apply`, tratamento de `status`) e não decide o envelope operacional (empacotamento, publicação, CI, SO). O guia promete enforcement que o AD-34 não entrega.

## Placar da rubrica

| Critério | Resultado |
| --- | --- |
| Fixa os pontos reais de divergência para as histórias | Parcial — vários pontos abertos (H-5, M-1..M-8) |
| Cada Rule é aplicável e impede a divergência declarada | Parcial — AD-32/AD-3 sem mecanismo; AD-34 não cobre o que o guia diz (H-6) |
| Nada em Deferred permite divergência | OK — os itens adiados não criam bifurcação no passo 1 |
| Cobre os Epics 1–4 | Parcial — Epic 4 (`skills install`, evals) e `read` (Epic 2) subespecificados (M-9, M-10) |
| Nenhuma AD nova enfraquece/contradiz o pai | Parcial — AD-3 sem reconciliação (H-2); AD-28 relaxa a letra do AD-8 (M-11); AD-13/AD-9 ignorados (M-6, M-7) |
| Toda dimensão da altitude decidida, adiada ou aberta (incl. envelope operacional) | Falha — empacotamento, publicação, CI, SO-alvo, versão do pacote ausentes (H-4) |
| Guia consistente com a espinha | Parcial — H-2, H-6, M-12, L-6 |

---

## Achados

### Alta

#### H-1 — Códigos de saída contradizem as histórias
- **Local:** AD-33; Convenções → "Códigos de saída".
- **Problema:** AD-33 manda `NOT_A_CATALOG` para `1`. A Story 1.1 exige `2` para "pasta que não é catálogo (sem `organization.yaml`)", e a Story 3.1 exige `2` para `init` em pasta não vazia que não é catálogo. Além disso, a regra "uso errado = prefixo `USAGE_*`" não diz a que código vão casos já citados nas histórias: `schemaVersion` maior (Story 1.1 → `1`), arquivo sujo no `apply` (Story 3.3 → `1`), `new domain` com id existente (Story 3.4, sem código), âncora inexistente (Story 2.4 → `1`), git ausente / pasta sem repo no `apply`. Cada história vai escolher um código.
- **Correção:** acrescentar à AD-33 uma **tabela fechada** `code → exit` para todos os `SinterError` do passo 1 (ex.: `USAGE_NOT_A_CATALOG → 2`, `USAGE_INIT_NOT_EMPTY → 2`, `CATALOG_VERSION_UNSUPPORTED → 1`, `ITEM_NOT_FOUND → 1`, `ANCHOR_NOT_FOUND → 1`, `FILE_DIRTY → 1`, `ID_ALREADY_EXISTS → 1`, `NOT_A_GIT_REPO → ?`, `GIT_NOT_INSTALLED → ?`), e um teste de contrato que confere a tabela. Alinhar `NOT_A_CATALOG` com a Story 1.1 (→ `2`) ou corrigir a história, explicitamente.

#### H-2 — AD-3 herdado (caminho único de escrita) não reconciliado com `init`, `fmt` e `skills install`
- **Local:** Inherited Invariants (linha AD-3); AD-28; AD-30; Seed (`application/init.py`, `fmt.py`, `skills_install.py`); Guia "Três proibições" item 2.
- **Problema:** a espinha reafirma "`application.apply` é o único caso de uso que grava no catálogo", mas a Story 3.1 (`init`) cria `organization.yaml`, pastas e commit; a Story 3.7 (`fmt`) reescreve manifestos **sem commit**; `skills install` grava fora do catálogo. Ou essas escritas são exceções ao AD-3 do pai (e a espinha precisa dizer isso e por quê), ou têm de passar pelo `apply`. Do jeito que está, o primeiro dev de `init`/`fmt` viola a regra que o guia diz que "o `poe check` pega". Também nada impede tecnicamente outro caso de uso de chamar `CatalogFiles.write`.
- **Correção:** nova cláusula na AD-28/AD-30 (ou AD própria): "`CatalogFiles.write` é chamado só por `apply`, `init` (bootstrap do catálogo, antes de existir catálogo) e `fmt` (reescrita só de formato, verificada idempotente e sem mudança semântica — compara modelos antes/depois)". Tornar aplicável: um contrato de import-linter que só permita `application.{apply,init,fmt}` importar o módulo de porta de escrita (separar `CatalogWriter` de `CatalogReader`), ou um teste arquitetural que procura `.write(` fora desses módulos. Atualizar o pai (nota no AD-3) e o guia.

#### H-3 — Forma do resultado de validação diverge do AC (`findings` vs `errors[]`/`warnings[]`)
- **Local:** AD-31 (`Finding = {code, severity, file, path, message}`); AD-33 ("`findings` no `Result`").
- **Problema:** a Story 1.1 exige `--json` com `errors[]` e `warnings[]`; a Story 3.2 exige `{items, errors, warnings}`. A espinha fala em `findings` com `severity`. Golden files, schemas e as skills dependem disso; duas histórias vão produzir formas diferentes.
- **Correção:** fixar na AD-31 a forma pública: `ValidationResult = {errors: Finding[], warnings: Finding[]}` (separação feita num único helper em `ports/inbound`), `Finding` sem `severity` no JSON ou com ela redundante — decidir. Definir também `Finding.file` como caminho **relativo à raiz do catálogo, com `/`** (determinismo entre SOs) e `path` como caminho de campo em notação ponto/colchete (`spec.applications[2].lifecycle`).

#### H-4 — Envelope operacional não decidido (empacotamento, publicação, CI, SO)
- **Local:** Stack; Structural Seed; AD-34; Deferred (ausente).
- **Problema:** a altitude é dona disso e nada está decidido nem adiado: (a) **build backend** (hatchling? `uv_build`?) e como `skills/` e `schemas/` (fora de `src/`) entram no wheel — o pai (AD-12, AD-17) exige que sejam publicados no pacote e `skills install` copia "a versão que acompanha a CLI"; (b) **fonte única da versão** (usada no trailer `Sinter-Version`, no `skills install` "de qual versão para qual" e no `schemaVersion` suportado); (c) **publicação** (PyPI? índice privado? `uv tool install sinter` precisa de um índice); (d) **CI**: provedor, matriz de Python (3.13 e 3.14, que o pai declara como alvo) e de SO; (e) **SO-alvo** — AD-30 exige LF, mas Windows/`core.autocrlf` não é tratado, e caminhos em `Finding.file`/golden variam por SO; (f) versão mínima de `git`.
- **Correção:** nova AD "Empacotamento e distribuição" + linha na tabela de Stack: backend escolhido, `skills/` e `schemas/` incluídos como package data e lidos via `importlib.resources`, versão única em `pyproject.toml` lida por `importlib.metadata`, CI com matriz {3.13, 3.14} × {ubuntu, macos} (Windows adiado explicitamente ou incluído), `.gitattributes` com `* text eol=lf` no catálogo criado por `init`, git ≥ X. O que não for decidido vai para Deferred com gatilho.

#### H-5 — Estrutura e entrypoint da Story 1.1 contradizem a espinha sem declaração de precedência
- **Local:** AD-25; Seed (`sinter = "sinter.adapters.inbound.cli.app:main"`); Stack.
- **Problema:** o AC da Story 1.1 é literal: `[project.scripts] sinter = "sinter.cli:app"` e "estrutura `core/` + `adapters/` + `cli.py`"; o addendum mostra o mesmo layout e `ports.py` com `CatalogStore`; epics/addendum fixam Pydantic 2.13 e Typer 0.26 (a espinha: 2.14/0.27). Quem implementar a Story 1.1 cumprindo o AC viola AD-25; quem seguir AD-25 reprova no AC.
- **Correção:** declarar no topo da espinha (ou em AD-25) "Esta espinha substitui a seção *Estrutura do projeto* do addendum e o AC estrutural da Story 1.1", e abrir a correção nos epics/addendum (entrypoint, layout, versões). Registrar o mapeamento `core/schemas → domain/model`, `core/authoring → application/apply+new`, `ports.py/CatalogStore → ports/outbound/{catalog_files,manifest_codec}`.

#### H-6 — Enforcement prometido não existe (AD-34 vs guia)
- **Local:** AD-34; AD-1 herdado ("sem relógio"); AD-32; Guia "Três proibições (o `poe check` pega todas)".
- **Problema:** `lint-imports` só vê imports. Não pega: `print` fora da CLI, leitura de relógio (`datetime.now`, `time.time` — stdlib, permitida no domínio), `open()`/`Path.read_text` no domínio, nem "só `apply` grava". "Domínio só importa stdlib e Pydantic" exige `include_external_packages` e contrato explícito. `mypy --strict` só em `domain`/`application` deixa adaptadores e `bootstrap` sem checagem de conformidade com os `Protocol` — justamente onde o hexágono quebra.
- **Correção:** acrescentar à AD-34: ruff `T20` (proíbe `print`) com exceção para `adapters/inbound/cli`; `flake8-tidy-imports.banned-api` em `domain/` e `application/` para `datetime.datetime.now`, `datetime.date.today`, `time.time`, `builtins.open`, `pathlib.Path.read_text/write_text`, `subprocess`, `sys.stdin`; `include_external_packages = true` com contrato "domain não importa ruamel/typer"; `mypy --strict` no pacote inteiro. Ajustar o guia para listar quais checagens pegam cada proibição.

#### H-7 — Descoberta da raiz do catálogo não decidida; guia contradiz o `bootstrap`
- **Local:** AD-27 (`build(catalog_root, …)`); Guia Receita 1 (`ListAreasRequest.catalog_root: Path`).
- **Problema:** só `validate [pasta]` e `catalog init [pasta]` recebem pasta. `get`, `find`, `list`, `read`, `new`, `apply`, `fmt` não dizem como acham o catálogo (diretório atual? subir até achar `organization.yaml`? `--catalog`/`SINTER_CATALOG`?). Cada comando vai resolver de um jeito. Além disso, o guia põe `catalog_root` no `Request`, enquanto AD-27 o amarra no `Container` — duas fontes da mesma informação.
- **Correção:** decidir numa AD (ou na AD-27): a raiz é resolvida **só** na CLI, por `--catalog <pasta>` > `SINTER_CATALOG` > subir a partir do cwd até achar `organization.yaml`; o resultado vai para `build(catalog_root)` e **nunca** aparece em `Request`. Corrigir o exemplo da Receita 1. Dizer como `skills install` (sem catálogo) e `init` (catálogo ainda inexistente) montam o container.

### Média

#### M-1 — Preservação da ordem das chaves (Story 3.3) vs formatador canônico (AD-30)
- **Local:** AD-30.
- **Problema:** a Story 3.3 diz que "comentários **e a ordem das chaves** são preservados ao gravar"; AD-30 reordena as chaves para a ordem do modelo. A Story 3.7 dá razão à espinha, mas a 3.3 continua com o AC oposto.
- **Correção:** declarar na AD-30 que ela prevalece sobre o AC da Story 3.3 ("ordem preservada" passa a ser "ordem canônica, comentários preservados") e pedir correção da história.

#### M-2 — Diff semântico não fixado ("sem mudança", mudança só de formato)
- **Local:** AD-29/AD-30; `domain/services/diff.py`.
- **Problema:** Story 3.3 ("nada mudou → sem commit") e Story 3.7 ("`--dry-run` não acusa diferença só de formato") dependem de **como** se compara. Comparar texto, dict ou modelo dá resultados diferentes (comentário mudou é mudança? chave desconhecida?).
- **Correção:** regra: `diff` compara **modelos Pydantic normalizados** (`model_dump(mode="json", exclude_unset=False)`), campo a campo; mudança só de comentário/formato = `sem mudança` para o resumo, mas — decidir — gera ou não commit (recomendação: gera se o texto formatado do arquivo difere, com ação `format`).

#### M-3 — Atomicidade do `apply` e escopo do commit
- **Local:** AD-28 (`VersionControl.commit(paths, …)`); sequência no Seed.
- **Problema:** "nada é gravado, nem em parte" (Story 3.3) é garantido só para erros de validação. Falha de I/O no 2º arquivo ou falha do `git commit` deixa gravação parcial. Também não está dito que o commit inclui **só** os `paths` (com índice pré-existente do usuário, `git commit` comum leva junto o que estava em stage).
- **Correção:** regra: gravar em arquivos temporários e renomear todos; se o commit falhar, restaurar os arquivos (ou `git checkout -- paths`) e devolver erro; `commit` usa pathspec (`git commit --only -- <paths>`) e recusa se houver stage alheio nos mesmos paths.

#### M-4 — `load` com arquivos inválidos e cascata de erros
- **Local:** AD-29; AD-31.
- **Problema:** `Catalog` é feito de modelos válidos; o que acontece com um arquivo que falha na fase 1? Ele some do índice e gera erros falsos de "referência inexistente" em quem o cita. Também é ambíguo se o caso de uso **recebe** o `Catalog` (AD-29: "Todo caso de uso recebe") ou o **carrega** (guia Receita 1; diagrama de sequência).
- **Correção:** `load(...) -> (Catalog, list[Finding])`; ids de arquivos inválidos ficam indexados como "presentes, inválidos" para não gerar cascata; decidir uma frase: "o caso de uso chama `load` no início do `__call__`" (ou "a CLI carrega e passa no `Request`" — mas não os dois).

#### M-5 — `apply` bloqueia por erros pré-existentes em outros arquivos?
- **Local:** AD-29 ("`apply` valida `catalog.with_replaced(rascunho)`").
- **Problema:** se o catálogo já tem erro (edição manual — permitida no passo 1, FR-18), validar o catálogo inteiro faz todo `apply` falhar, inclusive o que corrigiria outra coisa. Cada implementador decidirá se filtra por itens tocados.
- **Correção:** regra: `apply` falha só por erros **novos ou em itens do rascunho** (diferença de findings antes/depois); erros pré-existentes voltam como `warnings` com código próprio. Ajustar também `with_replaced` para cobrir criação (`with_upserted`).

#### M-6 — `metadata.status` e o modo `official` do pai (AD-13) ignorados
- **Local:** Inherited Invariants (AD-13 ausente); `domain/services/levels.py`, `search.py`.
- **Problema:** todo manifesto tem `status` (`candidate|approved|rejected|deprecated|superseded`). O pai diz que consultas/projeções usam só `approved`. A espinha não diz se `get`/`find`/`list` filtram, marcam ou ignoram itens não aprovados — `find` e `get` vão divergir.
- **Correção:** herdar AD-13 e decidir: no passo 1, `get/find/list` mostram só `approved`, exceto `get <id>` direto, que mostra e marca o status; `validate` valida todos.

#### M-7 — `read` devolve conteúdo de doc sem herdar AD-9 (dado marcado)
- **Local:** Inherited Invariants (AD-9 ausente); Epic 2 → `read`.
- **Problema:** o pai exige que conteúdo devolvido pela CLI venha num campo marcado (`content`, `source`, `locator`) para a skill tratá-lo como dado, não instrução. `ReadResult` não tem forma decidida.
- **Correção:** herdar AD-9 e fixar `ReadResult = {doc_id, source, locator, content | toc[]}`; aplicar o mesmo a `get --raw` (`raw` + `source`).

#### M-8 — Forma do `GetResult` por kind/nível e semântica de "omitido"
- **Local:** AD-26, AD-32; `domain/services/levels.py`.
- **Problema:** `get` serve 9+ tipos em 3 níveis. Não está decidido se o `Result` é união discriminada por `kind`, se campos fora do nível são ausentes ou `null`, como "não preenchido" aparece no JSON (string? `null` + flag?), nem a forma de `omitted`. Isso define o schema, o NFR-1 (tokens) e os golden files. "`model_dump_json()` ordenado" também é ambíguo (ordem dos campos do modelo? chaves ordenadas?).
- **Correção:** regra: `GetResult = {item: <união discriminada por kind>, level, omitted: [{what, command}]}`; campos fora do nível ausentes (`exclude_none` proibido; usar `exclude_unset` com construção explícita); "não preenchido" = lista vazia + entrada em `unfilled[]`; JSON na ordem dos campos do modelo, sem `sort_keys`, `ensure_ascii=False`, indentação fixa.

#### M-9 — `skills install`: porta, recursos empacotados e detecção de versão/modificação
- **Local:** AD-28 ("só três portas"); `application/skills_install.py`; Epic 4 Story 4.5.
- **Problema:** `skills install` lê recursos do pacote e grava em `.claude/skills/` (projeto/usuário) ou `--path` — fora da raiz amarrada ao `CatalogFiles`. Nenhuma das três portas serve, e a própria AD-28 diz "porta nova exige nova AD". Também falta como saber "de qual versão para qual" e "modificadas localmente" (o pai AD-6 manda cabeçalho com hash em todo arquivo gerado).
- **Correção:** nova AD (ou ampliação da AD-28): porta `InstallTarget`/`FileSystem` sem raiz fixa + `PackagedResources`; manifesto `.sinter-skill.json` por skill instalada com versão e hash de cada arquivo; `--force` compara hashes.

#### M-10 — Avaliação de skills e `skills-ref` fora do `poe check` e do Stack
- **Local:** AD-34; Stack; Guia Receita 7.
- **Problema:** Stories 4.1/4.2 exigem `skills-ref validate` "como teste automatizado" e evals versionados. `skills-ref` não está no Stack; evals da skill-creator dependem de um LLM (não determinísticos, rede) — conflito com AD-34 rodar tudo em CI e com NFR-5.
- **Correção:** declarar: `skills-ref` (versão X) como dependência de dev e teste em `tests/skills/`; evals rodam **fora** do `poe check` (tarefa `poe evals`, manual/agendada), com resultado versionado; ou adiar explicitamente.

#### M-11 — AD-28 relaxa a letra do AD-8 e troca as portas do pai sem mapeamento
- **Local:** AD-28.
- **Problema:** o AD-8 do pai diz que cada porta troca **só modelos de `core/schemas`** e nomeia `CatalogStore` (o AD-3 do pai cita `CatalogStore.write`). A AD-28 troca por `CatalogFiles` + `ManifestCodec` que trafegam `str`/`dict` + posições. É razoável (o codec precisa ser genérico), mas é um desvio não declarado. `ManifestCodec.edit(texto, operação)` tem `operação` sem tipo — cada uso vai inventar uma.
- **Correção:** declarar na AD-28 "refina o AD-8: `CatalogStore` = `CatalogFiles` + `ManifestCodec`; `dict` de dados brutos é aceito só entre `ManifestCodec` e `load`" e atualizar o pai. Definir `operação` (ex.: `InsertInList(path, index, value)`, `SetValue(path, value)`) em `domain` ou remover `edit` se `new subdomain` puder gerar o domínio por `get --raw` + reescrita.

#### M-12 — Granularidade de caso de uso para subcomandos (`list`, `get --raw`, `schema export`)
- **Local:** AD-26 ("cada comando tem um caso de uso"); Seed (`application/list.py`); Guia Receita 1 (`list_areas.py`).
- **Problema:** o Seed tem um `list.py`; o guia cria `list_areas.py`. `get --level` e `get --raw` são o mesmo comando com resultados de formas diferentes. "Comando" não está definido (comando Typer? subcomando? flag?).
- **Correção:** regra: um caso de uso por **subcomando folha** (`list_domains`, `list_areas`, `catalog_init`, `schema_export`); `get --raw` é caso de uso próprio (`get_raw`). Corrigir o Seed.

#### M-13 — Normalização de texto e parser de Markdown sem lugar único
- **Local:** `domain/services/`.
- **Problema:** três histórias comparam texto "sem maiúsculas e acentos" (find — 2.5; glossário — 1.5; âncora estilo GitHub — 2.4). Sem um lugar único, as três divergem (NFC vs NFD, `ç`, hífens). O corte de seção do `read` não tem módulo no Seed.
- **Correção:** `domain/services/text.py` (`normalize`, `slugify_anchor`) como único lugar, e `domain/services/markdown.py` para seções/TOC; acrescentar à convenção "Tokens, normalização, âncora: só …".

### Baixa

- **L-1 — `binds` incompleto.** Frontmatter não lista AD-19 (a tabela lista), nem AD-2 (schemaVersion/NFR-6), AD-5 (evidência validada na 1.5), AD-9, AD-10 (citado na AD-28), AD-13, AD-15 (trailers usados no `commit`). Correção: completar e acrescentar linhas na tabela de herdados.
- **L-2 — Onde vive o teste de `schemaVersion`.** NFR-6/AD-2: recusar catálogo mais novo (validate → `1`) e recusar escrita. Não está dito se é no `load` ou em cada caso de uso. Correção: no `load`, com código `CATALOG_VERSION_UNSUPPORTED`. `sinter migrate` (citado no guia Receita 3) fica em Deferred.
- **L-3 — Contagem de tokens (NFR-1).** A convenção do pai diz "tokens só por `core/context.count_tokens`"; a espinha não aponta módulo. Correção: `domain/services/tokens.py` com heurística fixa (ex.: chars/4) usada pelo teste da Story 2.1.
- **L-4 — Exemplo de código de erro.** O pai usa `ENTITY_NOT_FOUND`, a espinha `ITEM_NOT_FOUND`. Escolher um e corrigir o outro.
- **L-5 — Pasta do domínio.** Pai AD-2: `domains/<id-domínio em minúsculas>/`; FR-18 e Story 1.2: `domains/<id-domínio>/` batendo com `domainId` (maiúsculo). A espinha poderia fixar (função `canonical_path` em `domain/model/catalog.py`) e apontar a divergência ao pai.
- **L-6 — Guia: adaptador `memory` para toda porta.** Receita 6 manda criar versão `memory` de toda porta nova, mas o Seed não tem `ManifestCodec` em memória (os testes usam o codec real). Dizer que portas puras dispensam versão em memória.
- **L-7 — Logs.** A convenção do pai (JSON lines em `~/.sinter/logs`) não é decidida nem adiada para o passo 1; AD-32 só proíbe logging de conteúdo. Dizer "sem logs no passo 1" ou onde ficam.
- **L-8 — Marcação `[ADOPTED]`.** AD-25..AD-27 marcadas, AD-28..AD-34 não; esclarecer o significado ou uniformizar.
- **L-9 — Fixture do exemplo.** O pai diz que `docs/.../exemplo-catalogo/` "vira fixture"; a espinha diz "cópia". Fixar se é cópia (e teste que detecta deriva) ou link/geração.
- **L-10 — Guia: "Escrever na tela" só em `render/`.** AD-33 põe o envelope de erro em `cli/errors.py`. Ajustar a tabela do guia para `adapters/inbound/cli/` (render + errors).

## Itens adiados — verificação

Os seis itens de Deferred foram conferidos: servidor HTTP, `SecretScanner`, push/rebase/`people.yaml`, cache, plugins de regras e `new` interativo. Nenhum permite que duas histórias do passo 1 divirjam. Faltam itens que deveriam estar lá se não forem decididos: `sinter migrate`, Windows, publicação do pacote, logs, `sinter doctor` (citado no pai).

## Prioridade sugerida

1. H-1, H-3, H-5 (contratos e ACs literais que a Story 1.1 já vai bater).
2. H-2, H-7 (escrita e raiz do catálogo — afetam todo o Epic 3).
3. H-4, H-6 (envelope operacional e enforcement — necessário antes do primeiro PR com CI).
4. M-1..M-5 antes do Epic 3; M-6..M-8, M-13 antes do Epic 2; M-9, M-10 antes do Epic 4.
