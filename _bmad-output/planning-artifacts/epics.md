---
stepsCompleted: [1, 2]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-harness_corp-2026-09-26/prd.md
  - _bmad-output/planning-artifacts/prds/prd-harness_corp-2026-09-26/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-harness_corp-2026-09-26/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/ux-designs/ux-harness_corp-2026-09-26/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-harness_corp-2026-09-26/EXPERIENCE.md
---

# Sinter - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Sinter, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: O arquiteto pode criar um domínio (nome, descrição, local do repo do domínio novo ou existente); o repo criado contém todas as seções do padrão de documentação.
FR2: O sistema classifica cada item de conhecimento em exatamente uma seção do padrão; itens sem seção vão para a curadoria e não são aprovados sem escolha de seção.
FR3: Todo item de conhecimento registra proveniência; a interface abre o trecho de origem; item sem fonte só é aprovado com justificativa.
FR4: Toda alteração aprovada no repo do domínio vira commit (branch/PR ou direto, conforme configuração), com o autor da aprovação no histórico.
FR5: O arquiteto conecta repos Git por caminho local ou URL; repos sem permissão aparecem como "sem acesso".
FR6: O arquiteto conecta espaços do Confluence, pastas do Google Docs e arquivos PDF e DOCX, com status por documento.
FR7: O sistema só usa conteúdo que o usuário que conectou a fonte pode ler.
FR8: O sistema detecta segredos e nunca os grava no repo do domínio, no `.sinter/` ou em exports; cada segredo gera alerta com a localização.
FR9: O arquiteto reprocessa uma fonte ou o domínio; itens aprovados não são sobrescritos, mudanças viram propostas.
FR10: O sistema gera o mapa do domínio (sistemas, integrações API/evento/fila/arquivo, donos), cada integração com proveniência e marca extraída/inferida.
FR11: Qualquer papel navega o mapa (zoom, busca, filtro por tipo, foco num sistema e seus vizinhos) e vê o painel do sistema selecionado.
FR12: O arquiteto confirma, corrige ou descarta integrações inferidas; descartadas não voltam sem mudança na fonte.
FR13: Numa conversa no modo solução, o sistema mostra o mapa atual e o proposto, destacando o que foi adicionado, alterado e removido.
FR14: A fila de curadoria agrupa propostas por seção, com duplicatas agrupadas; aprovar, editar, descartar ou aprovar em lote.
FR15: Conflitos mostram as versões lado a lado com as fontes; escolher, escrever nova ou registrar decisão (ADR); conflito aberto impede aprovação.
FR16: Toda aprovação registra quem, quando, o quê e com base em qual fonte.
FR17: O usuário inicia uma conversa guiada em um domínio, no modo processo, funcionalidade ou solução.
FR18: O facilitador usa o repo do domínio; aponta conflitos com decisões e regras aprovadas citando o item; usa o glossário e propõe termos novos.
FR19: A conversa gera propostas de itens e, no modo funcionalidade, PRD e tarefas; tudo entra na curadoria.
FR20: Uma conversa pode ter participantes de papéis diferentes, em sequência.
FR21: O usuário cria uma tarefa a partir de uma conversa, de um PRD colado ou de texto livre, associada a um domínio.
FR22: O sistema monta o pacote de contexto inicial (sistemas afetados, integrações, contratos, regras, decisões), com origem de cada elemento e respeitando o orçamento.
FR23: Cada papel adiciona e aprova a sua camada (negócio, solução, repo); o pacote mostra camadas, donos e status.
FR24: O dev traz o pacote da tarefa para o repo pela CLI; o pacote vai para o `.sinter/` e os exports são atualizados.
FR25: Criar um repo novo associado a um domínio já com `.sinter/` completo e exports gerados.
FR26: Gerar o `.sinter/` para um repo existente do domínio, entregue como PR.
FR27: Gerar, a partir do `.sinter/`, AGENTS.md (com aninhados quando útil), CLAUDE.md, regras do Cursor e instruções do Copilot; mesma entrada gera mesma saída; aviso "gerado pelo Sinter, não edite".
FR28: Sincronizar o `.sinter/` com o repo do domínio pela CLI, mostrando diferenças e sinalizando edições manuais em exports.
FR29: `.sinter/` organizado para carregar pouco no início (AGENTS.md curto, skills sob demanda); limites do NFR-3 com aviso; interface mostra consumo contra orçamento.
FR30: A CLI oferece `init`, `task pull`, `sync`, `export` e `status`, todos sem o app aberto e com saída `--json`.
FR31: Navegar o catálogo por papel e tipo e instalar itens num domínio ou repo; itens do domínio entram no `.sinter/` dos repos.
FR32: O arquiteto publica skills, agentes e fluxos no catálogo da empresa, com autor, versão e licença.
FR33: O catálogo vem com os fluxos "nova feature" e "bugfix", que usam o pacote de contexto.
FR34: Navegar entre os níveis Empresa, Domínio, Sistema e Componente, mantendo a seleção ao descer (no MVP o nível Empresa só lista domínios).
FR35: No nível Domínio, alternar entre Mundo, Grafo e Caixas, com os mesmos dados, a mesma seleção e as mesmas cores de subdomínio; o Mundo respeita redução de movimento.
FR36: Exportar a visão Caixas e o mapa de um sistema em C4 (Structurizr), SVG e Markdown.
FR37: Anexar à conversa arquivos, páginas do Confluence/Google Docs, links e itens do domínio (`@`), com estado por anexo, confirmação do que foi extraído e proveniência apontando para o anexo.

