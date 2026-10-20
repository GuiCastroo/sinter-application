---
title: 'Revisão adversarial — espinha do código da fatia 1'
target: ../ARCHITECTURE-SPINE.md
companions_lidos: [../GUIA-EXTENSAO.md, ../../architecture-harness_corp-2026-09-26/ARCHITECTURE-SPINE.md, ../../../../../docs/prd-dominio-2026-10-17/epics.md, ../../../../../docs/prd-dominio-2026-10-17/prd.md (FR-18), exemplo-catalogo]
date: '2026-10-20'
method: 'pares de unidades um nível abaixo (histórias/devs) que obedecem a todas as ADs ao pé da letra e ainda assim constroem peças incompatíveis'
---

# Revisão adversarial — Sinter, código da fatia 1

## Veredito

A espinha acerta a **forma** do hexágono (camadas, composição, portas, registro de regras), mas deixa sem dono os **dados compartilhados** que atravessam comandos: forma do `Finding` e do `path`, forma do nível 0, casing das chaves do `--json`, mapa kind → pasta, modelos de rascunho, e a fronteira entre "finding" e "erro". Ela também **contradiz o parent e as histórias** em três pontos verificáveis (quem grava no catálogo, código de saída de "não é catálogo", e a estrutura `core/` + `sinter.cli:app` citada na Story 1.1). Dois devs seguindo cada AD ao pé da letra vão produzir golden files diferentes e `--json` incompatíveis já no Epic 1→2. **Não está pronta para fatiar em histórias paralelas**; faltam umas 10 regras curtas (propostas abaixo, AD-35..AD-46).

Severidade: **Crítica** = quebra contrato `--json`/schema ou contradiz AD herdada; **Alta** = golden files ou comportamento divergem entre histórias; **Média** = retrabalho localizado; **Baixa** = ambiguidade que um teste pega cedo.

---

## Resumo dos buracos

| # | Buraco | Pares em choque | Severidade | AD proposta |
|---|---|---|---|---|
| H1 | Forma do resultado de `validate`/`apply`: `findings[]` (AD-31/33) vs `errors[]`+`warnings[]` (Story 1.1, 3.2) | 1.1 × 3.2 × skills 4.3 | Crítica | AD-35 |
| H2 | Formato do `Finding.path` e do `file` (ponto vs JSON Pointer vs índice vs id; rascunho de stdin) | 1.x × 3.2 × guia (Receita 2) | Crítica | AD-35 |
| H3 | "Só o `apply` grava" vs `fmt`, `init`, `skills install`, `schema export`, criação de `docs/` | 3.7 × 3.1 × 4.5 × 1.6 × parent AD-3 | Crítica | AD-36 |
| H4 | Código de saída de "não é catálogo" e de outros casos (AD-33 diz 1, Story 1.1 diz 2) | 1.1 × 3.1 × AD-33 | Crítica | AD-37 |
| H5 | Casing e ordem de chaves do `--json` (snake_case Python vs camelCase do YAML; "ordenado") | 2.1 × 2.5 × 1.6 × golden | Crítica | AD-38 |
| H6 | Dono da forma do nível 0 (find, list, get area, filhos no nível 1, passo de jornada) | 2.1 × 2.3 × 2.5 | Alta | AD-39 |
| H7 | Dono do mapa kind → pasta e do caminho canônico; caixa da pasta (`camb` vs `CAMB`) | 1.2 × 3.3 × 3.4 × 3.5 × guia Receita 4 | Alta | AD-40 |
| H8 | Índice global do `Catalog` colide com ids locais (passos/etapas de jornada) e com itens sem arquivo (área) | AD-29 × 1.4 × 2.5 | Alta | AD-41 |
| H9 | Dono dos modelos de rascunho do `new` (domain? package data? `skills/.../assets/`?) e destino dos comentários do modelo | 3.4 × 3.5 × 4.2 × guia Receita 4 | Alta | AD-42 |
| H10 | `new subdomain` edita o domínio por `ManifestCodec.edit` (operação sem vocabulário) vs `apply` formatando o texto do rascunho; rascunho multi-documento sem operação na porta | 3.5 × 3.2/3.3 × AD-28 | Alta | AD-43 |
| H11 | `<obrigatório>` e `FILE_NOT_FORMATTED` não cabem no motor `(Catalog) -> Finding` da fase 2; `validate` e `apply --dry-run` divergem | 3.2 × 3.7 × AD-31 | Alta | AD-35, AD-44 |
| H12 | Texto em linguagem natural: domínio produz "não preenchido" no `Result` ou a CLI renderiza a partir de `[]`? | AD-32 × 2.1 × 3.2 × render | Alta | AD-45 |
| H13 | Semântica de "sem mudança" (dados vs texto; mudança só de comentário) e de troca de id | 3.3 × 3.7 × 3.6 | Média | AD-44 |
| H14 | `nextAdrNumber`: o `apply` incrementa (parent AD-14) ou o rascunho incrementa e o dry-run avisa (Story 3.6)? | 3.6 × parent AD-14 | Média | AD-44 |
| H15 | Normalização de texto em três lugares (slug de id no `new`, busca sem acento no `find`, âncora GitHub no `read`) | 3.5 × 2.5 × 2.4 | Média | AD-46 |
| H16 | `catalog_root` em dois lugares (Request do guia vs `bootstrap.build(catalog_root)`) | guia Receita 1 × AD-27 | Média | AD-27 (aperto) |
| H17 | Relógio, versão e data: `Sinter-Version`, `asOf` = data do commit, sem operação em `VersionControl` | 3.3 × 2.x × parent AD-6/AD-20 | Média | AD-28 (aperto) |
| H18 | Atomicidade do `apply` multi-arquivo; `dirty` só dos arquivos do rascunho | 3.3 × AD-28 | Média | AD-44 |
| H19 | `ManifestCodec.format(texto)` sem `kind`: o adaptador precisa de um segundo registro kind → modelo | AD-30 × AD-40 | Média | AD-40 |
| H20 | Story 1.1 manda `sinter.cli:app` e `core/`; Additional Requirements pinam Pydantic 2.13 / Typer 0.26 | 1.1 × AD-25 × Stack | Baixa (mas trava a 1ª história) | errata nas histórias |

