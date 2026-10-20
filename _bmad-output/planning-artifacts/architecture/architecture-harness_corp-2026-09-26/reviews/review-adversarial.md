---
review: adversarial
target: ../ARCHITECTURE-SPINE.md
spine_updated: '2026-10-17'
reviewed: '2026-10-17'
method: pares de unidades um nível abaixo que cumprem todos os ADs ao pé da letra e ainda assim constroem coisas incompatíveis
---

# Revisão adversarial — Architecture Spine do Sinter

## Veredito

A espinha está bem orientada: ela fecha o caminho de escrita, o formato e as portas. Mas ela ainda **não fecha identidade, posse e tempo**. Com os ADs atuais, dá para construir o importador, a curadoria, o `task build`, o impacto e o site de modo que cada um cumpra todas as regras e mesmo assim gerem catálogos duplicados, relações sem pasta definida, rejeições que voltam e projeções que não são determinísticas. Encontrei **16 brechas**: 6 altas, 7 médias e 3 baixas. Duas delas são contradições internas entre ADs, não só lacunas: AD-6 contra AD-20 (frescor depende do relógio) e AD-4 contra AD-16 (evidência de conversa local que não pode ser validada).

Legenda de severidade:
- **Alta:** quebra a fonte da verdade ou o determinismo, e o erro aparece já no primeiro piloto com dois devs.
- **Média:** dois módulos divergem e a correção depois exige migrar dados.
- **Baixa:** atrito ou ambiguidade que um teste de contrato pega cedo.

---

## Brechas altas

### H1 — Frescor depende do relógio, então a projeção não é função pura (contradição AD-6 × AD-20)

- **Par:** `core/scoring` (AD-20) × `core/projection` (`task build`, `.sinter/`, AD-6).
- **Cenário:** AD-20 calcula `frescor(idade, meia-vida)`, e a idade é medida contra "agora". AD-6 exige que a projeção seja função pura de (commit do catálogo, `context.yaml`, versão do gerador). Se dois devs rodam `sinter task build PAG-231` no mesmo commit com três dias de diferença, a ordem por relevância muda e o corte por orçamento tira outro recurso. O `.sinter/tasks/PAG-231/` sai diferente byte a byte, e o hash do cabeçalho acusa "edição manual" num arquivo que ninguém editou. As duas implementações cumprem seu AD, mas são incompatíveis entre si.
- **Regra proposta (novo item em AD-20):**
  > O instante de referência do score é a data do commit do catálogo usado na projeção (`committer date` de `catalogCommit` ou, na falta dele, do `HEAD` lido), nunca o relógio da máquina. `core/scoring` recebe `asOf` como parâmetro obrigatório, e nenhuma função de `core` lê o relógio do sistema. Empates de relevância são desfeitos por `id` em ordem lexicográfica.

### H2 — Entidade técnica não tem domínio dono, então pasta e dono da relação ficam indefinidos

- **Par:** importador do domínio PAG × importador do domínio CLI (ou importador × curadoria).
- **Cenário:** AD-18 tira `Application`, `Microservice`, `Api` etc. da hierarquia `parent`. Elas se ligam "só por relação, sem posse exclusiva". Mas o catálogo guarda essas entidades em `domains/<dominio>/entities/`, e AD-19 manda gravar a relação na pasta do "domínio da origem". Quando dois domínios documentam o mesmo `app-gateway`, cada importador cria o arquivo na própria pasta. Os dois cumprem AD-4 (um arquivo por manifesto), mas agora existem dois arquivos com o mesmo `id`. O `CatalogStore` de cada dev resolve o `id` para um caminho diferente, e a pasta de `rel-app-gateway--calls--api-x` depende de quem rodou primeiro.
- **Regra proposta (AD-18, nova frase):**
  > Toda entidade fora da raiz do catálogo tem exatamente um domínio dono, em `metadata.domain`. Ele é obrigatório e validado, e é o único fator que decide a pasta (`domains/<metadata.domain>/<pasta do kind>/<id>.yaml`). Entidades compartilhadas entre domínios continuam com um único dono, e os outros domínios se ligam a elas por relação. Trocar o dono é uma Proposta `op: update` aprovada pelos dois donos (CODEOWNERS de origem e de destino).