### NonFunctional Requirements

NFR1: Local-first; nenhum dado sai da máquina ou da rede do cliente, exceto chamadas ao provedor de LLM escolhido.
NFR2: O cliente escolhe provedor e modelo de LLM, incluindo modelos locais.
NFR3: AGENTS.md raiz com limite de tamanho e orçamento por camada do pacote de contexto (referência: AGENTS.md ~150 linhas, pacote ~5 mil tokens).
NFR4: `.sinter/` e exports funcionam sem o Sinter instalado.
NFR5: Exports reprodutíveis (mesma entrada, mesma saída).
NFR6: Domínio com até 50 repos e 500 documentos tem o mapa inicial em menos de 30 minutos numa máquina de desenvolvedor comum.
NFR7: 100% dos itens aprovados com proveniência ou justificativa.
NFR8: Nenhum segredo detectado aparece no repo do domínio, no `.sinter/` ou em exports.
NFR9: Interface em português e inglês.
NFR10: Mapa legível e navegável com 50 sistemas; arquiteto novo cria um domínio e vê o mapa sem ajuda.

### Additional Requirements

- **Sem starter template:** monorepo pnpm criado do zero com `packages/core`, `packages/adapters/*`, `packages/server`, `packages/ui`, `packages/cli` e `catalog/` (AD-1). Deve ser a primeira história do Epic 1.
- **Spike prioritário:** validar o Graphify (`graphifyy` 0.9.x via processo filho, lendo `graph.json`) em repos com integrações entre serviços, atrás da porta `GraphEngine`; se falhar, avaliar codebase-memory-mcp ou Cognee (Deferred da arquitetura).
- Direção de dependência do hexágono verificável (lint de imports): `core` não importa pacote do projeto nem SDK de I/O (AD-1).
- SQLite local (`node:sqlite`) é só cache, fila e staging; tem que ser reconstruível a partir do repo do domínio (AD-2).
- Schema único de Proposta; só `core/curation` faz `approve` e escreve no repo do domínio; lock de escrita no `DomainStore` (AD-3).
- Schema do item de conhecimento (Markdown + frontmatter com `id`, `kind`, `subject`, `status`, `provenance[]`, `approval`) validado na escrita e na leitura (AD-4).
- Proveniência `{ sourceId, locator, version, extraction }` com formatos de locator por tipo de fonte (AD-5).
- Projeções puras e determinísticas com cabeçalho e hash para detectar edição manual (AD-6); `.sinter/` com `schemaVersion` e migração em `sync` (AD-7).
- Sete portas: `DomainStore`, `SourceConnector`, `DocumentExtractor`, `GraphEngine`, `LlmProvider`, `SecretScanner`, `Exporter` (AD-8).
- LLM via Vercel AI SDK 6 com prompts versionados em `core/prompts`; saída só como Proposta; conteúdo mascarado pelo `SecretScanner` antes (AD-9, AD-10, betterleaks).
- Processo único Node; `sinter ui` sobe Hono em `127.0.0.1:4317`; fila de jobs persistida e retomável (AD-11).
- UI acessa dados só por RPC tipado com schemas do core; envelope de erro padrão (AD-12).
- `DomainGraph` único para as três visões; ordem e cor de subdomínios em `domain.yaml` (AD-13).
- Tarefas em `tasks/<id>/` no repo do domínio; numeração por `nextTaskNumber` com renumeração em conflito de push; `countTokens` único (AD-14).
- Identidade = git user; papéis em `people.yaml`; trailers de commit na aprovação (AD-15).
- Conversas e anexos no workspace local `~/.sinter/workspaces`; personas derivadas do BMAD (MIT) vendorizadas com atribuição, sem usar o nome "BMad" (AD-16).
- `sinter doctor` verifica Node 24+, git, uv/graphify e betterleaks.
- Logs JSON lines sem conteúdo das fontes; configuração do usuário em `~/.sinter/config.toml`, com chaves via variável de ambiente ou keychain.
- Testes e demos só com repos open source ou sintéticos (restrição de PI).

