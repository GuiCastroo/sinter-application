---
title: Revisão por rubrica — Architecture Spine Sinter (update 2026-10-17)
target: ../ARCHITECTURE-SPINE.md
inputs: [../.memlog.md, ../../../prds/prd-harness_corp-2026-09-26/prd.md, ../../../../../prd-yaml.md]
date: 2026-10-17
verdict: precisa de revisão antes de virar substrato (não está pronta como "final")
---

# Revisão por rubrica — Spine do Sinter

## Veredito

A espinha é enxuta, o paradigma é claro e a maior parte das ADs tem regra verificável. Não sobrou vocabulário velho no corpo do texto (`DomainStore`, `subdomínio`, `repo do domínio`, `DomainGraph` e `tasks/` no catálogo foram todos trocados). **Mas ela ainda não fecha os pontos de divergência da fatia 1.** Faltam regras para: (1) como Markdown e regras de negócio entram no catálogo, (2) onde mora uma entidade compartilhada e quem é dono de uma relação, (3) separar o grafo oficial do grafo de trabalho, e (4) impedir que alguém contorne a curadoria editando o Git direto. Com isso em aberto, duas histórias implementadas em paralelo vão divergir. O `status: final` está adiantado, até porque a própria espinha liga a um PRD que ainda vai ser atualizado (`binds: 'PRD a atualizar'`).

| Critério da rubrica | Resultado |
| --- | --- |
| Fixa os pontos de divergência reais do nível de baixo | **Parcial**: lacunas em C1, A1, A2, A4 |
| Toda Rule é aplicável e previne a divergência declarada | **Parcial**: AD-3, AD-6, AD-10, AD-13 e AD-15 têm furos (A3, A4, M4) |
| Nada em Deferred permite divergência | **Falha num item**: classificação (M3) |
| Cobre as capacidades da fatia 1 dos PRDs | **Parcial**: progressive disclosure e projeto têm cobertura rasa; regras e glossário ficaram sem kind |
| Toda dimensão estrutural está decidida, adiada ou em aberto | **Parcial**: operação multiusuário, versão do schema do catálogo, CI do catálogo e leitura remota não estão em nenhum dos três estados |
| Sem contradição interna entre ADs | **Parcial**: AD-4 × AD-14, AD-6 × AD-13, AD-2 × AD-15, AD-17 × Convenções, AD-4 × Convenções (nome de arquivo) |

---

## Achados

### C1 — Crítico: o caminho único de escrita não transporta Markdown, e regras de negócio e glossário ficaram sem kind

**Onde:** AD-3, AD-4 e AD-14; Kinds da fatia 1.

- O schema da Proposta (AD-3) só carrega `manifest (AD-4)`. Só que a fatia 1 grava Markdown no catálogo: `docs/` (incluindo "a doc única gerada pela skill"), `business.md`, `solution.md` e `repo.md` das tarefas. Como AD-3 diz que só `approve` escreve, esses arquivos **não têm caminho legal até o catálogo**. Na prática cada time vai improvisar: um grava direto, outro embute o texto no `spec` do `Resource`, um terceiro cria um op novo.
- Os kinds não incluem **regra de negócio** nem **termo de glossário**, que eram itens de conhecimento centrais no PRD do Sinter (FR-2, FR-15, FR-18, UJ-2: "o Confluence diz 30 s, o código usa 10 s") e que o `.sinter/context/rules.md` projeta. Se a regra vive só em Markdown, a curadoria não detecta o conflito, porque AD-3 só compara manifestos por identidade e chave de relação. O resultado é que FR-15 não tem como ser implementado.
- AD-4 diz "Markdown vive em `docs/` e só é alcançado por um `Resource`". AD-14 coloca Markdown em `projects/<id>/` sem `Resource`. As duas ADs se contradizem.

**Correção:** (a) adicionar os kinds `Rule` e `Term`, ou declarar de forma explícita que regras são Markdown e que FR-15 cai para a fatia 2; (b) estender a Proposta com `attachments[]: { path, sha256 }` para arquivos Markdown ligados ao manifesto (`Resource` ou camada), aprovados no mesmo commit; (c) ajustar AD-4 para "Markdown vive em `docs/` ou como camada de `Project`".

### A1 — Alto: a localização de entidade compartilhada e a posse de relação são ambíguas

**Onde:** AD-18, AD-19, AD-22 e o seed do repo do catálogo.