- **Complemento (AD-19):**
  > Relações cuja origem não tem domínio (`Organization`, `Regulation`, `Standard`, `Project`) ficam em `relations/` na raiz do catálogo, ou em `projects/<id>/relations/` quando a origem é um `Project`.

### H3 — Dois devs aprovando a mesma descoberta em paralelo geram duplicata ou conflito sem regra

- **Par:** dev A × dev B, cada um com seu staging SQLite local (AD-2, AD-3).
- **Cenário:** A e B importam o mesmo repo. A deduplicação de AD-3 só compara contra o catálogo **local**, e o lock de AD-3 é um lock de arquivo **na máquina**. Os dois aprovam: A grava `app-pagamentos` e B grava `app-pagamentos-api`, porque o slug veio de outra pista, ou o mesmo `id` com conteúdo diferente. No push, ou o Git aceita as duas entidades (duplicata silenciosa) ou dá conflito add/add num YAML. AD-14 define o que fazer no conflito de push só para o número de tarefa. Para aprovação, nada.
- **Regra proposta (AD-3, nova frase):**
  > `approve` executa: fetch do remote → rebase local → nova detecção de duplicata e conflito contra o `HEAD` atualizado → commit → push. Se o push falhar, repete o ciclo; se a revalidação achar duplicata, a aprovação vira Proposta de fusão e não é gravada. Nenhum commit de aprovação é publicado sem ter sido revalidado contra o remote. O `id` de uma entidade nova é derivado de forma determinística em `core/catalog/deriveId(kind, name, externalIds)`. Quando há `externalIds`, o `id` vem deles; sem eles, vem do nome normalizado. Por isso, a mesma descoberta feita por dois devs gera o mesmo caminho e colide no Git em vez de virar duplicata.

### H4 — Grafo com candidatos locais alimenta projeções que deveriam ser iguais para todos (AD-13 × AD-6)

- **Par:** site estático / `.sinter/context/neighbors` × `sinter impact` interativo.
- **Cenário:** AD-13 monta o `CatalogGraph` com os manifestos **mais as Propostas pendentes como `candidate`**. Só que as Propostas vivem no SQLite de cada máquina (AD-2). O site, o `.sinter/` e o impacto são "só leituras" desse grafo. Assim, o site gerado por A mostra candidatos que o de B não mostra, e a projeção deixa de ser função de (commit, `context.yaml`, gerador). Isso fere AD-6 e o próprio objetivo de AD-13 ("mesmos dados").
- **Regra proposta (AD-13):**
  > `buildCatalogGraph(commit, { includeStaging })` tem `includeStaging=false` por padrão. Projeções (AD-6) sempre usam `false`. Consultas interativas (`impact`, `query`) só incluem candidatos com `--with-staging`, e a saída declara o hash do staging usado. Candidatos nunca entram em arquivo gerado.

### H5 — Rejeição "até a `version` mudar" volta a cada commit do repo (AD-19 × AD-5)

- **Par:** importador / inferência de grafo × curadoria.
- **Cenário:** AD-5 define `version` como "o commit ou a revisão". Qualquer commit novo no repo de código troca o hash, mesmo que o arquivo citado não tenha mudado. Pelo AD-19, a relação rejeitada volta como Proposta em **toda** importação, e a rejeição perde o efeito. Se o importador interpretar `version` como hash do commit e a curadoria como hash do arquivo, as duas leituras cumprem o texto e se contradizem.
- **Regra proposta (AD-5 e AD-19):**
  > Cada evidência guarda também `contentHash`: o hash normalizado do trecho apontado pelo `locator`, ou do arquivo inteiro quando não há trecho. Item `rejected` só volta como Proposta se o `contentHash` de alguma evidência mudar ou se surgir evidência de uma fonte nova. A mudança de `version` sozinha não reabre. A mesma regra vale para entidades `rejected`, casadas por identidade (AD-18).