### UX Design Requirements

UX-DR1: Implementar os tokens do DESIGN.md (cores de superfície, texto, neon, esmaltes de integração, conflito, 8 cores de subdomínio, tipografia Optima/Avenir/Menlo, raios, espaçamento) como tema único do app.
UX-DR2: Shell do app em quatro colunas: trilho de navegação 76 px (Mapa, Curadoria com contador, Conversas, Tarefas, Catálogo; item ativo com filete neon), lista 260 px, área de trabalho, painel de detalhe 320 px; barra superior com marca, breadcrumb, seletor de nível e seletor de visão.
UX-DR3: Componente cartão de sistema com badge de tecnologia, nome, stack, ponto de aprovado e variantes foco, inferido, sem acesso e fora do foco.
UX-DR4: Componente grupo de subdomínio (caixa com cor, nome e contagem) e rótulo de integração em pílula, com integrações agregadas por quantidade e tipo.
UX-DR5: Visão Mundo em 3D: globo com constelações por subdomínio, estrelas proporcionais ao número de integrações, arrastar para girar, clicar para selecionar, voar até a constelação, rotação lenta com pausa e respeito a `prefers-reduced-motion`.
UX-DR6: Visão Grafo (constelação 2D) com halos por subdomínio, arestas entre subdomínios em cinza, inferidas como partículas, sem acesso tracejado e painel de resumo do domínio.
UX-DR7: Visão Caixas (estilo C4) com subdomínios contendo sistemas e integrações agregadas, com exportação.
UX-DR8: Mapa do sistema com fluxo passo a passo: marcadores numerados, passo atual em neon, esmaecimento de quem está fora do fluxo, barra inferior com Voltar e Próximo, camadas (Tecnologia, Status, Donos, Regras), minimapa e zoom.
UX-DR9: Tela de Curadoria: abas Conflitos, Propostas e Segredos; fila agrupada; comparação lado a lado com autor, idade e trecho; "Quem depende desta regra"; painel de decisão com 4 opções, sugestão pré-selecionada e justificativa; "Aprovar e próximo".
UX-DR10: Tela de Conversa guiada: seletor de modo, lista de conversas, thread com citações de ADR em caixa de conflito, chips de sistemas afetados, respostas rápidas, painel com mapa atual vs proposto e artefatos em produção com status e "Enviar para curadoria".
UX-DR11: Anexos no chat: botão `+` com menu de fontes, arrastar e soltar, chips pendentes com estado (lendo, lido, falhou com motivo), menção `@`.
UX-DR12: Tela de Tarefa: linha do bastão com camadas (feita, atual, aguardando), itens por camada, nota livre, "Aprovar camada e passar para…", árvore do `.sinter/` com novo/alterado/regerado, medidor de orçamento por camada e comando copiável.
UX-DR13: Saída da CLI no mesmo código de cores (neon para aplicado, âmbar para atenção, cobalto para exports), prefixos `+`, `~` e `!` com significado sem depender de cor.
UX-DR14: Estados: domínio vazio com convite, processamento com estrelas surgindo e progresso, sem acesso com "Pedir acesso", inferida, conflito aberto, anexo com falha, camada aguardando, segredo detectado (sem mostrar o valor), export editado à mão.
UX-DR15: Acessibilidade: tudo do canvas também pela lista e pelo painel; foco de teclado visível em neon; nada comunicado só por cor; atalhos (`/`, `1` `2` `3`, `[` `]`, `a`).
UX-DR16: Microcopy conforme o Voice and Tone do EXPERIENCE.md e os termos do Glossário do PRD; interface em português e inglês.
UX-DR17: Desktop a partir de 1280 px; entre 1280 e 1440 px o painel de detalhe vira gaveta; abaixo, aviso com leitura apenas.