- AD-18 diz que entidades técnicas não têm posse exclusiva, mas o seed obriga `domains/<dominio>/entities/…`. Não há regra que diga em qual domínio fica um microserviço usado por dois domínios (CA02, RF-H07). AD-22 afirma que "a pasta depende só do kind", o que é falso, porque ela também depende do domínio.
- AD-19 coloca a relação em `domains/<domínio da origem>/relations/`. Fica sem resposta quando a origem não está em domínio nenhum: `Project` (`changes`, `impacts`), `Regulation` e `Standard` (`applies_to`), `Organization`.
- O vocabulário herdado tem **pares inversos** (`implements`/`implemented_by`, `precedes`/`follows`, `supersedes`). O mesmo fato pode ser gravado nos dois sentidos, com ids diferentes e donos diferentes. A deduplicação pela chave `(source, type, target)` não pega esse caso.
- O `id = rel-<source>--<type>--<target>` com alvo `unresolved:<pista>` (AD-18) muda quando o alvo é resolvido. Isso renomeia o arquivo e quebra histórico e referências. Além disso, os tipos usam `snake_case`, enquanto a convenção de arquivos é kebab-case.
- Não está decidido se o vínculo entidade → `Resource` (`documented_by` no ERD) é um manifesto `Relation` ou um campo `spec.resources[]`, como no exemplo 13.2 do PRD corporativo.

**Correção:** tornar `spec.homeDomain` obrigatório para kinds técnicos e fazer dele a única regra de pasta, sem posse semântica. Relações cuja origem não está em domínio vão para `relations/` na raiz ou para `projects/<id>/relations/`. Gravar só a direção canônica de cada par inverso (lista em `core/schemas`) e derivar o inverso no grafo. Usar um id de relação estável que não dependa do alvo resolvido, ou exigir `supersede` na resolução. Decidir que todo vínculo com `Resource` é `Relation documented_by`.

### A2 — Alto: o grafo mistura catálogo e staging local, o que quebra o determinismo de AD-6 e a reprodutibilidade do impacto

**Onde:** AD-6, AD-13, AD-20 e AD-21.

- AD-13 monta o `CatalogGraph` com os manifestos **mais as Propostas pendentes do SQLite local**. AD-6 diz que o site estático e as projeções são funções puras do commit do catálogo. Se o site lê "só do grafo", deixa de ser função do commit. A classe "candidato" do impacto (AD-21) também passa a depender da máquina: duas pessoas no mesmo commit recebem respostas diferentes. Isso fere o PRD corporativo §17.4 e CA12.
- O `frescor(idade)` de AD-20 depende do relógio. `task build` no mesmo commit, em dias diferentes, gera um pacote diferente. O desempate da ordenação também não está definido, e AD-6 exige saída estável byte a byte.

**Correção:** ter dois modos explícitos do grafo, `official` (só commit, `approved`) e `working` (commit mais staging, marcado). Projeções, site, `task build` e `.sinter/` usam só `official`. `impact` aceita `--include-candidates` e registra o modo na saída. A idade passa a ser calculada contra o timestamp do `catalogCommit`. O desempate fica fixo (relevância desc, depois `id` asc).

### A3 — Alto: a curadoria pode ser contornada, e a operação multiusuário não está decidida

**Onde:** AD-2, AD-3 e AD-15; dimensão de operações.

- AD-3 proíbe módulos e skills de escreverem, mas **nada impede um humano de editar o YAML e dar push**. O próprio PRD corporativo descreve o Fluxo A como "usuário cria manifesto YAML". Não há verificação no remote (trailers `Sinter-*`, `sinter validate`), então a regra não é aplicável fora da CLI.
- **Dono duplicado:** AD-2 define donos por `CODEOWNERS`, AD-15 define papéis em `people.yaml`. Fica em aberto qual dos dois o `approve` consulta. Com dois arquivos, eles vão divergir.
- **Concorrência entre clones:** o lock de arquivo (AD-3) só protege uma máquina. Duas pessoas aprovando em clones diferentes criam duplicatas com ids diferentes, ou conflito de merge no mesmo arquivo. AD-14 trata isso só para o número da tarefa. FR-4 (commit direto ou branch + PR) também não foi decidido.
- **Versão do schema do catálogo:** AD-7 versiona só o `.sinter/`. Não existe regra para uma CLI antiga escrevendo num catálogo com `apiVersion` ou `sinter.yaml` mais novo.

**Correção:** criar uma AD de operação do catálogo com quatro pontos. (1) `sinter validate --ci` como check obrigatório no remote, que rejeita commit em pasta de conhecimento sem trailers válidos. (2) `people.yaml` como fonte única, com `CODEOWNERS` gerado como projeção (AD-6). (3) `approve` faz fetch e rebase, revalida identidade e conflito no HEAD novo e só então faz push, com modo `direct|pr` em `sinter.yaml`. (4) A CLI recusa escrita quando o `schemaVersion` do catálogo é maior que o suportado, e `sinter migrate` é o único caminho de subida.