### H6 — `update` sem base nem granularidade: a importação apaga a curadoria humana

- **Par:** importador (reprocessamento) × curador humano (que editou `aliases`, `lifecycle`, descrição).
- **Cenário:** AD-3 diz que a Proposta carrega `manifest`, mas não diz se é o manifesto inteiro ou um patch, nem contra qual versão. Um importador que manda o manifesto completo cumpre AD-3. Se a curadoria aprova "aplicando o manifesto", sobrescreve os `aliases` e o `spec.lifecycle` que um humano tinha aprovado. Outro curador que faz merge por campo também cumpre AD-3. Resultado: duas semânticas incompatíveis de `update`. Além disso, uma Proposta criada contra o commit X pode ser aprovada sobre o commit Y.
- **Regra proposta (AD-3):**
  > Proposta `op: update` carrega `baseCommit` e um patch por campo (JSON Merge Patch sobre `metadata`/`spec`), nunca o manifesto inteiro. Se o arquivo mudou desde `baseCommit` nos mesmos campos, a curadoria marca conflito. Importação e inferência nunca propõem mudança em campos de posse humana (`aliases`, `spec.lifecycle`, `spec.platform`, `approval`, `metadata.domain`, `pinned`), que ficam listados em `core/schemas`. Propostas pendentes com a mesma chave (identidade ou `(source, type, target)`) são fundidas em uma só no staging, com a união das evidências.

---

## Brechas médias

### M1 — Relação com alvo `unresolved` muda de `id` ao ser resolvida

- **Par:** importador (que "reavalia a cada importação", AD-18) × curadoria (dona da deduplicação, AD-3).
- **Cenário:** `id = rel-<source>--<type>--<target>`, e o alvo pode ser `unresolved:<pista>`, uma pista em texto livre com `:` e espaços. Quando a pista é resolvida para `api-cobranca`, o `id` e o nome do arquivo mudam. A rejeição gravada no `id` antigo não casa mais, e o histórico Git vira delete + add. Também não está dito quem resolve: o importador reescreve o alvo (fora da curadoria) ou abre uma Proposta?
- **Regra proposta (AD-18/AD-19):**
  > Alvo desconhecido vira um `id` normalizado `unr-<slug-da-pista>`. Resolver um `unresolved` é sempre uma Proposta `op: supersede` com destino a relação nova. A relação antiga fica `superseded`, com `spec.supersededBy`, e a rejeição migra junto. O importador só detecta candidatos à resolução; quem grava é `core/curation`.

### M2 — Vocabulário com tipos inversos cria duas relações para o mesmo fato

- **Par:** dono do domínio PAG (origem) × dono do domínio CLI (alvo).
- **Cenário:** se o vocabulário de AD-19 tiver `calls` e `called_by`, ou `publishes` e `published_by`, o PAG grava `rel-ms-a--calls--api-b` e o CLI grava `rel-api-b--called_by--ms-a`. A chave de duplicata `(source, type, target)` não detecta isso. O impacto conta a dependência em dobro, e cada fato tem dois donos.
- **Regra proposta (AD-19):**
  > O vocabulário de `core/schemas` só tem tipos na direção canônica (origem = quem consome, chama, publica, depende ou é governado). Tipos inversos não existem como `type`; são só rótulos de leitura gerados pelo grafo. A curadoria rejeita uma Proposta que traga um tipo fora do vocabulário canônico.

### M3 — Relação em outro domínio sem aprovação do domínio alvo

- **Par:** CODEOWNERS de origem × time dono do alvo.
- **Cenário:** pelo AD-19, quem aprova é o dono da origem. O PAG pode então declarar `governed_by reg-lgpd` ou `modernized_by ms-novo` (alvo no domínio CLI) sem que o CLI saiba. Isso é ok para `calls`. Para `modernized_by`, o PAG está decidindo o roadmap do CLI.
- **Regra proposta (AD-19):**
  > Para tipos marcados como `bilateral` no vocabulário (no mínimo `modernized_by`, `replaces` e `owned_by`), a aprovação exige trailer `Sinter-Approved-By` de alguém com papel no domínio de origem **e** no domínio de destino. Para os demais tipos, basta o dono da origem.