### FR Coverage Map

FR1: Epic 1 - Criar domínio e repo do domínio no padrão
FR2: Epic 2 - Classificação em uma seção do padrão
FR3: Epic 2 - Proveniência obrigatória
FR4: Epic 1 - Alterações aprovadas viram commit
FR5: Epic 1 - Conectar repos Git
FR6: Epic 2 - Conectar Confluence, Google Docs, PDF, DOCX
FR7: Epic 2 - Respeitar permissões das fontes
FR8: Epic 1 - Bloquear segredos
FR9: Epic 2 - Reprocessar fontes sem sobrescrever aprovados
FR10: Epic 1 - Gerar o mapa do domínio
FR11: Epic 1 - Navegar o mapa
FR12: Epic 2 - Confirmar ou descartar inferências
FR13: Epic 6 - Mapa atual vs proposto na conversa
FR14: Epic 2 - Fila de curadoria
FR15: Epic 2 - Resolver conflitos
FR16: Epic 2 - Registro de aprovação
FR17: Epic 6 - Conversa em um modo
FR18: Epic 6 - Conversa ancorada no domínio
FR19: Epic 6 - Saídas estruturadas da conversa
FR20: Epic 6 - Vários papéis em sequência
FR21: Epic 5 - Criar tarefa
FR22: Epic 5 - Pacote de contexto inicial
FR23: Epic 5 - Camadas por papel
FR24: Epic 5 - Entregar a tarefa ao repo
FR25: Epic 4 - Projeto novo com .sinter/
FR26: Epic 4 - .sinter/ em repo existente
FR27: Epic 4 - Gerar exports
FR28: Epic 4 - Sincronizar
FR29: Epic 4 - Contexto disponível, não todo carregado
FR30: Epic 4 - Comandos essenciais da CLI
FR31: Epic 4 - Navegar e instalar do catálogo
FR32: Epic 4 - Publicar no catálogo
FR33: Epic 4 - Fluxos de partida
FR34: Epic 3 - Níveis de zoom
FR35: Epic 3 - Três visões do domínio
FR36: Epic 3 - Exportar a visão
FR37: Epic 6 - Anexos na conversa

## Epic List

### Epic 1: O primeiro mapa do domínio
O Rafael instala o Sinter, cria o domínio Pagamentos, aponta os repos e vê o mapa dos sistemas e integrações no app local, sem segredo vazando. Inclui o esqueleto do monorepo e o spike do Graphify.
**FRs covered:** FR1, FR4, FR5, FR8, FR10, FR11
**NFRs:** NFR1, NFR6, NFR8

### Epic 2: Documentos e curadoria anti-lama
O Rafael conecta Confluence, Google Docs, PDF e DOCX; o Sinter propõe regras, padrões e integrações; ele resolve conflitos e aprova, e cada aprovação vira commit com proveniência.
**FRs covered:** FR2, FR3, FR6, FR7, FR9, FR12, FR14, FR15, FR16
**NFRs:** NFR2, NFR7, NFR8

### Epic 3: O domínio em três visões
Qualquer papel navega pelos níveis e alterna entre Mundo 3D, Grafo e Caixas; vê o mapa do sistema com fluxo passo a passo; exporta em C4, SVG e Markdown.
**FRs covered:** FR34, FR35, FR36
**NFRs:** NFR9, NFR10

### Epic 4: Repo pronto para decolar
Diego e Bia recebem repos com `.sinter/` e exports para Claude, Cursor, Copilot e AGENTS.md; usam `init`, `sync`, `status` e `export`; instalam e publicam skills, agentes e fluxos no catálogo.
**FRs covered:** FR25, FR26, FR27, FR28, FR29, FR30, FR31, FR32, FR33
**NFRs:** NFR3, NFR4, NFR5

