---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - docs/prd-dominio-2026-10-17/prd.md
  - docs/prd-dominio-2026-10-17/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-harness_corp-2026-09-26/ARCHITECTURE-SPINE.md
  - docs/prd-dominio-2026-10-17/exemplo-catalogo/
---

# Sinter — Catálogo, passo 1 (Domínio) - Epic Breakdown

## Overview

Este documento quebra em épicos e histórias os requisitos do PRD do catálogo (passo 1: Domínio), do addendum e da espinha de arquitetura, para implementação.

## Requirements Inventory

### Functional Requirements

FR1: Iniciar o catálogo — cria estrutura de pastas e `organization.yaml` (áreas e repos vazios, `schemaVersion`); rodar de novo num catálogo existente não altera nada e avisa.
FR2: Manter as listas da organização — áreas, repos (id + endereço), regulações (nome, jurisdição, vigência, pode substituir outra) e padrões; um repo pode ser citado por vários domínios.
FR3: Criar domínio — id-domínio (obrigatório, único, maiúsculas/números 2–8), nome, área (existe na organização) e propósito; mesmo nome pode existir em áreas diferentes.
FR4: Descrever o domínio para a IA — faz/não faz/não sabemos, regras inline com id (só as que valem para todos os subdomínios), jornadas principais, fronteiras calculadas a partir dos subdomínios, donos, repos compartilhados; domínio sem propósito é recusado; listas vazias aparecem como vazias na consulta.
FR5: Intenção de modernização — objetivo (uma frase) + decisão em domínio/subdomínio; panorama (contagem por lifecycle) é calculado.
FR6: Conhecimento ligado ao nível — regulações, padrões, decisões (por id, em domínio/subdomínio/jornada) e docs (em todos os níveis, inclusive cada repo de aplicação); tipos de doc da lista aberta `organization.docTypes`; doc com path em `docs/` ou url; reaproveitamento por id; herança domínio→subdomínio sem exceção, marcada como herdada na consulta.
FR7: Criar subdomínio — nome, propósito, `metadata.domain`; mesmos blocos do domínio (exceto id-domínio, área e config); o domínio mantém `subdomains:` como sumário que tem de bater; criar pela CLI já inclui o domínio com o sumário atualizado; jornadas do subdomínio calculadas; herança somada e marcada.
FR8: Aplicações do subdomínio — inline, com id `app-` único no catálogo, nome, lifecycle obrigatório (legacy|modernizing|modern|retired), apelidos e repos (repo, path, role, platform, docs); um repo pode compor várias aplicações.
FR10: Substituição de legado — relação `modernized_by` app→app com fase (planned|in-progress|done) e evidência.
FR11: Descrever jornada — propósito, gatilho, resultado, pendências, orquestrador, `variantOf`.
FR12: Etapas e passos — etapas com entrada e passos; passo aponta para subdomínio (ou só externo) e opcionalmente `calls`; ação, resultado, regras, regulação, evento, job, `onFailure`; grafo com `next` e `parallelWith`; todo `next` existe na jornada e todo subdomínio citado existe; consulta devolve a sequência em ordem com desvios de falha.
FR13: Do passo ao detalhe — navegação passo → subdomínio → aplicações → repos → docs, um nível por vez.
FR14: Documentos do domínio — `.md` em `docs/` do domínio; pauta e ata como tipos próprios; ata pode ser promovida a decisão (evidência aponta para a ata).
FR15: Consultar por nível — `get <id> --level 0|1|2` (0: id, nome, tipo, propósito, contagens; 1: + faz/não faz/não sabemos, filhos, repos calculados, panorama, conhecimento próprio e herdado, jornadas; 2: + vizinhança); JSON; diz o que foi omitido e como pedir.
FR16: Ler documento por seção — `read <doc>#âncora`.
FR17: Validar o catálogo — schema e obrigatórios; unicidade de ids e id-domínio; hierarquia sem ciclo; sumário de subdomínios bate; glossário sem redefinição na mesma linha; aviso de repetição de herdado; referências internas existem; `dom-` fora do catálogo = aviso; `ext-`/`evt-`/`agenda-` só formato; doc com path ou url e path existente; área existe; campos `(calc)` escritos = erro.
FR18: Caminho único de escrita — rascunho (item inteiro) → conferir (`apply --dry-run`: resumo em linguagem natural + erros, não grava) → gravar no lugar canônico (tabela kind→path) com registro de quem/quando/o quê; rascunho com erro não grava nada.
FR19: Dados do subdomínio — `data[]` (id `dat-`, nome, descrição, producedBy, personalData, docs) com camadas de `organization.dataLayers` (location, format, refresh, quality, consumers); dado pessoal marcado na consulta.
FR20: Glossário — em organização, domínio e subdomínio (termo, definição, sinônimos, não confundir com); definido uma vez no nível mais alto; herdado e marcado na consulta; redefinir na mesma linha = erro; domínios diferentes podem divergir.
FR21: Operação (opcional) — horário, janelas de batch, criticidade, volume em domínio/subdomínio; subdomínio herda o que não declarar.
FR22: Buscar no catálogo — `find <texto>` em nome, id-domínio, apelidos, glossário (termos e sinônimos), propósito e repo, ordenado por relevância, nível 0 + campo que casou, sem diferenciar maiúsculas/acentos; `list domains [--area]`.
FR25: Navegar por área — `list areas` (nome, descrição, quantos domínios), `get area-<slug>` (área + domínios no nível 0, calculados), `find` casa no nome da área, `get org --level 1` agrupa domínios por área; área continua sem arquivo próprio e sem herança.
FR23: Editar a partir do atual — `get <id> --raw` devolve o YAML do item como rascunho para voltar pelo `apply`.
FR24: Skills `/sinter-find` (só lê: find + get) e `/sinter-domain` (busca antes de criar; estrutura existente ou cria novo por **entrevista guiada**: uma pergunta por vez, com exemplo, opções do catálogo, seguimento em resposta vaga, "não sei" vira pendência, resumo por bloco, parar e retomar; sempre `apply --dry-run` → resumo → confirmação → `apply`). Ler fontes para rascunhar fica fora.

(FR9 foi incorporado ao FR8.)

### NonFunctional Requirements

NFR1: Compacto para a IA — nível 0 de um domínio ≤ ~300 tokens; nível 1 ≤ ~2.000 tokens para 10 subdomínios e 40 aplicações.
NFR2: Determinístico — mesma versão do catálogo gera a mesma resposta, byte a byte, na mesma ordem.
NFR3: Rápido — `validate` de 500 itens em ≤ 3 s numa máquina comum.
NFR4: Legível por humano — todo arquivo revisável num PR sem ferramenta especial (comentários preservados ao gravar).
NFR5: Local — sem rede e sem chamar modelo de IA.
NFR6: Versionado — o formato tem versão; CLI mais velha recusa catálogo de formato mais novo.