### M4 — Fusão de entidades não tem operação nem efeito definido

- **Par:** curador que funde `app-pag` com `app-pagamentos` × relações e tarefas que citam o `id` perdedor.
- **Cenário:** AD-18 permite fusão "só por aprovação humana", mas AD-3 só tem `create|update|supersede|reject`. Um dev pode implementar a fusão como `supersede` com alias; outro, como reescrita de todas as relações. Os `id`s de relação embutem o `id` da entidade (AD-19), então a fusão renomeia N arquivos de outros domínios.
- **Regra proposta (AD-3/AD-18):**
  > A fusão é `op: merge { survivor, merged[] }`. O `id` perdedor vira alias do sobrevivente e o arquivo perdedor fica `superseded`, com `spec.supersededBy`. As relações que citam o perdedor são reescritas no mesmo commit, por `core/curation`, como supersede de cada relação. As referências em `context.yaml` e camadas são resolvidas por alias na leitura, sem reescrita.

### M5 — Duas travessias: `task build` (só `approved`) × impacto (inclui `candidate`) × `.sinter/neighbors` (indefinida)

- **Par:** `core/tasks` × `core/graph/impact` × `core/projection`.
- **Cenário:** AD-14 percorre só `approved`. AD-21 percorre `candidate` e `unresolved`, filtra por `lifecycle` e não fala de `validFrom/validTo` nem de `phase`. Os vizinhos do `.sinter/context/neighbors` não têm regra nenhuma. Três implementações de travessia com filtros diferentes cumprem tudo, e cada uma decide sozinha se segue um `modernized_by phase: planned` ou uma relação com `validTo` no passado, ou se atravessa uma entidade `deprecated`.
- **Regra proposta (AD-13, nova frase):**
  > Existe uma única função `core/graph/traverse(graph, start[], policy)`. `TraversalPolicy` é um schema de `core/schemas`: `statuses[]`, `relationTypes[]`, `maxDepth`, `lifecycles[]`, `asOf` (para `validFrom/validTo`), `phases[]` e `throughDeprecated: bool`. `task build`, impacto, vizinhos do `.sinter/` e o site só montam políticas, e as padrão ficam nomeadas e versionadas em `core/graph/policies` (`TASK`, `IMPACT`, `NEIGHBORS`). Uma relação `approved` cujo extremo esteja `deprecated|superseded|rejected` não conta como `approved` na travessia.

### M6 — Evidência `conversation/<id>` aponta para algo que só existe numa máquina (contradição AD-4 × AD-16)

- **Par:** dev que aprova uma decisão vinda de conversa × `sinter validate` no CI ou na máquina de outro dev.
- **Cenário:** AD-16 mantém a conversa no workspace local e manda a evidência apontar para `conversation/<id>`. AD-4 diz que `sinter validate` falha se um `ref` não existir. Na máquina de B, ou no CI, o catálogo é inválido por construção. Se um dev relaxar o `validate`, outro vai mantê-lo estrito.
- **Regra proposta (AD-5/AD-16):**
  > Evidência de conversa aponta para um `Resource` `type: meeting|conversation` aprovado no catálogo, que guarda o conteúdo minimizado. `conversation/<id>` só pode aparecer como `locator` dentro desse `Resource` e é marcado `localOnly: true`; `validate` não exige que o alvo `localOnly` exista. Nenhuma `evidence.source` aponta direto para o workspace local.

### M7 — `catalogCommit` da receita × `HEAD` no build; e quem grava a tarefa