### A4 — Alto: o modelo de Projeto e Tarefa está ambíguo

**Onde:** AD-4, AD-14 e as Convenções.

- AD-4 lista o kind `Project`, mas AD-14 define "tarefa = `projects/<id>/` com `context.yaml`". Não fica claro se `context.yaml` é o manifesto `Project` (`apiVersion`, `kind`, `metadata`) ou só uma receita. A convenção "nome do arquivo = `id` + `.yaml`" também é violada por `context.yaml`, `domain.yaml` e `organization.yaml`.
- O `changes[]` da receita não vira `Relation`, mas AD-13 monta o grafo "só a partir dos manifestos". Com isso, RF-G10 (projetos relacionados a uma entidade) e RF-PR09 (conflito entre projetos) ficam sem dado no grafo.
- Os estados da camada não têm onde ficar: Markdown não tem `metadata.status` nem `approval`. Os estados do PRD corporativo (`not_started|in_progress|needs_review|approved|superseded`, §12.11) também não foram adotados nem descartados.
- A escolha de **3 camadas** (`business`, `solution`, `repo`) contra os **7 Markdown** do PRD corporativo (DA06, CA09) não está registrada como decisão.
- Falta prefixo de id para `Project` (tarefas usam `PAG-231`, mas o projeto fica na raiz, sem domínio). A numeração `ADR-NNN` também não tem escopo nem contador definidos.

**Correção:** decidir que `projects/<id>/project.yaml` é o manifesto `Project` (com `spec.recipe` e `spec.layers[{ role, file, status, approval }]`) e que `changes[]` e `impacts[]` são materializados como `Relation`. Registrar "3 camadas em vez de 7 Markdown" como decisão, ou como `[ASSUMPTION]` para validar com o Gui. Fixar `ADR-<CHAVE>-NNN` com contador em `domain.yaml`, igual ao das tarefas. Reescrever a convenção para "manifesto de entidade = `id`.yaml; arquivos de configuração têm nome fixo".

### M1 — Médio: progressive disclosure sem contrato

**Onde:** AD-20 e o mapa de capacidades.

Os níveis 0 a 3 do PRD corporativo (§11), a leitura de metadados sem conteúdo (RF-K04, CA03), a leitura sob demanda por seção (RF-K05, RF-K09, CA04) e o aviso de contexto incompleto (RF-PD07) não estão em nenhuma AD. O score decide a ordem, mas **o que cada nível devolve** não está fixado. A skill `get-domain` e a CLI vão divergir nos campos.

**Correção:** criar uma AD para os níveis de divulgação, com campos fixos por nível em `core/schemas`, `sinter get <id> --level 0..3`, `sinter resource read <id>[#secao]` e a flag `truncated` mais a lista de ponteiros em toda saída cortada por orçamento.

### M2 — Médio: leitura de recurso remoto e conteúdo não confiável não foram decididos

`Resource` aceita URL (seed do catálogo), mas não está definido quem busca o conteúdo na fatia 1 (CLI ou agente), nem com que salvaguardas (timeout, tamanho, redirecionamento, destinos internos; PRD corporativo §16.3). §16.4 (conteúdo como dado, não instrução) também não está em nenhuma AD, e essa é justamente a fatia em que o agente do cliente consome o conteúdo.

**Correção:** decidir que, na fatia 1, a CLI só lê `repo@commit` e arquivos locais, e que URL é só ponteiro devolvido ao agente. Alternativamente, criar uma porta `ResourceFetcher` com limites fixos. Adicionar uma regra em AD-17: a saída `--json` marca o conteúdo de fonte como `untrusted: true`, e as skills tratam esse conteúdo como dado.

### M3 — Médio: um item do Deferred deixa divergir (classificação)

"`classification` pode ser gravado, mas a aplicação fica para depois." Sem regra, um exportador inclui o conteúdo de um recurso `confidential` no `.sinter/` de um repo de código com acesso mais amplo e outro não inclui. Isso diverge e ainda vaza informação.

**Correção:** antecipar uma regra mínima. Projeções (`.sinter/`, exports, site, pacote de tarefa) levam recurso com `classification ≥ confidential` só como ponteiro, nunca o conteúdo.

### M4 — Médio: algumas Rules não são aplicáveis como estão escritas