---

## Buracos em detalhe

### H1 — Duas formas para o mesmo resultado de validação [Crítica]

**Par:** Dev A (Story 1.1) lê o AC "`--json` com `errors[]` e `warnings[]`, cada item com `file`, `path`, `code` e `message`" e cria `ValidateResult{errors: list[Finding], warnings: list[Finding]}`. Dev B (Story 3.2) lê AD-31 ("`Finding = {code, severity, file, path, message}`") e AD-33 ("`findings` no `Result`") e cria `ApplyResult{items, findings: list[Finding]}` — ou segue o AC da 3.2 (`{items, errors, warnings}`) mas com `severity` dentro de cada item, redundante.

**Ambos obedecem:** AD-31 só define `Finding`, não a coleção; AD-33 diz "findings no Result" sem nome nem forma.

**Quebra:** a skill `sinter-domain` (4.3) precisa ler o mesmo campo do `validate` e do `apply --dry-run`; Story 3.3 exige "resultado é o mesmo da conferência"; `schemas/` passa a ter dois tipos para a mesma ideia. A regra de saída `1` ("se houver `error`") é calculada em dois lugares diferentes.

**Proposta (AD-35, parte 1):** existe um único bloco `Report` em `ports/inbound/common.py`: `{errors: list[Finding], warnings: list[Finding]}` (atende às histórias), e todo `Result` que valida o embute com o mesmo nome (`ValidateResult.report`, `ApplyResult.report`) — ou, se preferir `findings[]` plano, **errata nas Stories 1.1 e 3.2**. `Finding.severity` continua no item. O código de saída derivado de `report.errors` é calculado por **uma** função (ver AD-37).

### H2 — `Finding.path` e `Finding.file` sem formato [Crítica]

**Par:** Dev A (regra de aplicações) emite `path="spec.applications[2].lifecycle"`. Dev B (regra de sumário) emite `path="/spec/subdomains/3"` (JSON Pointer, natural para quem converte erro do Pydantic, que dá `loc=('spec','subdomains',3)`). Dev C segue a Receita 2 do guia: `Finding.at(sub, "spec.applications", …)` sem índice. Dev D prefere por id (`spec.applications[app-camb-carteira]`), estável a reordenação.

**Ambos obedecem:** AD-31 diz só `path`. A ordem "arquivo, path, code" vira ordenação de string, e `[10]` < `[2]` — o golden muda quando o exemplo cresce.

**Casos sem resposta:**
- Rascunho lido de `-` (stdin) no `apply --dry-run`: `file` é `-`, `<stdin>#2` (índice do documento) ou o caminho canônico que o item **vai** ter? Story 3.2 pede "o manifesto e o campo".
- Duplicata entre dois arquivos (Story 1.2/1.3: "citando os dois arquivos"): um `Finding` com `file` único não cita dois. Dois findings (um por arquivo)? Um com `details.other_file`?
- `file` absoluto ou relativo à raiz? Absoluto quebra o golden em toda máquina.
- Posição em linha/coluna: o codec devolve posições (AD-28), mas o `Finding` não as tem — o editor do usuário não consegue pular para o erro.