- **Par:** `sinter task new` / `task build` × `approve` (AD-3).
- **Cenário:** a receita fixa `catalogCommit`, mas AD-6 diz "commit do catálogo" sem dizer qual. Um `task build` que lê `HEAD` e outro que lê `catalogCommit` cumprem AD-6 e geram pacotes diferentes. Além disso, `task new` cria `projects/<id>/` e incrementa `nextTaskNumber` num commit, ou seja, escreve no catálogo, e isso é um segundo caminho de escrita fora de AD-3. A aprovação por camada (`business.md` etc.) também não tem onde guardar estado: Markdown não tem `status` (AD-4), e AD-4 diz que Markdown só é alcançado por `Resource`.
- **Regra proposta (AD-14):**
  > `task build` lê o catálogo **em `catalogCommit`** (worktree ou `git show`), nunca o `HEAD`. Atualizar `catalogCommit` é uma Proposta `op: update` na receita. Criar tarefa, incrementar `nextTaskNumber` e aprovar camada são operações de `core/curation` (o mesmo `approve`, com seus trailers). O estado de cada camada fica no manifesto `Project` (`spec.layers.<papel>: { file, status, approval }`); o Markdown da camada não carrega status. Tarefa que toca vários domínios usa o contador do domínio do `primary`.

---

## Brechas baixas

### L1 — Renumeração de tarefa depois que o número já vazou

- **Cenário:** AD-14 renumera em conflito de push, mas o número já pode estar em `.sinter/tasks/<id>/`, em nome de branch e no trailer `Sinter-Item` de um commit local.
- **Regra proposta (AD-14):**
  > Até o push dar certo, o número é provisório (`PAG-~231`) e não é projetado. `task build` e `Sinter-Item` só usam número confirmado no remote. Depois do push, um número nunca é renumerado.

### L2 — `ADR-NNN` sem contador nem prefixo coerente

- **Cenário:** decisões usam `ADR-NNN`, fora do padrão "prefixo por kind + slug" e sem contador definido. Dois domínios criam `ADR-007`.
- **Regra proposta (Convenções):**
  > O `id` de `Decision` é `adr-<chave-do-domínio>-<n>`, com contador `nextDecisionNumber` em `domain.yaml` e as mesmas regras de L1. `ADR-NNN` é só o rótulo de exibição.

### L3 — Arquivos de configuração do catálogo e versão mínima da CLI

- **Cenário:** `repositories.yaml`, `people.yaml`, `scoring.yaml` e `organization.yaml` são escritos por quem? Um dev com CLI antiga grava manifestos de schema antigo, e dois geradores de versões diferentes produzem `.sinter/` com bytes diferentes no mesmo repo.
- **Regra proposta (AD-3/AD-7):**
  > Os arquivos de configuração da raiz e `domain.yaml` só mudam via Proposta `op: update` aprovada (`origin: config`), pelo mesmo `approve`. `sinter.yaml` do catálogo declara `minCliVersion` e `generatorVersion`. A CLI recusa escrever e projetar abaixo do mínimo, e a projeção usa a versão de gerador fixada no catálogo, não a instalada.

---

## Pares testados que ficaram fechados

- **Skill × skill gravando arquivo:** fechado por AD-17 (só CLI `--json`).
- **UI × Git direto:** fechado por AD-12.
- **Dois motores de token:** fechado por AD-14 e pelas convenções (`countTokens` único). Falta só dizer **o que** se conta: o texto renderizado final, incluindo os ponteiros. Sugestão: "`countTokens` recebe o texto final da projeção, ponteiros incluídos".
- **Score gravado no manifesto:** fechado por AD-20, a não ser pelo `asOf` (H1).
- **Formato de Graphify vazando:** fechado por AD-8. Uma recomendação: o mapeamento do tipo de aresta do Graphify para o vocabulário de AD-19 deveria ser uma tabela única em `core/schemas`, para que os dois adaptadores (`graphify` e `sinter-documentar`) não mapeiem `calls` de formas diferentes.

## Prioridade sugerida

1. H1, H4 (determinismo): são só uma frase cada e não mexem em dados.
2. H2, H3, H6 (identidade, posse e concorrência): precisam entrar antes do primeiro importador.
3. H5, M1, M4 (ciclo de vida de rejeição, resolução e fusão).
4. M5, M7 (travessia única e `catalogCommit`).
5. Restante.