### Epic 5: A tarefa que passa de mão em mão
Uma tarefa é criada, cada papel adiciona e aprova a sua camada, e a Bia recebe o pacote com `sinter task pull`.
**FRs covered:** FR21, FR22, FR23, FR24
**NFRs:** NFR3

### Epic 6: Conversas guiadas
Carla e Rafael desenham processo, funcionalidade ou solução com o facilitador, anexam documentos, veem o mapa atual vs proposto e geram propostas, PRD e tarefas.
**FRs covered:** FR13, FR17, FR18, FR19, FR20, FR37
**NFRs:** NFR2, NFR8

## Epic 1: O primeiro mapa do domínio

O Rafael instala o Sinter, cria o domínio Pagamentos, aponta os repos e vê o mapa dos sistemas e integrações no app local, sem segredo vazando. Inclui o esqueleto do monorepo e o spike do Graphify.

### Story 1.1: Sinter instalável com diagnóstico do ambiente

As a arquiteto que vai experimentar o Sinter,
I want instalar o `sinter` e rodar `sinter doctor`,
So that eu saiba em um comando se minha máquina tem tudo o que o Sinter precisa.

**Acceptance Criteria:**

**Given** o monorepo pnpm com `packages/core`, `packages/adapters`, `packages/server`, `packages/ui`, `packages/cli` e `catalog/` (AD-1)
**When** o pacote é instalado globalmente e o usuário roda `sinter --version`
**Then** a versão é exibida e o comando termina com código 0
**And** `sinter doctor` verifica Node 24+, git, uv/graphify e betterleaks, mostrando `+` para o que está ok e `!` com instrução de instalação para o que falta
**And** `sinter doctor --json` devolve o mesmo resultado no formato de saída padrão e, em caso de erro, o envelope `{ "error": { "code", "message", "details" } }`
**And** um lint de imports falha o build se `packages/core` importar outro pacote do projeto ou SDK de I/O
**And** logs vão para `~/.sinter/logs` em JSON lines

### Story 1.2: Spike — o motor de grafo encontra as integrações entre serviços

As a fundador do Sinter,
I want medir se o Graphify identifica bem as integrações entre serviços,
So that a gente decida o motor do grafo antes de construir o mapa em cima dele.

**Acceptance Criteria:**

**Given** a porta `GraphEngine` em `core/ports` devolvendo `GraphFacts` (nós, arestas `api|event|file|queue`, flag `extracted|inferred`, proveniência) (AD-8)
**And** um conjunto de teste com pelo menos 10 repos de microsserviços open source com integrações conhecidas e anotadas à mão (nunca dados da empregadora)
**When** o adaptador do Graphify roda `graphify` como processo filho e converte o `graph.json` em `GraphFacts`
**Then** um relatório em `docs/spikes/graph-engine.md` registra precisão e cobertura das integrações HTTP, eventos e filas contra a anotação manual, e o tempo de processamento
**And** o relatório termina com uma decisão explícita: manter o Graphify, complementar com regras próprias ou trocar de adaptador (codebase-memory-mcp ou Cognee)
**And** nenhum tipo específico do Graphify aparece fora de `packages/adapters/graphify`

### Story 1.3: Criar o domínio

As a arquiteto,
I want criar o domínio Pagamentos com um repo no padrão de documentação,
So that o conhecimento do domínio tenha um lugar único e versionado desde o primeiro dia.

**Acceptance Criteria:**

**Given** o Sinter instalado e uma identidade git configurada
**When** o arquiteto roda `sinter domain create --name Pagamentos --key PAG --path ./dominio-pagamentos`
**Then** o repo do domínio é criado com as seções do padrão (glossário, sistemas, integrações, regras de negócio, decisões, padrões), cada uma com um README de instruções, e com `domain.yaml`, `people.yaml` e `sinter.yaml`
**And** o criador entra em `people.yaml` com o papel de arquiteto
**And** a criação vira um commit com os trailers `Sinter-Approved-By` e `Sinter-Role` (AD-15, FR4)
**And** apontar para um repo existente fora do padrão é recusado com a lista do que falta (FR1)
**And** o domínio é registrado no workspace local `~/.sinter` para os próximos comandos