**Proposta (AD-35, parte 2):** `Finding = {code, severity, file, path, message, line?, related?: [{file, path}]}`. `file` = caminho POSIX **relativo à raiz do catálogo**; para rascunho, `file` = caminho canônico de destino e `source = "draft#<n>"` (índice 1-based do documento). `path` = segmentos separados por `.` com **chave do item de lista por id quando o item tem id** (`spec.applications[app-camb-carteira].lifecycle`) e índice 0-based só quando não tem. Construído **só** por `Finding.at(item, *segments)` em `domain/validation/finding.py`; ninguém monta string de path à mão. Ordem: `file`, `line`, `path` (comparado por segmentos, índice numérico), `code`, `message`. Duplicata = um finding no arquivo que vem depois na ordem, com `related` apontando o primeiro.

### H3 — Quem grava no catálogo (e fora dele) [Crítica]

**Pares:**
- Dev da Story 3.7 (`fmt`) implementa `application/fmt.py` chamando `CatalogFiles.write`. O guia diz "Ninguém grava no catálogo fora de `application/apply.py`" e "o `poe check` pega todas"; parent AD-3: "Nenhum outro módulo chama `CatalogStore.write`". Dev do `poe check` escreve o contrato que proíbe `CatalogFiles.write` fora de `apply` → o `fmt` não compila no CI.
- Dev da Story 3.1 (`init`) grava `organization.yaml`, `repositories.yaml` e faz `git init` + commit — também fora do `apply`.
- Dev do `apply` (3.4) precisa **criar a pasta `docs/`**; `CatalogFiles` não tem `mkdir`, e o Git não versiona pasta vazia. Um dev grava `.gitkeep`, outro não cria nada (e o próximo clone não tem `docs/`), o `init` faz o mesmo com `domains/`, `regulations/`, `standards/`.
- Dev da Story 4.5 (`skills install`) e da 1.6 (`schema export`) precisam ler **recursos do pacote** e gravar **fora da raiz do catálogo** (`.claude/skills/`, `~/.claude/skills`, `schemas/`). A única porta de arquivo é `CatalogFiles`, presa a `catalog_root`; AD-28 proíbe porta nova sem AD. Resultado previsível: `pathlib`/`importlib.resources` direto em `application/` (viola parent AD-1) ou `CatalogFiles` instanciado com outra raiz pelo bootstrap (vira porta genérica de disco, sem regra).

**Proposta (AD-36):** "Gravar no **conteúdo** do catálogo (manifestos e `docs/`) só por `apply`. Exceções nomeadas e fechadas: `init` (cria o esqueleto, só em pasta vazia, commit `Sinter-Action: init`) e `fmt` (só reescreve com `ManifestCodec.format`, nunca muda dados — verificado por `parse(antes) == parse(depois)` — e não comita). O contrato do `poe check` lista exatamente `apply`, `init`, `fmt` como chamadores de `CatalogFiles.write`. Pastas vazias levam `.gitkeep`; `CatalogFiles.write` cria pais. Para fora do catálogo existe uma quarta porta, `InstallTarget` (ou `PackageResources` + `LocalFiles`), usada só por `skills_install` e `schema_export`." Isso também precisa de uma errata no parent AD-3 (que hoje proíbe o `fmt` e o `init`).

### H4 — Código de saída: AD-33 contra as histórias [Crítica]

**Par:** Dev A (AD-33) faz `NOT_A_CATALOG` → `1`. Dev B (Story 1.1: "pasta que não é catálogo … o código de saída é `2`"; Story 3.1: "pasta não vazia que não é catálogo → `2`") faz `2`. Os dois obedecem a um documento vinculante.

**Outros casos sem dono:**
- `schemaVersion` maior que o suportado (Story 1.1 → `1`): finding (`SCHEMA_VERSION_UNSUPPORTED` em `errors[]`) ou `SinterError`? Muda a forma do `--json` (Result vs envelope).
- Arquivo sujo no `apply` (3.3 → `1`): finding ou erro? Catálogo fora de repo Git no `apply`: `1` ou `2`?
- `new domain` com `--domain-id` repetido (3.4, "erro já no `new`"): finding ou `SinterError`?
- `fmt --check` com arquivos fora do formato → `1` (3.7), mas no `validate` o mesmo fato é **aviso** e AD-33 só dá `1` "se houver `error`".
- `init` repetido → aviso e `0`: onde fica o aviso, se o `InitResult` não tem `warnings`?
- Erro de parse do Typer (opção inválida) sai com `2` e mensagem do Click, **sem envelope** `--json`, sem passar por `cli/errors.py`.
- Parent usa `ENTITY_NOT_FOUND`; esta espinha usa `ITEM_NOT_FOUND`. Skill escrita pelo exemplo do parent nunca casa.
- O envelope de erro (`details`) não tem schema: viola AD-12 ("`--json` segue o schema").