### Additional Requirements

- **Sem starter template:** a História 1.1 cria o projeto do zero com `uv` + hatchling (Python 3.13+, `[project.scripts] sinter = "sinter.adapters.inbound.cli.app:main"`), Pydantic 2.14, Typer 0.27, ruamel.yaml 0.19, pytest 9. **A espinha de código (`_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/`) vence este documento em nomes de pasta, formato de `--json`, códigos de saída e versões.**
- Arquitetura hexagonal (espinha de código AD-25..AD-48): `domain/` → `application/` → `ports/{inbound,outbound}` ← `adapters/{inbound/cli, outbound/{yaml_fs,git,local_fs,memory}}`, composição só em `bootstrap.py`; garantido por import-linter no `poe check`.
- Escrita só pelo `apply` (AD-3): grava no lugar canônico preservando comentários e faz **um** commit com trailers `Sinter-*`; exige o catálogo num repo git.
- Herança e calculados num lugar só (AD-22): repos do domínio, fronteiras do domínio, panorama, jornadas do subdomínio, lista de domínios da organização nunca são gravados.
- Contrato JSON Schema gerado a partir dos modelos Pydantic em `schemas/*.json` (AD-12), para o front TS da fatia 2.
- Todo comando aceita `--json` (chaves camelCase, resultado com `report: {errors[], warnings[]}` quando valida); códigos de saída 0 (ok), 1 (erro de validação ou item não encontrado), 2 (uso errado ou ambiente), 3 (erro interno).
- O `exemplo-catalogo/` vira fixture principal de teste (`tests/fixtures/exemplo-catalogo/`): tem de validar com zero erros e só avisos `dom-`.
- Restrição de PI: desenvolver e testar só com dados sintéticos/abertos (nunca código, docs ou reuniões do empregador do fundador).
- Instalação para o usuário: `uv tool install sinter`.
- **Skills (Epic 4) no padrão aberto [Agent Skills](https://agentskills.io/specification):** uma pasta por skill com `SKILL.md` (frontmatter `name` = nome da pasta, minúsculas/números/hífen, ≤ 64; `description` ≤ 1024 com o que faz **e quando usar**; `compatibility: Requer a CLI sinter (uv tool install sinter)`), corpo < 500 linhas, detalhes em `references/` e modelos de rascunho em `assets/`, referências a um nível só. Validadas com `skills-ref validate`.
- **Skills criadas e iteradas com a skill-creator da Anthropic:** rascunho → evals (casos de teste com o exemplo-catalogo) → ajuste da `description` para disparar certo. Os evals ficam versionados junto da skill.

### UX Design Requirements

Não se aplica: esta história é só CLI + skills, sem interface visual. A experiência da CLI está coberta por FR15, FR18 e FR22 (saída texto/JSON, resumo em linguagem natural, códigos de saída).

### FR Coverage Map

FR1: Epic 3 - `sinter catalog init`
FR2: Epic 1 - listas da organização (schema + validação)
FR3: Epic 3 - criar domínio (`new domain` + `apply`); regras de id-domínio validadas no Epic 1
FR4: Epic 1 - blocos do domínio (fronteiras calculadas exibidas no Epic 2)
FR5: Epic 1 - modernização (panorama calculado exibido no Epic 2)
FR6: Epic 1 - conhecimento ligado e herança (marcação do herdado no Epic 2)
FR7: Epic 1 - subdomínio e sumário que bate (sumário atualizado pela CLI no Epic 3)
FR8: Epic 1 - aplicações e repos
FR10: Epic 1 - relação `modernized_by`
FR11: Epic 1 - jornada
FR12: Epic 1 - etapas e passos (sequência devolvida pela consulta no Epic 2)
FR13: Epic 2 - do passo ao detalhe
FR14: Epic 1 - docs em `docs/` (promover ata a ADR no Epic 3)
FR15: Epic 2 - `get --level 0|1|2`
FR16: Epic 2 - `read doc#âncora`
FR17: Epic 1 - `sinter validate`
FR18: Epic 3 - `apply [--dry-run]` + commit
FR19: Epic 1 - dados por camada
FR20: Epic 1 - glossário (glossário somado na consulta no Epic 2)
FR21: Epic 1 - operação
FR22: Epic 2 - `find` e `list domains`
FR23: Epic 3 - `get --raw`
(NFR4 também: Story 3.7 `sinter fmt`)
FR25: Epic 2 - navegar por área (`list areas`, `get area-`, `find` na área)
FR24: Epic 4 - skills `/sinter-find` e `/sinter-domain`

## Epic List

### Epic 1: Um catálogo que se confere
O arquiteto escreve os YAML do catálogo (organização, domínio, subdomínio, jornada, relação) e `sinter validate` aponta cada erro com arquivo e motivo; o exemplo PAGV + CAMB passa com zero erros. Inclui o projeto do zero (uv), o modelo do Apêndice A em Pydantic, o JSON Schema gerado, `--json` e códigos de saída.
**FRs covered:** FR2, FR4, FR5, FR6, FR7, FR8, FR10, FR11, FR12, FR14, FR17, FR19, FR20, FR21 · NFR3, NFR6

### Epic 2: A IA acha e entende o domínio
O agente acha um item sem saber o id (`find`, `list domains`) e o explica do geral para o detalhe (`get --level 0|1|2`, `read doc#âncora`), com herança marcada e calculados (repos, fronteiras, panorama, jornadas do subdomínio); mede o SM-2.
**FRs covered:** FR13, FR15, FR16, FR22, FR25 · NFR1, NFR2, NFR5

### Epic 3: Criar e estruturar pela CLI
O arquiteto cria o catálogo, domínios, subdomínios e jornadas e edita o que existe por um caminho só (`new`/`get --raw` → `apply --dry-run` → `apply`), com resumo em linguagem natural e um commit por gravação.
**FRs covered:** FR1, FR3, FR18, FR23 · NFR4

### Epic 4: Estruturar conversando com o agente
O arquiteto usa `/sinter-find` para achar e entender e `/sinter-domain` para criar ou estruturar um domínio: a skill busca antes de criar, pergunta só o obrigatório, mostra o resumo e grava após confirmação.
**FRs covered:** FR24

## Epic 1: Um catálogo que se confere

O arquiteto escreve os YAML do catálogo e `sinter validate` aponta cada erro com arquivo e motivo; o exemplo PAGV + CAMB passa com zero erros e só avisos `dom-`. Cada história acrescenta um `kind` (ou um grupo de regras) ao modelo e ao `validate`.

### Story 1.1: Validar a raiz do catálogo

Como arquiteto,
Quero rodar `sinter validate` numa pasta de catálogo e ver se a organização, os repos, as regulações e os padrões estão corretos,
Para que eu tenha uma base confiável antes de descrever qualquer domínio.

**Acceptance Criteria:**

**Dado** um projeto novo criado com `uv` + hatchling (Python 3.13+, Pydantic, Typer, ruamel.yaml, pytest) com `[project.scripts] sinter = "sinter.adapters.inbound.cli.app:main"`, as pastas `domain/`, `application/`, `ports/`, `adapters/` e `bootstrap.py` da espinha de código, e `uv run poe check` (import-linter, ruff, mypy, pytest) passando
**Quando** rodo `uv run sinter --help`
**Então** vejo o comando `validate`
**E** o CI (GitHub Actions, Python 3.13 e 3.14, ubuntu e macos) roda o mesmo `poe check`

**Dado** uma pasta com `organization.yaml`, `repositories.yaml`, `regulations/*.yaml` e `standards/*.yaml` no formato do Apêndice A (envelope `apiVersion`/`kind`/`metadata`/`spec`)
**Quando** rodo `sinter validate <pasta>`
**Então** cada arquivo é lido como o seu `kind` (Organization, RepositoryList, Regulation, Standard)
**E** a saída diz "0 erros" e o código de saída é `0`

**Dado** um arquivo com campo obrigatório faltando, campo desconhecido, `kind` desconhecido ou id fora do prefixo (`reg-`, `std-`, `repo-`, `area-`)
**Quando** rodo `sinter validate`
**Então** cada erro aparece com caminho do arquivo, campo e motivo, e o código de saída é `1`

**Dado** uma regulação com `supersedes` apontando para uma regulação que não existe
**Quando** rodo `sinter validate`
**Então** recebo erro de referência

**Dado** um catálogo com `schemaVersion` maior que o suportado pela CLI
**Quando** rodo `sinter validate`
**Então** a CLI recusa com mensagem clara e código `1` (NFR6)

**Dado** uma pasta que não é catálogo (sem `organization.yaml`) ou uma opção inválida
**Quando** rodo `sinter validate`
**Então** o código de saída é `2`

**Dado** qualquer execução
**Quando** passo `--json`
**Então** a saída é JSON com `report.errors[]` e `report.warnings[]`, cada item com `code`, `severity`, `file` (relativo à raiz), `path` (ex.: `spec.applications[app-x].lifecycle`) e `message`, na ordem da AD-35

### Story 1.2: Validar o domínio

Como arquiteto,
Quero que `sinter validate` confira cada `domain.yaml`,
Para que todo domínio tenha identidade única e o que a IA precisa ler primeiro.

**Acceptance Criteria:**

**Dado** `domains/<d>/domain.yaml` com `kind: Domain` no formato do Apêndice A.2 (identidade, purpose, does/doesNot/unknowns, subdomains, rules, decisions, glossary, operation, modernization, regulations, standards, docs, sharedRepositories, nextTaskNumber/nextAdrNumber/delivery)
**Quando** rodo `sinter validate`
**Então** os domínios PAGV e CAMB do exemplo passam sem erro de schema

**Dado** um domínio sem `purpose`
**Quando** valido
**Então** recebo erro (FR4)

**Dado** um `domainId` fora do formato (maiúsculas e números, 2–8) ou repetido em outro domínio, ou uma pasta `domains/<x>/` cujo nome não bate com o `domainId`
**Quando** valido
**Então** recebo erro com os dois arquivos envolvidos, quando houver repetição (FR3)

**Dado** dois domínios com o mesmo `name` em áreas diferentes e `domainId` diferentes
**Quando** valido
**Então** não há erro

**Dado** `metadata.area` que não está em `organization.areas`
**Quando** valido
**Então** recebo erro

**Dado** um domínio que escreve um campo calculado (`boundaries`, `repositories`, `journeys`, panorama)
**Quando** valido
**Então** recebo erro "campo calculado não deve ser escrito"

**Dado** regras (`rule-`) e decisões (`ADR-<ID>-NNN`) inline
**Quando** valido
**Então** ids fora do formato ou repetidos no catálogo são erro, e o `ADR-<ID>` tem de usar o `domainId` do próprio domínio

**Dado** blocos `operation` e `glossary`
**Quando** valido
**Então** são aceitos como opcionais e checados no formato dos blocos comuns (FR20, FR21)

### Story 1.3: Validar o subdomínio, suas aplicações e seus dados

Como arquiteto,
Quero que `sinter validate` confira cada subdomínio com aplicações, repos e dados,
Para que o legado, os repos e os dados de cada parte estejam descritos de um jeito só.

**Acceptance Criteria:**

**Dado** `domains/<d>/subdomains/sub-*.yaml` com `kind: Subdomain` (Apêndice A.3)
**Quando** valido
**Então** os 13 subdomínios do exemplo passam sem erro de schema

**Dado** `metadata.domain` apontando para um domínio inexistente, ou um subdomínio fora da pasta do seu domínio
**Quando** valido
**Então** recebo erro

**Dado** a lista `subdomains:` do domínio
**Quando** ela tem um subdomínio a mais, a menos ou repetido em relação aos arquivos que dizem pertencer a ele
**Então** recebo erro dizendo qual falta ou sobra (FR7)

**Dado** uma aplicação sem `lifecycle`, com lifecycle fora de `legacy|modernizing|modern|retired`, ou id fora de `app-<id-domínio>-<slug>`
**Quando** valido
**Então** recebo erro (FR8)

**Dado** um `repositories[].repo` que não está em `repositories.yaml`, ou `role` fora de `frontend|bff|api|batch|lib|infra`
**Quando** valido
**Então** recebo erro

**Dado** o mesmo repo em duas aplicações diferentes
**Quando** valido
**Então** não há erro

**Dado** um dado (`dat-`) com camada que não está em `organization.dataLayers`, ou `producedBy` que não é uma aplicação do catálogo
**Quando** valido
**Então** recebo erro (FR19)

**Dado** ids de aplicação ou de dado repetidos em qualquer lugar do catálogo
**Quando** valido
**Então** recebo erro citando os dois arquivos

### Story 1.4: Validar jornadas e substituição de legado

Como arquiteto,
Quero que `sinter validate` confira jornadas e relações `modernized_by`,
Para que a sequência de passos e o caminho da modernização nunca apontem para o vazio.

**Acceptance Criteria:**

**Dado** `domains/<d>/journeys/jor-*.yaml` com `kind: Journey` (Apêndice A.4)
**Quando** valido
**Então** as 3 jornadas do exemplo passam sem erro

**Dado** um passo com `capability` que não é subdomínio do catálogo, ou sem `capability` e sem `calls`
**Quando** valido
**Então** recebo erro (FR12)

**Dado** um `next` ou `parallelWith` que aponta para passo de outra jornada ou inexistente, ou ids de passo/etapa repetidos na jornada
**Quando** valido
**Então** recebo erro

**Dado** `next` formando ciclo
**Quando** valido
**Então** é aceito (jornadas podem ter retentativa), sem erro

**Dado** `application`, `rules`, `governedBy` de um passo apontando para itens inexistentes
**Quando** valido
**Então** recebo erro

**Dado** `variantOf` ou `orchestrator` apontando para itens inexistentes
**Quando** valido
**Então** recebo erro

**Dado** `calls`/`event`/`job`/`trigger` com `ext-`, `evt-` ou `agenda-`
**Quando** valido
**Então** só o formato do id é conferido

**Dado** `domains/<d>/relations/rel-*.yaml` com `kind: Relation`
**Quando** o tipo não é `modernized_by`, origem ou destino não são aplicações do catálogo, a fase não é `planned|in-progress|done`, ou o nome do arquivo não bate com origem/tipo/destino
**Então** recebo erro (FR10)

### Story 1.5: Validar referências, docs, glossário e herança

Como arquiteto,
Quero que `sinter validate` confira tudo que um nível cita e o que ele herda,
Para que a IA nunca receba um link quebrado, um termo com dois sentidos ou uma repetição inútil.

**Acceptance Criteria:**

**Dado** referências internas (regulação, padrão, regra, decisão, jornada, doc por `ref`, `mainJourneys`, `modernization.decision`, `boundaries.from/to` internos, evidência `source`)
**Quando** alguma não existe
**Então** recebo erro com o arquivo e o campo (FR17)

**Dado** uma referência `dom-` a um domínio que não está no catálogo
**Quando** valido
**Então** recebo **aviso**, não erro, e o código de saída continua `0`

**Dado** um doc
**Quando** não tem `path` nem `url`, tem os dois, tem `type` fora de `organization.docTypes`, ou o `path` aponta para arquivo que não existe em `domains/<d>/`
**Então** recebo erro (FR6, FR14)

**Dado** um termo de glossário definido na organização e redefinido no domínio, ou no domínio e redefinido no subdomínio (comparação sem maiúsculas e acentos, incluindo sinônimos)
**Quando** valido
**Então** recebo erro citando os dois níveis (FR20)

**Dado** o mesmo termo definido em dois domínios diferentes
**Quando** valido
**Então** não há erro

**Dado** um subdomínio que repete uma regulação, padrão, regra ou decisão já ligada ao seu domínio
**Quando** valido
**Então** recebo **aviso** de repetição de herdado (FR6)

**Dado** o `exemplo-catalogo/` copiado para `tests/fixtures/`
**Quando** rodo `sinter validate`
**Então** o resultado é **zero erros** e só avisos `dom-` (SM-1), e isso é um teste automatizado

### Story 1.6: Contrato JSON Schema e desempenho

Como arquiteto (e como o futuro front TS),
Quero o formato publicado como JSON Schema e um `validate` rápido,
Para que outras ferramentas e editores entendam o catálogo e o validate rode a cada salvar.

**Acceptance Criteria:**

**Dado** os modelos Pydantic de todos os `kind`
**Quando** rodo `sinter schema export <pasta>`
**Então** é gerado um `*.schema.json` por `kind` em `schemas/`, determinístico (mesma entrada, mesmo arquivo byte a byte)
**E** um teste falha se o `schemas/` versionado estiver desatualizado em relação aos modelos (AD-12)

**Dado** um catálogo sintético gerado no teste com 500 itens
**Quando** rodo `sinter validate`
**Então** termina em até 3 s numa máquina comum (NFR3), medido por teste marcado como `perf`

## Epic 2: A IA acha e entende o domínio

O agente acha um item sem saber o id e o explica do geral para o detalhe, com herança marcada e campos calculados, sem rede e sem IA; a saída é a mesma byte a byte para o mesmo catálogo. Fecha medindo o SM-2.

### Story 2.1: Consultar domínio e subdomínio nos níveis 0 e 1

Como agente de código (e como arquiteto),
Quero rodar `sinter get <id> --level 0|1` num domínio ou subdomínio,
Para que eu entenda para que ele existe, o que faz e não faz, e o que ninguém sabe, sem ler arquivos inteiros.

**Acceptance Criteria:**

**Dado** o exemplo-catalogo
**Quando** rodo `sinter get dom-pagv --level 0`
**Então** vejo id, nome, tipo, id-domínio, área, propósito e contagens (subdomínios, aplicações, jornadas)

**Dado** o mesmo domínio
**Quando** rodo `--level 1`
**Então** vejo também faz / não faz / não sabemos, a lista de subdomínios na ordem do sumário (cada um no nível 0), regras, jornadas principais, operação, modernização, glossário, regulações, padrões, decisões (resumo) e docs (título, tipo, path ou url)

**Dado** faz, não faz ou não sabemos vazios
**Quando** consulto
**Então** a saída diz explicitamente "não preenchido" (FR4)

**Dado** um subdomínio
**Quando** rodo `get sub-pagv-conciliacao --level 1`
**Então** vejo o que é dele somado ao que herda do domínio (regras, regulações, padrões, decisões, docs, glossário da organização e do domínio, operação não declarada), **cada item herdado marcado com a origem** (FR6, FR7, FR20, FR21)

**Dado** qualquer resposta
**Quando** passo `--json`
**Então** recebo o mesmo conteúdo em JSON, com um campo `omitted` dizendo o que ficou de fora e o comando para pedir (ex.: `get <id> --level 2`) (FR15)

**Dado** um id que não existe
**Quando** consulto
**Então** recebo erro com código `1` e até 3 ids parecidos sugeridos

**Dado** o domínio CAMB (10 subdomínios)
**Quando** consulto nos níveis 0 e 1
**Então** o nível 0 cabe em ~300 tokens e o nível 1 em ~2.000 tokens, medido por teste (NFR1)

### Story 2.2: Ver o que é calculado (repos, fronteiras, legado, dados)

Como agente de código,
Quero que a consulta do domínio já traga os repos, as fronteiras, o panorama de modernização e os dados,
Para que eu saiba onde está o código e o que é legado sem que ninguém mantenha essas listas à mão.

**Acceptance Criteria:**

**Dado** `get dom-pagv --level 1`
**Quando** vejo a seção de repos
**Então** ela traz os repos de todas as aplicações dos subdomínios mais os `sharedRepositories`, sem repetição, cada um com papel, plataforma e as aplicações que usam o repo (FR4, FR8)

**Dado** o mesmo domínio
**Quando** vejo as fronteiras
**Então** elas são calculadas das fronteiras dos subdomínios que apontam para fora do domínio (entra: de onde/o quê; sai: para onde/o quê), sem fronteiras internas entre subdomínios do mesmo domínio (FR4)

**Dado** o mesmo domínio
**Quando** vejo a modernização
**Então** aparece o objetivo, a decisão e o panorama com a contagem por lifecycle e quais aplicações estão em cada estado, incluindo as relações `modernized_by` com fase (FR5, FR10)

**Dado** `get sub-camb-carteira --level 1`
**Quando** vejo os dados
**Então** cada dado aparece com as camadas na ordem de `organization.dataLayers` e, se `personalData: true`, marcado como "dado pessoal (LGPD)" (FR19)

**Dado** `get sub-<x> --level 1`
**Quando** vejo jornadas
**Então** aparecem as jornadas que têm passo apontando para o subdomínio (calculadas), com os passos onde ele aparece (FR7)

**Dado** o mesmo catálogo consultado duas vezes
**Quando** comparo as saídas texto e JSON
**Então** são idênticas byte a byte, com ordem estável (NFR2)

### Story 2.3: Seguir a jornada e descer do passo até o repo

Como agente de código,
Quero consultar uma jornada em ordem e descer de um passo até a aplicação, os repos e os docs,
Para que eu explique em que ordem as coisas acontecem e o que acontece quando um passo falha.

**Acceptance Criteria:**

**Dado** `get jor-pagv-pagar-pedido --level 1`
**Quando** vejo a saída
**Então** aparecem propósito, gatilho, resultado, pendências e as etapas em ordem, cada passo com subdomínio (nível 0), ação, resultado, próximos, paralelos e `onFailure` (FR11, FR12)

**Dado** passos com `next` formando desvios
**Quando** consulto a jornada
**Então** a ordem segue o grafo a partir do primeiro passo de cada etapa (ordem do arquivo como desempate), sem repetir passos em ciclo

**Dado** uma jornada com `variantOf`
**Quando** consulto
**Então** a saída mostra de qual jornada é variante

**Dado** `get app-pagv-conciliacao --level 1` ou `get repo-<x> --level 1`
**Quando** consulto
**Então** vejo, para a aplicação: subdomínio, lifecycle, apelidos, repos (papel, plataforma, path) e docs; para o repo: endereço, aplicações que o usam e docs (FR13)

**Dado** qualquer item
**Quando** rodo `--level 2`
**Então** vejo também a vizinhança: jornadas e passos que passam pelo item, aplicações que ele substitui ou que o substituem (FR15)

### Story 2.4: Ler só uma seção de um documento

Como agente de código,
Quero rodar `sinter read <doc>#<âncora>`,
Para que eu leia só a parte que interessa de um `.md` sem gastar contexto com o documento inteiro.

**Acceptance Criteria:**

**Dado** um doc com `path` para um `.md` em `docs/`, identificado pelo id do doc ou pelo caminho
**Quando** rodo `sinter read <doc>#decisoes`
**Então** recebo só o conteúdo do título cuja âncora (estilo GitHub, sem acento) é `decisoes`, até o próximo título do mesmo nível ou superior (FR16)

**Dado** `sinter read <doc>` sem âncora
**Quando** rodo
**Então** recebo o sumário de títulos com as âncoras e o tamanho de cada seção, não o arquivo inteiro

**Dado** uma âncora que não existe
**Quando** rodo
**Então** recebo erro com código `1` e a lista de âncoras disponíveis

**Dado** um doc que é só `url`
**Quando** rodo `read`
**Então** recebo a url e o aviso de que o Sinter não lê conteúdo externo (NFR5)

### Story 2.5: Achar um item sem saber o id, começando pela área

Como agente de código (e como arquiteto),
Quero rodar `sinter find <texto>`, `sinter list areas` e `sinter list domains`,
Para que eu descubra se um domínio, subdomínio, aplicação ou termo já existe antes de perguntar ou criar.

**Acceptance Criteria:**

**Dado** o exemplo-catalogo
**Quando** rodo `sinter find boleta`
**Então** recebo, ordenados por relevância, o termo de glossário *Boleta* (CAMB), `sub-camb-boletagem` e a aplicação com apelido `BOL0100`, cada um no nível 0 com o campo onde casou (FR22)

**Dado** `sinter find cambio` (sem acento) ou `CAMB`
**Quando** rodo
**Então** `dom-camb` aparece em primeiro (casamento exato de id-domínio ou nome vence casamento parcial)

**Dado** a busca
**Quando** casa em nome, id-domínio, apelido, termo ou sinônimo, propósito ou repo
**Então** a relevância segue a ordem: id/id-domínio/apelido exato > nome exato > termo/sinônimo > nome parcial > propósito > repo; empates por id em ordem alfabética (NFR2)

**Dado** um texto sem resultado
**Quando** rodo `find`
**Então** a saída diz "nada encontrado" e o código é `0` (não é erro)

**Dado** `sinter list domains --area area-cambio`
**Quando** rodo
**Então** vejo id, id-domínio, nome, área e propósito dos domínios daquela área, em ordem de id-domínio

**Dado** `sinter list areas`
**Quando** rodo
**Então** vejo id, nome, descrição e quantidade de domínios de cada área, em ordem de id (FR25)

**Dado** `sinter get area-cambio --level 0|1`
**Quando** rodo
**Então** vejo nome e descrição da área e os seus domínios no nível 0 (lista calculada do `metadata.area`); no nível 1, também as contagens de subdomínios e aplicações por domínio

**Dado** `sinter find cambio`
**Quando** rodo
**Então** a área `area-cambio` aparece entre os resultados, com o campo "nome da área"

**Dado** `sinter get org-acme --level 1`
**Quando** rodo
**Então** os domínios aparecem agrupados por área (área sem domínio aparece com "nenhum domínio")

**Dado** `--json` e `--limit N` em `find`
**Quando** rodo
**Então** a saída é JSON e tem no máximo N resultados (padrão 10)

### Story 2.6: Medir se a IA entende (SM-2)

Como fundador,
Quero rodar o questionário de avaliação contra a saída do Sinter,
Para que eu saiba com número se a estrutura faz a IA entender o domínio melhor que texto corrido.

**Acceptance Criteria:**

**Dado** o [avaliacao-ia.md](avaliacao-ia.md) e o exemplo-catalogo
**Quando** sigo o roteiro (rodada Sinter com `get`/`read`/`find`, rodada base com os `.md` sem estrutura, 3 execuções cada)
**Então** cada resposta do gabarito pode ser obtida só com `get --level 1|2` e `read` (verificado por teste que procura cada fato do gabarito na saída)

**Dado** as rodadas feitas
**Quando** registro na tabela do avaliacao-ia.md
**Então** fica anotado data, agente, modelo, nota por execução, média e se houve resposta inventada na Q9

**Dado** a meta do SM-2 (média ≥ 9/10 e zero inventadas)
**Quando** não é atingida
**Então** as perguntas erradas viram itens de ajuste do formato do nível 1, sem crescer o nível 1 além do NFR1 (SM-C2)

## Epic 3: Criar e estruturar pela CLI

O arquiteto cria e altera o catálogo por um caminho só: rascunho → `apply --dry-run` (confere, não grava) → `apply` (grava no lugar canônico e faz um commit). O rascunho vem do `new`, do `get --raw` ou é escrito à mão.

### Story 3.1: Iniciar um catálogo

Como arquiteto,
Quero rodar `sinter catalog init [pasta]`,
Para que eu comece um catálogo com a estrutura certa sem montar pastas à mão.

**Acceptance Criteria:**

**Dado** uma pasta vazia ou inexistente
**Quando** rodo `sinter catalog init <pasta> --org-id org-acme --org-name "Acme"`
**Então** são criados `organization.yaml` (com `schemaVersion`, áreas vazias, os 7 `docTypes` padrão e `dataLayers` raw/trusted/refined), `repositories.yaml` vazio e as pastas `domains/`, `regulations/` e `standards/` (FR1)
**E** se a pasta não é repo git, é feito `git init` e um primeiro commit com trailer `Sinter-Action: init`

**Dado** a pasta criada
**Quando** rodo `sinter validate`
**Então** o resultado é zero erros

**Dado** uma pasta que já é catálogo
**Quando** rodo `init` de novo
**Então** nada é alterado, recebo aviso e o código é `0`

**Dado** uma pasta não vazia que não é catálogo
**Quando** rodo `init`
**Então** a CLI recusa com código `2`

### Story 3.2: Conferir um rascunho sem gravar

Como arquiteto (e como skill),
Quero rodar `sinter apply <arquivo|-> --dry-run`,
Para que eu veja em linguagem natural o que vai mudar e os erros antes de gravar qualquer coisa.

**Acceptance Criteria:**

**Dado** um rascunho com um ou mais manifestos (YAML multi-documento, de arquivo ou da entrada padrão)
**Quando** rodo `apply --dry-run`
**Então** cada manifesto é validado contra o seu `kind` **e** contra o catálogo como ficaria depois da mudança (todas as regras do Epic 1) (FR18)

**Dado** um rascunho válido
**Quando** confiro
**Então** recebo, para cada item, a ação (cria / altera / sem mudança) e um resumo em linguagem natural (ex.: "cria o subdomínio Hedge em CAMB, com 1 aplicação (modern) e 1 repo; inclui no sumário depois de Liquidação"); para alterações, o que mudou campo a campo

**Dado** um rascunho com erro
**Quando** confiro
**Então** recebo os erros com o manifesto e o campo, e o código é `1`

**Dado** um rascunho que ainda tem marcas de obrigatório não preenchido (`<obrigatório>`)
**Quando** confiro
**Então** cada marca é um erro

**Dado** qualquer conferência
**Quando** termina
**Então** nenhum arquivo do catálogo foi alterado e nenhum commit foi feito

**Dado** `--json`
**Quando** confiro
**Então** recebo `{items: [{kind, id, action, file, summary, changes, commentsChanged}], report: {errors, warnings}, summary}`

### Story 3.3: Gravar um rascunho com um commit

Como arquiteto (e como skill),
Quero rodar `sinter apply <arquivo|->` sem `--dry-run`,
Para que a mudança vá para o lugar certo do catálogo e fique registrada com quem, quando e o quê.

**Acceptance Criteria:**

**Dado** um rascunho válido
**Quando** rodo `apply`
**Então** cada manifesto é gravado no caminho canônico do seu `kind` (tabela do FR18), substituindo o arquivo do item inteiro
**E** é feito **um** commit com o autor do `git config` e trailers `Sinter-Action`, `Sinter-Items` (ids) e `Sinter-Version`

**Dado** um rascunho com erro em qualquer manifesto
**Quando** rodo `apply`
**Então** nada é gravado, nem em parte, e o código é `1`

**Dado** um item que já existe e tem comentários no YAML
**Quando** o rascunho veio do `get --raw` com os comentários
**Então** os comentários são preservados e as chaves ficam na ordem canônica (Story 3.7) ao gravar (NFR4)

**Dado** um arquivo do item com alterações não commitadas
**Quando** rodo `apply` sobre ele
**Então** a CLI recusa com código `1` dizendo qual arquivo, para não perder edição

**Dado** um rascunho em que nada mudou
**Quando** rodo `apply`
**Então** nenhum commit é feito e a saída diz "sem mudança"

**Dado** a gravação concluída
**Quando** rodo `sinter validate`
**Então** o resultado é o mesmo da conferência (zero erros)

### Story 3.4: Criar um domínio

Como arquiteto,
Quero rodar `sinter new domain`,
Para que eu receba um rascunho de domínio com tudo o que precisa ser preenchido marcado.

**Acceptance Criteria:**

**Dado** um catálogo
**Quando** rodo `sinter new domain`
**Então** recebo na saída padrão (ou em `-o arquivo`) um rascunho no formato do Apêndice A.2 com os obrigatórios marcados `<obrigatório>` e os opcionais comentados com uma linha de explicação

**Dado** flags `--domain-id PAGV --name "Pagamentos (Varejo)" --area area-varejo --purpose "..."`
**Quando** rodo `new domain`
**Então** o rascunho já vem com esses campos e o id `dom-pagv` (FR3)

**Dado** um `--domain-id` que já existe, ou `--area` fora da organização
**Quando** rodo `new domain`
**Então** recebo o erro já no `new`, com o domínio existente citado

**Dado** o rascunho preenchido
**Quando** rodo `apply`
**Então** o domínio é gravado em `domains/<id-domínio>/domain.yaml` e a pasta `docs/` é criada

### Story 3.5: Acrescentar subdomínio e jornada

Como arquiteto,
Quero rodar `sinter new subdomain` e `sinter new journey`,
Para que eu estruture um domínio existente sem esquecer de atualizar o sumário.

**Acceptance Criteria:**

**Dado** o domínio `dom-camb`
**Quando** rodo `sinter new subdomain --domain dom-camb --name Hedge --purpose "..." [--after sub-camb-liquidacao]`
**Então** recebo um rascunho com **dois** manifestos: o subdomínio novo (Apêndice A.3, com uma aplicação de exemplo comentada) e o domínio inteiro com `sub-camb-hedge` inserido no sumário na posição pedida (no fim, se não informado) (FR7)

**Dado** esse rascunho aplicado
**Quando** rodo `sinter validate`
**Então** o sumário bate com os arquivos e não há erro

**Dado** `sinter new journey --domain dom-camb --name "Enviar moeda PJ" [--variant-of jor-camb-enviar-moeda-pf]`
**Quando** rodo
**Então** recebo um rascunho de jornada (Apêndice A.4) com uma etapa e um passo de exemplo, `capability` marcada `<obrigatório>` e a lista dos subdomínios do domínio comentada para escolha (FR11, FR12)

**Dado** um id gerado que já existe
**Quando** rodo `new`
**Então** recebo erro já no `new`

### Story 3.6: Editar o que já existe

Como arquiteto (e como skill),
Quero rodar `sinter get <id> --raw`,
Para que eu altere um item a partir do arquivo atual e devolva pelo mesmo caminho.

**Acceptance Criteria:**

**Dado** um item que mora em arquivo próprio (organização, lista de repos, regulação, padrão, domínio, subdomínio, jornada, relação)
**Quando** rodo `get <id> --raw`
**Então** recebo o conteúdo exato do arquivo, com comentários (FR23)

**Dado** um item que mora dentro de outro (aplicação, dado, regra, decisão)
**Quando** rodo `get app-camb-carteira --raw`
**Então** recebo o arquivo do item que o contém (o subdomínio inteiro) e um aviso dizendo isso, porque o rascunho é sempre o item inteiro

**Dado** o rascunho alterado (ex.: acrescentar uma área em `organization.yaml`, um repo em `repositories.yaml`, uma aplicação num subdomínio)
**Quando** rodo `apply --dry-run` e depois `apply`
**Então** o resumo mostra só o que mudou e o commit grava a mudança com os comentários preservados (FR2, FR18)

**Dado** uma ata em `docs/`
**Quando** acrescento ao domínio uma decisão `ADR-<ID>-NNN` com `evidence` apontando para a ata e aplico
**Então** a ata fica promovida a decisão, e o `nextAdrNumber` do domínio deve ser incrementado no mesmo rascunho (o `dry-run` avisa se não foi) (FR14)

## Epic 4: Estruturar conversando com o agente

O arquiteto conversa com o agente de código: `/sinter-find` acha e explica; `/sinter-domain` busca antes de criar, preenche cada nível numa **entrevista guiada** (uma pergunta por vez, com exemplo e opções), mostra o resumo e grava após confirmação. As skills seguem o padrão [Agent Skills](https://agentskills.io/specification), são criadas e iteradas com a skill-creator da Anthropic e só chamam a CLI com `--json`.

### Story 4.1: Achar e explicar com `/sinter-find`

Como arquiteto,
Quero perguntar ao agente "onde fica X?" ou "explica o domínio Y" usando `/sinter-find`,
Para que eu entenda o catálogo conversando, sem decorar ids nem comandos.

**Acceptance Criteria:**

**Dado** a skill-creator instalada
**Quando** crio a skill `skills/sinter-find/`
**Então** ela tem `SKILL.md` com `name: sinter-find`, `description` (≤ 1024) dizendo o que faz e quando usar, `compatibility` citando a CLI, corpo < 500 linhas e `references/` explicando a saída de `find` e dos níveis 0/1/2
**E** `skills-ref validate skills/sinter-find` passa, como teste automatizado

**Dado** o pedido "onde fica a geração da boleta?"
**Quando** a skill roda contra o exemplo-catalogo
**Então** ela chama `sinter find boleta --json` e depois `sinter get sub-camb-boletagem --level 1 --json`, e responde com subdomínio, domínio, legado BOL0100 e repo, sem inventar nada fora da saída da CLI

**Dado** uma pergunta cuja resposta é pendência (ex.: Q9 do avaliacao-ia.md)
**Quando** a skill responde
**Então** ela diz que ninguém sabe ainda e cita a pendência, em vez de inventar

**Dado** mais de um resultado no `find`
**Quando** a skill responde
**Então** ela lista as opções e pergunta qual, em vez de escolher sozinha

**Dado** a skill
**Quando** ela é usada
**Então** ela nunca grava nem chama `apply` (só leitura)

**Dado** os evals da skill-creator (no mínimo 5 pedidos que devem disparar a skill e 3 que não devem, contra o exemplo-catalogo)
**Quando** rodo os evals
**Então** todos passam, e os evals ficam versionados em `skills/sinter-find/`

### Story 4.2: Entrevista guiada para preencher o YAML

Como arquiteto,
Quero que o preenchimento de cada nível seja uma conversa em que a skill me faz as perguntas certas,
Para que eu descreva o domínio em linguagem de negócio, sem conhecer os campos do YAML, e a resposta saia no formato que a IA precisa.

**Acceptance Criteria:**

**Dado** a skill-creator instalada
**Quando** crio a skill `skills/sinter-domain/`
**Então** ela tem `SKILL.md` com `name: sinter-domain`, `description` (≤ 1024) dizendo o que faz e quando usar, `compatibility` citando a CLI, corpo < 500 linhas, os roteiros em `references/entrevista-<kind>.md` e os modelos de rascunho em `assets/`
**E** `skills-ref validate skills/sinter-domain` passa, como teste automatizado

**Dado** a skill `sinter-domain`
**Quando** ela vai preencher um domínio, subdomínio, aplicação ou jornada
**Então** segue um roteiro de perguntas por nível em `references/entrevista-<kind>.md`, do geral para o detalhe: identidade → propósito → faz / não faz → não sabemos → subdomínios → aplicações e legado → regras e regulações → glossário → jornadas → docs (FR24)

**Dado** cada pergunta
**Quando** a skill pergunta
**Então** faz **uma pergunta por vez** (ou um bloco pequeno), em linguagem de negócio, nunca pelo nome do campo, e com um **exemplo** do tipo de resposta esperada (ex.: "Em uma frase, para que esse domínio existe? Ex.: *Permite que clientes comprem e enviem moeda estrangeira, da cotação até a liquidação*")

**Dado** um campo com valores conhecidos no catálogo (área, lifecycle, papel e plataforma do repo, tipo de doc, regulações, padrões, repos, subdomínios para um passo de jornada)
**Quando** a skill pergunta
**Então** oferece as **opções numeradas** lidas da CLI (`get`/`list`/`find --json`) e aceita "outra", em vez de pergunta aberta

**Dado** uma resposta vaga ou incompleta (ex.: propósito com mais de uma frase, "faz tudo de câmbio", aplicação sem lifecycle)
**Quando** a skill recebe
**Então** faz uma **pergunta de seguimento** para direcionar (ex.: "O que as pessoas acham que esse domínio faz, mas não faz? E quem faz então?"; "Esse sistema é legado, está sendo modernizado ou já é o novo?")

**Dado** a resposta "não sei" ou "depende"
**Quando** a skill recebe
**Então** registra como item de **não sabemos** (pendência), com a dúvida em uma frase, e **não inventa** um valor

**Dado** uma sugestão que a skill deduz (ex.: id `sub-camb-hedge`, papel `api` para um repo `*-service`)
**Quando** a skill propõe
**Então** a sugestão aparece marcada como sugestão e só entra no rascunho se o arquiteto aceitar

**Dado** o fim de cada bloco
**Quando** a skill fecha o bloco
**Então** **resume o que entendeu** em linguagem natural e pede confirmação antes de seguir ("Entendi: Câmbio faz cotação, contratação e envio; não faz conta corrente (é de Contas). Certo?")

**Dado** o arquiteto quer parar no meio
**Quando** diz "chega por hoje"
**Então** a skill grava o que tem (se os obrigatórios estão preenchidos, pelo `apply`) e lista o que ficou faltando; numa próxima conversa, a skill começa por essas lacunas, lidas do "não preenchido" do `get --level 1`

**Dado** os evals da entrevista contra o exemplo-catalogo (respostas vagas, "não sei", área inexistente, opções numeradas)
**Quando** rodo
**Então** todos passam: uma pergunta por vez, exemplo em cada pergunta, opções quando há lista, "não sei" vira pendência e nenhum valor inventado no rascunho

### Story 4.3: Criar um domínio novo com `/sinter-domain`

Como arquiteto,
Quero pedir "cadastra o domínio X" usando `/sinter-domain`,
Para que o agente monte o domínio comigo, sem duplicar o que já existe.

**Acceptance Criteria:**

**Dado** a skill `sinter-domain` da Story 4.2
**Quando** acrescento o fluxo de criar
**Então** o `SKILL.md` descreve buscar → entrevista → rascunho → `apply --dry-run` → confirmar → `apply`, e `references/` traz os obrigatórios por `kind`; `skills-ref validate` continua passando

**Dado** o pedido "cadastra o domínio de Câmbio" num catálogo que já tem CAMB
**Quando** a skill roda
**Então** ela **primeiro** chama `sinter find câmbio --json`, mostra o domínio existente e pergunta se é para estruturá-lo ou criar outro em outra área (FR24)

**Dado** um domínio que não existe
**Quando** a skill roda
**Então** ela pergunta só o obrigatório (id-domínio, nome, área entre as existentes, propósito em uma frase) e, opcionalmente, faz / não faz / não sabemos; gera o rascunho com `sinter new domain` e flags

**Dado** o rascunho pronto
**Quando** a skill vai gravar
**Então** ela roda `sinter apply - --dry-run --json`, mostra o resumo em linguagem natural, **pede confirmação** e só então roda `sinter apply -`

**Dado** erros no `dry-run`
**Quando** a skill recebe
**Então** ela explica cada erro em linguagem simples e pergunta o que falta, sem gravar

**Dado** a área pedida não existe na organização
**Quando** a skill percebe
**Então** ela oferece acrescentar a área em `organization.yaml` pelo mesmo caminho (`get --raw` → `apply`), com confirmação separada

**Dado** os evals (incluindo "cadastra o domínio Câmbio" → tem de achar o CAMB e não criar outro)
**Quando** rodo os evals
**Então** todos passam e ficam versionados

### Story 4.4: Estruturar um domínio existente com `/sinter-domain`

Como arquiteto,
Quero pedir "falta o subdomínio Hedge no Câmbio" ou "a Conciliação tem uma aplicação nova",
Para que o agente acrescente subdomínios, aplicações e jornadas ao domínio sem eu editar YAML.

**Acceptance Criteria:**

**Dado** o pedido de um subdomínio novo
**Quando** a skill roda
**Então** ela confere com `find` que não existe, pergunta propósito, posição no sumário e se há aplicação (nome, lifecycle, repos com papel e plataforma), e monta o rascunho com `sinter new subdomain` (os dois manifestos)

**Dado** o pedido de uma aplicação, dado, regra, doc ou ADR num subdomínio/domínio existente
**Quando** a skill roda
**Então** ela pega o item atual com `sinter get <id> --raw`, acrescenta o pedido sem mexer no resto e passa pelo `apply --dry-run` → confirmação → `apply`

**Dado** um repo citado que não está em `repositories.yaml`
**Quando** a skill monta o rascunho
**Então** ela inclui a alteração de `repositories.yaml` no mesmo rascunho e isso aparece no resumo

**Dado** o pedido de uma jornada
**Quando** a skill roda
**Então** ela pergunta gatilho, resultado e os passos em ordem, liga cada passo a um subdomínio existente (perguntando quando não houver) e pergunta o que acontece se cada passo falhar

**Dado** qualquer gravação
**Quando** termina
**Então** a skill diz o que foi gravado e oferece o próximo passo comum (ex.: "quer descrever as aplicações do Hedge?")

**Dado** os evals de estruturar (subdomínio novo, aplicação nova, jornada nova contra o exemplo-catalogo)
**Quando** rodo
**Então** todos passam e, depois de cada eval, `sinter validate` dá zero erros

### Story 4.5: Instalar as skills no agente

Como arquiteto,
Quero rodar `sinter skills install`,
Para que as skills fiquem disponíveis no meu agente sem copiar pastas à mão.

**Acceptance Criteria:**

**Dado** a CLI instalada
**Quando** rodo `sinter skills install [--project | --user]`
**Então** `sinter-find` e `sinter-domain` são copiadas para `.claude/skills/` do projeto (padrão) ou do usuário, na versão que acompanha a CLI

**Dado** skills já instaladas de versão anterior
**Quando** rodo `install` de novo
**Então** elas são atualizadas e a saída diz de qual versão para qual

**Dado** skills instaladas modificadas localmente
**Quando** rodo `install`
**Então** a CLI não sobrescreve sem `--force` e diz quais arquivos mudaram

**Dado** `--path <pasta>`
**Quando** rodo `install`
**Então** as skills vão para a pasta indicada (outros agentes que seguem o padrão Agent Skills)

### Story 3.7: Formatar o catálogo (`sinter fmt`)

Como arquiteto,
Quero que todo arquivo do catálogo tenha o mesmo formato, com as chaves na mesma ordem,
Para que a IA e quem revisa um PR achem cada bloco sempre no mesmo lugar e o diff mostre só o que mudou.

**Acceptance Criteria:**

**Dado** um manifesto válido com chaves fora de ordem, recuo diferente ou espaços no fim da linha
**Quando** rodo `sinter fmt <arquivo>`
**Então** o arquivo fica com envelope `apiVersion → kind → metadata → spec`, cada bloco na ordem dos campos do Apêndice A (a mesma dos modelos), recuo de 2 espaços, LF e linha final
**E** todo comentário continua junto da chave ou do item a que pertencia

**Dado** um arquivo já formatado
**Quando** rodo `sinter fmt` de novo
**Então** nada muda (idempotente), verificado por teste sobre todo o exemplo-catalogo

**Dado** `sinter fmt --check`
**Quando** há arquivos não formatados
**Então** nada é alterado, os arquivos são listados e o código é `1`

**Dado** `sinter apply`
**Quando** grava um rascunho
**Então** grava a versão formatada, e o `--dry-run` não acusa diferença só de formato como mudança

**Dado** `sinter validate`
**Quando** encontra arquivo não formatado
**Então** dá **aviso**, não erro

**Dado** `sinter fmt` sem argumento
**Quando** rodo na raiz do catálogo
**Então** formata todos os manifestos e diz quantos mudaram (alteração manual, sem commit: o commit continua sendo do `apply`)