### Story 1.4: Conectar os repos do domínio

As a arquiteto,
I want adicionar ao domínio os repos de código por caminho local ou URL,
So that o Sinter saiba quais sistemas fazem parte do domínio.

**Acceptance Criteria:**

**Given** um domínio criado
**When** o arquiteto roda `sinter domain add-repo <caminho-ou-url>` (um ou vários)
**Then** cada repo é registrado como fonte com status `ok`, `sem acesso` ou `erro`, e o motivo
**And** repos sem permissão de leitura continuam listados como `sem acesso`, nunca omitidos (FR5)
**And** `sinter domain sources` lista as fontes e o status, também em `--json`
**And** nenhuma informação de fonte é gravada no repo do domínio neste passo (fica no workspace local)

### Story 1.5: Segredos nunca passam da leitura

As a arquiteto,
I want que credenciais encontradas nas fontes sejam barradas na leitura,
So that nenhum segredo chegue ao repo do domínio, ao modelo de IA ou a um export.

**Acceptance Criteria:**

**Given** a porta `SecretScanner` implementada com betterleaks (AD-10)
**When** qualquer conteúdo é lido de uma fonte
**Then** o scanner roda antes de o conteúdo ser guardado, enviado a um LLM ou projetado
**And** cada achado é guardado só como localização (fonte, locator, tipo), nunca o valor
**And** o trecho com segredo é mascarado antes de seguir no fluxo
**And** `sinter domain sources` mostra a contagem de segredos por fonte
**And** um teste com um repo de exemplo contendo chaves falsas comprova que nenhum valor aparece no SQLite, nos logs ou no repo do domínio (NFR8)

### Story 1.6: Gerar o mapa inicial e aceitar os sistemas detectados

As a arquiteto,
I want gerar o mapa do domínio a partir dos repos e aceitar os sistemas detectados,
So that eu tenha um primeiro mapa oficial do domínio sem montar nada à mão.

**Acceptance Criteria:**

**Given** um domínio com repos conectados e o adaptador de grafo escolhido no spike
**When** o arquiteto roda `sinter domain map`
**Then** o grafo é gerado numa fila de jobs retomável, com progresso por repo (AD-11)
**And** sistemas e integrações viram **Propostas** no schema único, com proveniência `{ sourceId, locator, version, extraction }` (AD-3, AD-5)
**And** `sinter domain map --accept-detected` aprova em lote só os itens `extracted`, gravando um arquivo por item no padrão (AD-4) em um único commit (FR4)
**And** integrações `inferred` continuam como propostas, para o Epic 2
**And** num conjunto de 50 repos de exemplo, o processamento termina em menos de 30 minutos numa máquina de desenvolvedor comum (NFR6)
**And** apagar o SQLite local e rodar de novo reconstrói o mesmo estado a partir do repo do domínio (AD-2)

### Story 1.7: Ver e navegar o mapa no app

As a arquiteto,
I want abrir o app com `sinter ui` e navegar pelo mapa do domínio,
So that eu veja pela primeira vez como os sistemas se conversam.

**Acceptance Criteria:**

**Given** um domínio com sistemas aprovados
**When** o arquiteto roda `sinter ui`
**Then** o servidor sobe só em `127.0.0.1:4317` e abre o app no navegador (AD-11, NFR1)
**And** o app usa os tokens do DESIGN.md (tema Esmalte) e o shell em quatro colunas: trilho, lista, área de trabalho e painel (UX-DR1, UX-DR2)
**And** a área de trabalho mostra o mapa do sistema selecionado com os vizinhos, em cartões de sistema com badge de tecnologia e estado (UX-DR3)
**And** o usuário busca sistemas, filtra por tipo de integração e foca um sistema; o painel mostra responsabilidade, stack, dono, o que expõe e o que consome (FR11)
**And** cada integração mostra a proveniência e abre o trecho de origem (FR10)
**And** a UI só acessa dados pelo RPC tipado do servidor (AD-12), e sistemas sem acesso aparecem tracejados com "sem acesso de leitura" (UX-DR14)
**And** o domínio vazio mostra o convite "Adicione o primeiro repositório ou documento"