**Proposta (AD-37):** tabela fechada em `domain/errors.py`: cada `code` com `exit` e modelo de `details` (Pydantic, entra em `schemas/error.schema.json`). Regras: (a) **pré-condição de ambiente** (não é catálogo, pasta não vazia, não é repo Git, versão maior) = `SinterError` com `exit 2` — errata em AD-33 *ou* nas Stories 1.1/3.1, mas uma das duas; (b) **estado do catálogo/rascunho** = finding; (c) `exit` de um `Result` é uma função única `exit_code(result)` em `adapters/inbound/cli/errors.py`, e todo `Result` que pode falhar sem exceção tem `report` (H1) — `fmt --check` emite `FILE_NOT_FORMATTED` com severidade `error` nesse comando; (d) `ITEM_NOT_FOUND` é o nome (errata no parent); (e) o Typer roda com `standalone_mode=False` e erros de uso viram `USAGE_*` no envelope; (f) envelope em **stdout** quando `--json`, texto em **stderr** sem `--json`.

### H5 — Casing e ordem das chaves no `--json` [Crítica]

**Par:** Dev A (modelos, Epic 1) escreve `domain_id: str = Field(alias="domainId")` (PEP 8 + mypy strict). Dev B (Story 2.1) faz `result.model_dump_json()` como AD-32 manda — sai `domain_id`. Dev C (Story 3.6) faz `model_dump(by_alias=True)` para devolver YAML — sai `domainId`. A skill lê `domainId` do `get --raw` e `domain_id` do `get --json`. O `schema export` (1.6) gera o schema com `by_alias` ou não, e o `tests/contract` passa nos dois casos. Também "`--json` = `model_dump_json()` **ordenado**": ordenado por quê? Pydantic preserva a ordem dos campos e não ordena; um dev adiciona `sort_keys` via `json.dumps`, outro não, e os golden files divergem.

**Proposta (AD-38):** todos os modelos (`domain/model` e `ports/inbound`) herdam de `SinterModel` com `alias_generator=to_camel`, `populate_by_name=True`, `extra="forbid"`; **toda** serialização (JSON, YAML, schema) usa `by_alias=True` — uma função `to_json(result)` só, em `adapters/inbound/cli/render/json.py`. Ordem das chaves = ordem dos campos do modelo (não alfabética); a ordem das **listas** é responsabilidade do domínio (AD-6). `None` é emitido como `null` (nunca omitido), para o schema ser estável.

### H6 — Sem dono para a forma do nível 0 [Alta]

**Par:** Dev A (Story 2.1) define `Level0` em `ports/inbound/get.py` (id, name, kind, domainId, area, purpose, counts). Dev B (Story 2.5, `find`) precisa de "cada um no nível 0 com o campo onde casou" e define `FindHit` em `ports/inbound/find.py`, com `type` em vez de `kind` e sem `counts` (porque contar sai caro na busca). Dev C (Story 2.3) precisa do "subdomínio (nível 0)" dentro de cada passo da jornada; Dev D (`list domains`) e `get area-` de novo. AD-26 diz que `Request/Result` vivem em `ports/inbound/<verbo>.py`, mas não diz onde vivem os **tipos compartilhados** nem se `ports/inbound/find.py` pode importar de `ports/inbound/get.py`. AD-25 põe "consulta por nível" em `domain/services/levels.py`, mas o modelo de saída é de `ports/inbound` — dois donos.

Também falta: o que é "contagens" por `kind` (domínio: subdomínios/aplicações/jornadas; aplicação: repos?; área: domínios?), a forma do `omitted` (lista de `{field, command}` ou uma frase), e como o herdado é marcado (`inheritedFrom: id` em cada item, ou wrapper `{item, origin}`).

**Proposta (AD-39):** as **visões** (`Level0`, `Level1<Kind>`, `Level2<Kind>`, `Inherited[T] = {value: T, origin: id}`, `Omitted = {field, command}`) são modelos de **domínio** em `domain/model/views.py`, produzidos só por `domain/services/levels.py`. `ports/inbound/*` os **reusam**, nunca redefinem. `Level0` é uma união discriminada por `kind`, com `counts: dict[str, int]` de chaves fixas por kind (tabela no próprio módulo). `find`, `list`, `get area`, filhos e passos usam o mesmo `Level0`.

### H7 — Mapa kind → pasta sem dono e caixa da pasta [Alta]

**Par:** o guia (Receita 4) põe o mapa em `domain/model/catalog.py`. O dev do `apply` (3.3) precisa dele para gravar; o do `new` (3.4/3.5) para dizer "id já existe"; o do `validate` (1.2/1.3: "subdomínio fora da pasta do seu domínio", "pasta não bate com o `domainId`") para conferir; o do `load` (AD-29) para descobrir o `kind` pelo caminho ou pelo conteúdo. Cada um tem motivo para reimplementar ali mesmo. E a caixa: parent AD-2 diz `domains/<id-domínio em minúsculas>/`; o exemplo usa `domains/camb/` com `domainId: CAMB`; Story 1.2 diz "pasta cujo nome não bate com o `domainId`" (comparação literal falha no exemplo); Story 3.4 diz `domains/<id-domínio>/domain.yaml`. Dev do validate compara `==` e o exemplo-catalogo deixa de ter zero erros; dev do apply grava `domains/CAMB/` e cria um segundo domínio no macOS (sistema de arquivos sem distinção de caixa) ou no Linux (com).