- **AD-10** diz que o scanner roda "antes de ser enviado a LLM". Na fatia 1 quem lê a fonte e chama o LLM é o agente do cliente, e o Sinter não controla isso. O ponto que dá para garantir é `sinter propose` ou `import` e as projeções. A regra precisa ser reescrita para esse escopo e declarar o limite.
- **AD-17**: "as skills só agem chamando `sinter`", mas a `sinter-documentar` lê repos diretamente. O que importa é "nenhuma skill lê ou escreve catálogo, staging ou `.sinter/`", e a primeira frase deveria ser só essa.
- **AD-5**: evidência `conversation/<id>` aponta para um conteúdo que fica só na máquina de quem conversou (AD-16). Para as outras pessoas, FR-3 ("abre o trecho de origem") não funciona. Isso precisa estar explícito como limitação, ou a evidência precisa de um resumo minimizado aprovado.
- **AD-3**: os ops `create|update|supersede|reject` não cobrem **fusão de identidade** (AD-18: "fundidas por aprovação humana"), desfazer a fusão (RF-I05) nem `deprecate`. Sem um op, cada módulo vai fundir de um jeito. A correção é adicionar `merge`, em que o perdedor vira `superseded` e o id dele entra em `aliases`, e `deprecate`.

### M5 — Médio: suposições não marcadas e cobertura de requisitos

- **Q02 do PRD corporativo** (sigla em vários domínios) foi decidida em silêncio: `Group` tem pai único `Domain` (AD-18). O PRD §5.4 pede para **não** assumir isso sem validar. Marcar como `[ASSUMPTION]`.
- Os estados de identidade `ambiguous` e `candidate` (PRD corporativo §8.3) não aparecem: AD-18 só tem `unresolved`. Definir onde a ambiguidade fica (na Proposta, com candidatos) e que ela nunca chega ao catálogo.
- O `binds: FR-1..FR-37` inclui FR-31..FR-33 (catálogo de skills, agentes e fluxos) e FR-6/FR-7 (Confluence, Google Docs, permissões), mas nenhuma AD os governa e eles não estão no Deferred. O mesmo vale para FR-13 e FR-36 (fatia 2?). Mover para o Deferred ou mapear.
- Há uma **colisão de termo**: no PRD do Sinter, "Catálogo" é a coleção de skills, agentes e fluxos (FR-31), e o monorepo tem `catalog/` para skills. Na espinha, "catálogo" é o repo de conhecimento. A convenção "Textos de interface: termos do Glossário do PRD" reimporta o vocabulário velho (subdomínio, repo do domínio). Renomear `catalog/` do monorepo (ex.: `bundles/`) e fazer a convenção apontar para o glossário do PRD atualizado.
- **Nomes de skill:** a convenção diz `sinter-<verbo>`, mas AD-14 cita `/create-context` e o memlog cita `/get-domain` e `sinter-impacto`, que é substantivo. Escolher um padrão.

### B1 — Baixo

- `status: final` com `binds` apontando para um "PRD a atualizar": rebaixar para `draft` ou registrar a dependência como questão aberta.
- Stack: Node 24 como mínimo, mas o memlog registra `node:sqlite` estável só no Node 26. Confirmar o nível de estabilidade no 24 ou subir o mínimo.
- Repositório não é nó do grafo (vive em `repositories.yaml`), diferente do PRD corporativo (`repository` é entidade). É uma escolha válida, mas sem consulta "entidades deste repo" precisa ficar registrada como decisão.
- A chave de duplicata de relação `(source, type, target)` impede manter histórico com `validFrom` e `validTo` diferentes para o mesmo trio (RF-R08). Ajustar a chave ou usar `supersede`.
- O memlog ainda tem o frontmatter antigo (`scope: … repo do domínio`). É só higiene.

---

## Pontos fortes (manter)

- AD-1, AD-9, AD-17: a separação "skill julga, CLI decide" é a decisão certa e está bem formulada.
- AD-5: a evidência estruturada com `locator` tipado é concreta e testável.
- AD-20: "score calculado, nunca digitado" elimina uma fonte inteira de divergência.
- AD-21: as quatro classes de impacto seguem o PRD corporativo §9.4 e são aplicáveis.
- AD-22: legado como estado, não como pasta, evita a quebra de referências.
- O Deferred é na maior parte honesto (MCP, federado, Backstage, `verified`) e não cria divergência, com exceção de M3.

## Ordem sugerida de correção

1. C1 e A4: modelo de escrita e de projeto. Muda o schema da Proposta e os kinds, então precisa vir antes de qualquer história.
2. A1: pasta, posse e direção de relação.
3. A2: grafo `official` × `working` e o relógio do score.
4. A3: AD de operação do catálogo (CI, dono único, concorrência, versão do schema).
5. M1 a M5 e B1.