Também: `apply` de um rascunho cujo `metadata.domain` mudou (mover subdomínio) ou cujo `id` mudou grava num caminho novo e deixa o antigo — dois arquivos, `DUPLICATE_ID` no próximo `validate`. A espinha não diz se `apply` move, recusa ou deixa.

**Proposta (AD-40):** `domain/model/registry.py` é o **único** lugar com `KIND → (modelo, prefixo, função canonical_path(item))`; `canonical_path` usa `domainId.lower()`. Comparação de pasta = `lower()`. `load`, `validate`, `new`, `apply` e o `ManifestCodec` (para a ordem das chaves, H19) leem esse registro. `apply` recusa (finding `APPLY_ID_CHANGED` / `APPLY_PATH_CHANGED`) rascunho que muda `id` ou caminho de um item existente; renomear/mover fica para um comando futuro.

### H8 — Índice global de ids colide com ids locais [Alta]

AD-29: o `Catalog` "indexa cada id (inclusive aplicações, dados, regras, ADRs e **passos**)". No exemplo, passos e etapas têm ids curtos e locais à jornada (`cotar`, `cotacao`, `limite`, `cliente`, `boletar`…), e Story 1.4 só exige unicidade **dentro da jornada**. Dev A (Catalog) faz `dict[str, Entry]` global e o segundo `cliente` sobrescreve o primeiro (ou dispara `DUPLICATE_ID` em catálogo válido). Dev B (regras de jornada) supõe índice local. Também: `area-*` não tem arquivo nem `kind` (vive em `organization.yaml`), mas `get area-cambio` e `find` precisam dele no índice; `doc-*` aparece definido num nível e "reaproveitado por id" em outros — qual ocorrência o índice guarda?

**Proposta (AD-41):** o índice global guarda só ids **globais** (prefixos do Apêndice A.8, incluindo `area-` como pseudo-kind `Area` com `file = organization.yaml`); passos e etapas são indexados por `(jor-id, step-id)`. A "posição" do índice é `{file, path, line}` — o mesmo `path` de AD-35 —, não um número solto. Doc reaproveitado: o índice aponta a **definição**; as referências ficam numa lista `refs` separada.

### H9 — Dois donos para os modelos de rascunho [Alta]

**Par:** Dev A (Story 3.4) precisa de um rascunho com "obrigatórios marcados `<obrigatório>` e opcionais **comentados** com uma linha de explicação". Comentário YAML só sai de texto (ou de ruamel), então ele não pode gerar no `domain` a partir do modelo; põe modelos `.yaml` como *package data* em `adapters/outbound/yaml_fs/templates/` (mas a aplicação não pode lê-los: `CatalogFiles` é do catálogo). Dev B põe strings de modelo em `domain/drafts/` (domínio puro, sem I/O, ok, mas fora das pastas permitidas por AD-25). Dev C (Story 4.2) cria `skills/sinter-domain/assets/` com **os mesmos** modelos para a skill montar o rascunho sem o `new` — duas cópias que divergem no primeiro campo novo. O guia (Receita 4) diz só "crie o modelo de rascunho".

Consequência extra: o `apply` grava "o texto formatado" do rascunho (AD-30) com comentários preservados — então **as linhas de explicação e os blocos opcionais comentados do modelo vão parar no catálogo** para sempre. Um dev remove comentários de modelo antes de gravar, outro não; o diff do PR fica poluído exatamente como AD-30 queria evitar.

**Proposta (AD-42):** modelos de rascunho são função pura `domain/drafts/<kind>.py → str`, a partir do modelo e do registro (AD-40); são a **única** fonte — a skill obtém o modelo por `sinter new <kind> --json` (campo `draft`), e `skills/*/assets/` não contém manifestos. Comentários de modelo começam com `#~` e são removidos pelo `apply` (e acusados como aviso `DRAFT_TEMPLATE_COMMENT` no dry-run); comentários do usuário ficam.

### H10 — `new subdomain` e `apply` editam o mesmo texto por caminhos diferentes [Alta]

**Par:** Dev A (Story 3.5) gera o domínio "inteiro com `sub-camb-hedge` inserido no sumário na posição pedida", preservando comentários, via `ManifestCodec.edit(texto, operação)`. A "operação" não tem tipo nem vocabulário; Dev A inventa `InsertInList(path, after, value)` em `ports/outbound`. Dev B (Story 4.4, aplicação nova num subdomínio) precisa de "acrescentar sem mexer no resto" — mas a skill só pode chamar a CLI, então ou a skill edita YAML de cabeça (perdendo comentários) ou alguém inventa `sinter new application`/`sinter edit`. Dev C (`apply`) recebe o texto multi-documento: a porta tem `texto → dict + posições`, mas **não tem** operação para separar documentos preservando o texto de cada um (que é o que `format` e `write` precisam). Dev C passa a re-serializar `dict → texto`, e os comentários morrem (contra Story 3.3 / NFR-4).

**Proposta (AD-43):** `ManifestCodec` ganha `split(texto) -> list[ManifestText]` (texto + dados + posições por documento) e `edit` recebe um tipo fechado `domain/model/edits.py: Edit = InsertListItem | ReplaceField | RemoveListItem` com `path` no formato de AD-35. `new subdomain` usa `edit`; `apply` usa `split` → `format` por documento; nenhum caso de uso faz `dict → texto` de um arquivo que já existe. Se a 4.4 precisar de inserção sem LLM, ela vira subcomando (`new application --subdomain …`) que usa o mesmo `edit`.

### H11 — Checagens que não cabem no motor de regras [Alta]

AD-31: fase 2 = funções puras `(Catalog) -> Findings`, "só sobre itens que passaram na fase 1"; `validate` e `apply --dry-run` chamam **o mesmo** `validate_catalog(catalog)`.

- **`<obrigatório>`** (Story 3.2: "cada marca é um erro"): num campo `str` a marca passa no schema; num enum (`lifecycle`) ou id com padrão, falha na fase 1 como erro genérico do Pydantic. Dev A cria regra `DRAFT_REQUIRED_MARK` na fase 2 (não vê os campos de enum); Dev B faz varredura de texto no `apply` antes do parse (fora do motor, então o `validate` de um arquivo editado à mão com a marca não acusa).
- **`FILE_NOT_FORMATTED`** (AD-30, Story 3.7): exige `ManifestCodec.format`, que não está no `Catalog`. Dev do `validate` coloca a checagem em `application/validate.py`, fora de `validate_catalog` → `apply --dry-run` não a emite, e Story 3.3 ("validate dá o mesmo da conferência") falha. Dev do `load` grava `formatted: bool` no `Catalog` → aí o rascunho do `apply`, ainda não formatado, sempre acusa.
- **Regras de conjunto** (sumário bate, unicidade) com um subdomínio que falhou no schema: ele some do conjunto e o sumário acusa "falta" — um erro vira dois, e o golden depende de qual dev filtrou.

**Proposta (AD-35, parte 3):** `validate_catalog(catalog, *, files: FileFacts)` recebe fatos de arquivo calculados pela aplicação com a mesma função nos dois caminhos (`formatted`, `has_required_marks`); para o rascunho, `formatted` é calculado **depois** de formatar (então nunca acusa). A marca `<obrigatório>` vira valor sentinela reconhecido antes do schema (`REQUIRED_MARK` com `path` exato) e substituído por `None` para não gerar erro duplo. Itens que falham na fase 1 continuam no índice com `valid=False`, e regras de conjunto os contam como presentes.

### H12 — Quem escreve "não preenchido" e o resumo [Alta]

AD-32: "textos que são regra (resumo do `apply`, 'não preenchido', 'herdado de…') são produzidos no `domain` e só impressos pela CLI". Dev A (get, 2.1) segue à letra e põe `does: "não preenchido"` (string no lugar da lista) no `Result` → o tipo do campo vira `list[str] | str`, e a skill (4.2), que precisa ler "lacunas do 'não preenchido' do `get --level 1`", tem de casar texto em português. Dev B põe `does: []` e deixa o `render/get.py` escrever "não preenchido" → viola AD-32, mas o JSON fica limpo. O mesmo com o resumo: Story 3.2 pede `summary` (texto) **e** `changes` (estrutura) — se o render montar o texto a partir de `changes`, `--json` e texto divergem.

**Proposta (AD-45):** no `Result` os fatos são **estruturados** (`does: []`, `gaps: [{field, level}]`, `changes: [{path, before, after}]`, `inheritedFrom`); o **texto em linguagem natural** é um campo `summary: str` produzido por `domain/services/summary.py` e o render imprime `summary` sem recompor. "Não preenchido" é a palavra que `summary`/render mostram para `gaps`; nunca substitui o valor do campo. A skill lê `gaps`, nunca o texto.

### H13 — "Sem mudança" e a ação de cada item [Média]

Story 3.3: nada mudou → sem commit; Story 3.7: diferença só de formato não é mudança; Story 3.3: comentários preservados. Dev A (diff) compara **dados** → uma mudança só de comentário (o usuário corrige um comentário pelo `get --raw`) vira "sem mudança" e é descartada em silêncio. Dev B compara **texto formatado** → coerente com a 3.7, mas `changes` campo a campo fica vazio com ação "altera". Também falta a ação para um rascunho que repete um item **igual** de outro arquivo (duplicata) e para "cria" quando o arquivo existe mas está fora do caminho canônico.

**Proposta (AD-44, parte 1):** ação = `create` se o id não está no índice; `unchanged` se `format(rascunho) == texto atual`; senão `update`, com `changes` vindo do diff de **dados** e `commentsChanged: bool`. `unchanged` em todos os itens → sem commit.

### H14 — `nextAdrNumber`: quem incrementa [Média]

Parent AD-14: números de ADR vêm de `nextAdrNumber`, "incrementados no commit que cria o item" (leitura natural: o `apply` incrementa). Story 3.6: "deve ser incrementado **no mesmo rascunho** (o `dry-run` avisa se não foi)". Dev do `apply` incrementa automaticamente (e o rascunho que já incrementou é incrementado duas vezes); dev da regra emite o aviso. Contradição entre documentos vinculantes.

**Proposta (AD-44, parte 2):** o `apply` **nunca** altera o rascunho; o contador é dado escrito pelo autor; regra `ADR_COUNTER_NOT_ADVANCED` (aviso) quando `max(NNN) >= nextAdrNumber`. Errata no parent AD-14 ("incrementado no rascunho que cria o item").

### H15 — Três normalizadores de texto [Média]

`new subdomain --name "Liquidação à vista"` → slug do id (3.5); `find cambio` casa "Câmbio" (2.5); `read doc#decisoes` âncora "estilo GitHub, sem acento" (2.4); glossário "sem maiúsculas e acentos, incluindo sinônimos" (1.5). Quatro devs, quatro funções com `unicodedata` ligeiramente diferentes (NFD vs NFKD, `ç`, hífens duplos, emoji). A âncora do GitHub **mantém** hífens múltiplos e remove pontuação de um jeito específico; o slug de id não pode ter hífen duplo (o `--` é separador de relação, AD-19).

**Proposta (AD-46):** `domain/services/text.py` com três funções nomeadas e testadas por tabela: `fold(s)` (comparação: casefold + sem acento), `slug(s)` (ids: `[a-z0-9]+(-[a-z0-9]+)*`, sem `--`), `gh_anchor(s)` (âncora GitHub). Ninguém mais importa `unicodedata`.

### H16 — `catalog_root` em dois lugares [Média]

O guia (Receita 1) põe `catalog_root: Path` no `Request`; AD-27 põe em `bootstrap.build(catalog_root)`. Dev A ignora o do Request (usa a porta já presa à raiz); Dev B usa o do Request para abrir caminhos → com o `memory` não há caminho real; o servidor da fatia 2 recebe pedidos para catálogos diferentes num mesmo `Container`. `catalog_root` como `Path` no Result ainda vaza caminho absoluto para o golden.

**Aperto em AD-27:** a raiz é só do `Container`; `Request` nunca tem `catalog_root` (errata no guia); nenhum `Result` contém caminho absoluto.

### H17 — Relógio, data do commit e versão [Média]

Parent AD-6/AD-20: `asOf` = data do commit do catálogo, nunca o relógio. `VersionControl` (AD-28) não tem `head()`/`head_date()`. Dev A (2.x) precisa de `asOf`, não tem como obter, e lê `datetime.now()` na aplicação (AD-1 só proíbe no `domain`). Dev B (3.3) precisa de `Sinter-Version` e chama `importlib.metadata` dentro de `application/apply.py`. Golden de `get` muda por dia.

**Aperto em AD-28:** `VersionControl.head() -> CommitInfo{sha, date} | None`; `Container` recebe `sinter_version: str` e `clock` explícitos no `build`; `application` não importa `datetime.now`, `importlib.metadata` nem `os.environ` (contrato no `poe check`).

### H18 — `apply` multi-arquivo sem atomicidade [Média]

Story 3.3: "nada é gravado, nem em parte". O `apply` valida antes, mas a gravação de N arquivos com `CatalogFiles.write` pode falhar no meio (disco, permissão, `commit` recusado por hook). Dev A não trata; Dev B faz `git checkout -- paths` (operação que a porta não tem). `dirty(paths)` com o caminho canônico de um item **novo** (não rastreado) também não tem semântica definida.

**Proposta (AD-44, parte 3):** gravação em duas fases: `CatalogFiles.write_all(dict[path, text])` atômica por arquivo (tmp + rename) e, se o commit falhar, restauração do texto anterior (que o `apply` já leu). `dirty` considera também arquivos não rastreados no caminho de destino.

### H19 — `format(texto)` precisa saber o kind [Média]

AD-30: chaves "na ordem dos campos do modelo Pydantic". A assinatura `format(texto)` não recebe kind nem modelo; o adaptador `yaml_fs` lê `kind` do texto e precisa do mapa kind → modelo — um segundo registro dentro do adaptador, que diverge do de AD-40 (e da Receita 4, que só manda atualizar `catalog.py`). Também: "chaves desconhecidas, se houver, ao fim" contradiz Story 1.1 ("campo desconhecido → erro") só se o `fmt` aceitar arquivo inválido; a 3.7 fala de "manifesto válido".

**Proposta:** em AD-40, o adaptador importa `domain.model.registry` (permitido: adaptador importa `domain`) e não tem lista própria. `fmt` de arquivo que falha no schema: formata só o envelope e reporta o finding, sem recusar.

### H20 — Histórias contradizem a estrutura [Baixa, mas bloqueia a 1ª história]

Story 1.1 manda `[project.scripts] sinter = "sinter.cli:app"` e "estrutura `core/` + `adapters/` + `cli.py`"; a espinha manda `sinter.adapters.inbound.cli.app:main` e `domain/application/ports`. Additional Requirements fixa Pydantic 2.13 e Typer 0.26; a Stack fixa 2.14 e 0.27. Um dev que segue a história ao pé da letra falha no `lint-imports` de AD-34 no primeiro PR.

**Proposta:** errata nas histórias (a espinha é mais recente e mais específica) e uma linha na espinha: "Em conflito de nomes de pasta/pacote/versão, a espinha vence o texto das histórias."

---

## ADs propostas (texto pronto para colar)

- **AD-35 — Relatório e `Finding` únicos.** `Report{errors, warnings}` em `ports/inbound/common.py`, embutido em todo `Result` que valida. `Finding{code, severity, file, path, message, line?, source?, related?}`; `file` relativo POSIX; `path` em segmentos `.` com chave por id (`[app-x]`) e índice só sem id; construído só por `Finding.at`. Ordem: file, line, path (por segmentos), code, message. `validate_catalog(catalog, files)` recebe `FileFacts` calculados igual nos dois caminhos; marca `<obrigatório>` reconhecida antes do schema; itens inválidos ficam no índice com `valid=False`.
- **AD-36 — Quem grava em disco.** Conteúdo do catálogo: `apply`; exceções fechadas `init` e `fmt` (fmt só formata, nunca muda dados, não comita). Fora do catálogo: porta `InstallTarget`/`PackageResources`, só para `skills_install` e `schema_export`. `.gitkeep` em pasta vazia. Contrato no `poe check`. Errata no parent AD-3.
- **AD-37 — Tabela de erros.** Cada `code` com `exit` e modelo de `details` em `domain/errors.py`, publicados em `schemas/`. Ambiente = `SinterError` exit 2; estado = finding; `exit_code(result)` único; Typer sem `standalone_mode`; envelope em stdout com `--json`. Nome `ITEM_NOT_FOUND` (errata no parent).
- **AD-38 — Serialização única.** `SinterModel` com camelCase por alias, `extra="forbid"`; toda saída `by_alias=True` por `to_json`; ordem de chaves = ordem dos campos; `null` explícito.
- **AD-39 — Visões por nível são do domínio.** `domain/model/views.py` (Level0 discriminado por kind, `Inherited[T]`, `Omitted`), produzidas só por `levels.py`, reusadas por todo `ports/inbound`.
- **AD-40 — Registro de kinds.** `domain/model/registry.py`: kind → modelo, prefixo, `canonical_path` (pasta em minúsculas). Lido por load, validate, new, apply e `ManifestCodec`. `apply` recusa troca de id ou caminho.
- **AD-41 — Escopo dos ids no índice.** Global só para prefixos do A.8 (+ `Area` pseudo-kind); passos/etapas por `(jornada, id)`; posição = `{file, path, line}`; doc reaproveitado aponta a definição.
- **AD-42 — Modelos de rascunho.** `domain/drafts/<kind>.py` é a única fonte; skills pegam por `sinter new --json`; comentários de modelo `#~` removidos pelo `apply`.
- **AD-43 — Edição de texto.** `ManifestCodec.split` e `edit(texto, Edit)` com `Edit` fechado em `domain/model/edits.py`; nenhum caso de uso re-serializa arquivo existente a partir de `dict`.
- **AD-44 — Semântica do `apply`.** Ação por (índice, texto formatado); `commentsChanged`; o `apply` nunca altera o rascunho (contadores são do autor; aviso `ADR_COUNTER_NOT_ADVANCED`, errata no parent AD-14); gravação atômica por arquivo com restauração se o commit falhar.
- **AD-46 — Normalização de texto.** `fold`, `slug`, `gh_anchor` em `domain/services/text.py`, únicos.
- **Apertos:** AD-27 (raiz só no `Container`, nenhum caminho absoluto em `Result`); AD-28 (`VersionControl.head()`, versão e relógio injetados no `build`); precedência espinha > histórias em nomes e versões.

## O que está bom (e não deve mudar)

- Um caso de uso por comando, `Request/Result` como contrato, sem `Protocol` para caso de uso (AD-26).
- `bootstrap.py` como composição única e o `memory` para testes (AD-27).
- Registro de regras com código estável e teste por `code` (AD-31).
- Golden files + `tests/contract` + `lint-imports` no `poe check` (AD-34): é exatamente o mecanismo que vai **pegar** H1, H2, H5 e H6 — desde que as regras acima digam qual é o certo.
