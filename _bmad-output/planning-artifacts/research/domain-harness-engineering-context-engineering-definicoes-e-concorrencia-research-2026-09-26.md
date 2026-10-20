---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments: []
workflowType: 'research'
lastStep: 6
research_type: 'domain'
research_topic: 'Harness Engineering e Context Engineering para desenvolvimento assistido por IA — definições, padrões e concorrência'
research_goals: 'Embasar brief e PRD do harness_corp: consolidar definições e padrões do mercado, mapear concorrência, afiar diferencial e escopo do MVP'
user_name: 'Gui'
date: '2026-09-26'
web_research_enabled: true
source_verification: true
---

# Research Report: domain — Harness Engineering e Context Engineering

**Date:** 2026-09-26
**Author:** Gui
**Research Type:** domain

---

## Research Overview

Esta pesquisa de domínio investigou **definições, padrões e concorrência** em Harness Engineering e Context Engineering para desenvolvimento assistido por IA, com o objetivo de embasar o brief e o PRD do harness_corp. Foram cerca de 30 buscas web (set/2026), com fontes primárias sempre que possível (Linux Foundation, spec do MCP, agentskills, Fowler, Anthropic, legislação brasileira e europeia) e níveis de confiança explícitos.

Achados centrais: o gargalo dos agentes é o contexto, não o modelo; AGENTS.md, SKILL.md e MCP já são padrões abertos com governança neutra e expressam a hierarquia Empresa → Domínio → Repo → Módulo; a concorrência é forte em *recuperar* contexto (Augment, Unblocked, Tabnine) e fraca em *construir* contexto em cadeia entre papéis, que é a brecha do harness_corp. Riscos críticos: titularidade do produto (Lei 9.609/98), colisão de nome ("harness") e context rot.

O resumo executivo completo, as recomendações e os próximos passos estão na seção **Síntese** ao final do documento.

---

<!-- Content will be appended sequentially through research workflow steps -->

## Domain Research Scope Confirmation

**Research Topic:** Harness Engineering e Context Engineering para desenvolvimento assistido por IA — definições, padrões e concorrência
**Research Goals:** Embasar brief e PRD do harness_corp: consolidar definições e padrões do mercado, mapear concorrência, afiar diferencial e escopo do MVP

**Domain Research Scope:**

- Análise do setor (peso alto): context engines, plataformas de harness, SDD, marketplaces de skills/agentes
- Tendências de tecnologia (peso alto): definições canônicas, padrões abertos (AGENTS.md, SKILL.md, MCP, plugins), spec-driven development
- Ecossistema / cadeia de valor (peso médio): camadas modelo → agente → harness → contexto → fontes
- Fatores econômicos (peso leve): funding e sinais de mercado dos principais players
- Regulatório (peso leve): dados de código/documentos corporativos, IP, self-hosted vs cloud

**Research Methodology:**

- All claims verified against current public sources
- Multi-source validation for critical domain claims
- Confidence level framework for uncertain information
- Comprehensive domain coverage with industry-specific insights

**Scope Confirmed:** 2026-09-26

---

## Industry Analysis

### Market Size and Valuation

Não existe um relatório de mercado específico para "harness engineering" ou "context engineering". A categoria é nova demais. A melhor referência é o mercado-mãe de **ferramentas de IA para código**, e as estimativas divergem bastante por causa de definições diferentes de escopo:

| Fonte | Tamanho 2026 | Projeção | CAGR |
|---|---|---|---|
| Grand View Research | US$ 10,3 bi | US$ 42,8 bi (2033) | 22,5% |
| Mordor Intelligence (code gen + assistentes) | US$ 16,1 bi | US$ 79,0 bi (2031) | 37,4% |
| Research and Markets (AI Code Tools) | US$ 9,5 bi | US$ 22,2 bi (2030) | 23,8% |
| New Market Pitch | US$ 12,8 bi | US$ 30,1 bi (2032) | 27% |

_Total Market Size: US$ 9,5 a 16 bi em 2026 (mercado-mãe de ferramentas de IA para código)_
_Growth Rate: CAGR de 22% a 37%, conforme a definição_
_Market Segments: assistentes/IDEs (Copilot, Cursor), agentes autônomos (Devin, Codex), context engines (Augment, Unblocked, Tabnine, Sourcegraph), SDD/governança (Kiro, Spec Kit, BMAD, Tessl)_
_Economic Impact: América do Norte concentra ~33% da receita (2025)_
_Confiança: **média**. Os números mostram tendência, não precisão. O segmento "contexto/harness" é uma fatia não medida do total._
_Sources: [Grand View Research](https://www.grandviewresearch.com/industry-analysis/ai-code-assistants-market-report), [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/ai-code-generation-and-developer-assistant-market), [Research and Markets](https://www.researchandmarkets.com/reports/6225896/ai-code-tools-market-report), [New Market Pitch](https://newmarketpitch.com/blogs/news/ai-code-assistant-market-size)_

**Sinais de capital (proxy do tamanho real):**

- **Cursor/Anysphere:** ARR estimado em ~US$ 4 bi em 2026; adquirida pela SpaceX por US$ 60 bi (aquisição fechada em ago/2026)
- **Cognition (Devin):** Series D de US$ 1 bi+ a US$ 26 bi (mai/2026), com rodada seguinte negociada a ~US$ 47 bi
- **Augment Code:** US$ 252 mi captados, avaliação de ~US$ 1,4 bi; posicionamento em "Context Engine"
- **Unblocked:** Series A de US$ 20 mi (mai/2025); posicionamento "context engine" sobre as fontes da empresa

_Sources: [TheNextWeb](https://thenextweb.com/news/cursor-anysphere-2-billion-funding-50-billion-valuation-ai-coding), [Wikipedia: Cursor](https://en.wikipedia.org/wiki/Cursor_(company)), [Latka](https://getlatka.com/companies/cursor.com), [Yellow: Cognition](https://yellow.com/news/cognition-raises-1-billion-26-billion-valuation-ai-coding-agent), [GCN: Cognition](https://gcn.com/cognition-ai-47-billion-funding-round/21603/), [Augment Code](https://www.augmentcode.com/blog/augment-inc-raises-227-million), [BetaKit: Unblocked](https://betakit.com/unblocked-raises-27-5-million-series-a-to-make-sure-developers-actually-understand-their-code/)_

### Market Dynamics and Growth

_Growth Drivers:_
- **Adoção quase universal:** 90% dos devs profissionais usam agentes de código toda semana e 68% usam todo dia (JetBrains, 15 mil+ devs, 2026)
- **Lacuna de confiança:** só ~3% dizem confiar muito no código gerado por IA, e perto de metade desconfia ativamente. A lacuna entre uso e confiança é exatamente o espaço do harness (guides + sensors)
- **Legado e codebases grandes:** o estudo controlado do METR mostrou devs experientes **19% mais lentos** com IA em codebases grandes e desconhecidas. Falta de contexto é o gargalo
- **SDD:** relatos de early adopters (GitHub/AWS) apontam taxa de sucesso na 1ª tentativa de 3 a 10 vezes maior quando o agente trabalha a partir de specs

_Growth Barriers:_ confiança e governança; capacidade de review humano não escala junto com a geração; segurança e privacidade de código e documentos corporativos; ROI difícil de provar (DORA sozinho não captura o efeito da IA)
_Cyclical Patterns:_ ciclos curtíssimos. Padrões e ferramentas mudam em meses; vendors de modelo absorvem funcionalidades de startups
_Market Maturity:_ mercado-mãe em **crescimento acelerado com início de consolidação**; o segmento de contexto/harness está em **formação** (vocabulário ainda sendo definido)
_Sources: [JetBrains Research](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/), [daily.dev](https://daily.dev/posts/ai-coding-tools-in-mid-2026-high-adoption-low-trust-and-what-it-means-for-developers-pnvdzeodd), [Uvik: estatísticas](https://uvik.net/blog/ai-coding-assistant-statistics/), [Sonar State of Code 2026](https://www.sonarsource.com/state-of-code-developer-survey-report.pdf), [Uvik: SDD benchmark](https://uvik.net/spec-driven-development-benchmark/), [BCMS: SDD guide](https://www.thebcms.com/blog/spec-driven-development/)_

### Market Structure and Segmentation

O mercado se organiza em **camadas**, e o harness_corp atua nas camadas 3 e 4:

| # | Camada | Exemplos | Dinâmica |
|---|---|---|---|
| 1 | **Modelo** | Anthropic, OpenAI, Google | Poucos players, capital massivo |
| 2 | **Agente / IDE** | Claude Code, Cursor, Copilot, Codex, Devin, Kiro | Consolidação acelerada (SpaceX–Cursor) |
| 3 | **Harness / método (guides)** | AGENTS.md, Skills, Spec Kit, BMAD, OpenSpec, Tessl | Majoritariamente **open source e gratuito** |
| 4 | **Contexto (engines + grafos)** | Augment, Unblocked, Tabnine Context Engine, Sourcegraph, Glen, Harness Inc. | Startups e plataformas DevOps disputando o "control point" |
| 5 | **Sensors / governança** | Sonar, Qodo, CloudWatch Coding Agent Insights | Vendors de qualidade e observabilidade entrando |
| 6 | **Fontes** | GitHub, Confluence, Google Docs, Jira, Slack, reuniões | Incumbentes; acesso via MCP e conectores |

_Primary Segments:_ assistentes/agentes (camada 2) concentram a receita; contexto (camada 4) é onde está a disputa estratégica atual
_Sub-segment Analysis:_ camada 3 tem alta adoção comunitária (Spec Kit, com 93 mil+ estrelas; BMAD e OpenSpec, com 48 mil+ cada) e baixa monetização direta
_Geographic Distribution:_ EUA dominam em vendors e receita; o Brasil aparece como consumidor, sem players locais relevantes identificados nesta pesquisa
_Vertical Integration:_ agentes e IDEs puxam para si contexto e harness (skills, rules, memória nativa). Esse é o principal risco estrutural para quem atua só na camada 3
_Sources: [Futurum: Tabnine](https://futurumgroup.com/insights/tabnines-visionary-status-does-context-driven-ai-coding-redefine-enterprise-software-delivery/), [MarkTechPost: SDD tools](https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/), [DEV: SDD 2026](https://dev.to/krlz/spec-driven-development-in-2026-what-it-is-the-tooling-and-how-teams-actually-use-it-2fk2), [Cruxdigits: context engineering](https://cruxdigits.nl/blog/context-engineering-ai-agents-2026/)_

### Industry Trends and Evolution

_Emerging Trends:_
- **De "prompt" para "context" para "harness":** o vocabulário amadureceu rápido. Martin Fowler formalizou harness = tudo exceto o modelo, com guides e sensors
- **Padrões abertos convergindo:** AGENTS.md (lido por Claude Code, Cursor, Copilot e 60 mil+ projetos) e SKILL.md viram "formato de arquivo" comum entre ferramentas
- **Spec-driven development** virou categoria com várias ferramentas; críticos chamam de "o waterfall contra-ataca"
- **Context rot** passou de curiosidade acadêmica a métrica acompanhada por líderes de engenharia
- **Camada de contexto entre agentes:** produtos como o Glen unificam sessões de vários agentes com Slack, PRs, tickets, docs e chamadas

_Historical Evolution:_ 2023–24 autocomplete e chat → 2025 agentes, Skills (out/2025) e AGENTS.md → 2026 harness engineering, SDD, context engines e observabilidade de agentes
_Technology Integration:_ MCP como protocolo de conexão com fontes; plugins e marketplaces multi-ferramenta
_Future Outlook:_ contexto e governança viram o diferencial enterprise (Gartner já tem um MQ de "Enterprise AI Coding Agents"); esperam-se mais aquisições de startups de contexto por plataformas de agentes e DevOps
_Sources: [Martin Fowler](https://martinfowler.com/articles/harness-engineering.html), [Anthropic: context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [BuildBetter: AGENTS.md vs rules vs skills](https://blog.buildbetter.ai/agents-md-vs-cursorrules-vs-claude-skills-2026-comparison/), [Marmelab: SDD](https://marmelab.com/blog/2025/11/12/spec-driven-development-waterfall-strikes-back.html), [Wikipedia: SDD](https://en.wikipedia.org/wiki/Spec-driven_development)_

### Competitive Dynamics

_Market Concentration:_ alta nas camadas 1 e 2; **fragmentada** nas camadas 3 e 4 (muitos players, nenhum dominante em "harness por papel")
_Competitive Intensity:_ muito alta. Players bem capitalizados (Augment, Tabnine, Harness Inc.) e alternativas open source gratuitas (Spec Kit, BMAD, marketplaces de skills)
_Barriers to Entry:_ baixas para ferramentas de harness `.md` (qualquer um publica); **altas** para context engines em escala (indexação, segurança, conectores enterprise, confiança de dados)
_Innovation Pressure:_ extrema. Vendors de agente (Anthropic, GitHub, Cursor) lançam de forma nativa o que startups vendem (memória, skills, rules, plan mode)
_Confiança: **média-alta** sobre a estrutura; **baixa** sobre participação de mercado no segmento de contexto (sem dados públicos)_

### Implicações para o harness_corp

1. **O espaço existe e está quente**, mas o segmento "contexto" está sendo disputado por players com US$ 20 mi a US$ 250 mi+ captados. Competir como "mais um context engine" é arriscado.
2. **A lacuna de confiança é o argumento.** O mercado já adotou agentes, mas não confia neles. O harness_corp vende confiança via contexto curado por papel, e não mais uma IA.
3. **Os padrões abertos são aliados.** Materializar em AGENTS.md/SKILL.md no repo evita lock-in e surfa a convergência.
4. **A camada 3 open source é concorrente e canal ao mesmo tempo.** BMAD e Spec Kit resolvem o método, mas não conectam as fontes da empresa nem o grafo de domínio. Essa é a costura possível.
5. **Risco de absorção:** agentes nativos podem absorver funcionalidades. A defesa está no que o vendor de agente não faz bem: **cadeia entre papéis + grafo de domínio multi-repo + fontes corporativas**.

---

## Competitive Landscape

### Key Players and Market Leaders

Não existe um líder em "harness por projeto e por papel". A concorrência vem de **cinco grupos**, cada um cobrindo uma parte da proposta do harness_corp:

**Grupo A: Context engines (contexto na hora da consulta)**
- **Unblocked:** "context engine for engineering". Lê código, PRs, Slack, Jira, Notion e Confluence e entrega contexto "decision-grade" com conflitos resolvidos para IDEs, agentes (via MCP), CLI e API. Respeita as permissões de cada fonte; SOC 2 Type II. Afirma 48% menos tokens e tarefas 83% mais rápidas (benchmark interno). Series A de US$ 20 mi.
- **Augment Code:** Context Engine semântico em escala (centenas de milhares de arquivos), exposto também como MCP. Cobra por token (preço do provedor + 40%) e tem planos a partir de US$ 20/mês. US$ 252 mi captados.
- **Tabnine Enterprise Context Engine:** "modelo estruturado e continuamente atualizado da sua arquitetura, dependências e padrões". Visionary no Gartner MQ 2026 de Enterprise AI Coding Agents. US$ 39/usuário/mês (Code Assistant) e US$ 59 (Agentic Platform).
- **Sourcegraph (Cody/Amp):** busca e navegação de código entre repos; forte em descoberta, fraco em contexto de decisão.
- **Glen:** camada que unifica sessões de vários agentes (Claude Code, Codex, Cursor) com Slack, PRs, tickets, docs e chamadas, e injeta o contexto prévio relevante.

**Grupo B: Plataformas de entrega com knowledge graph**
- **Harness Inc.:** *Software Delivery Knowledge Graph* (567 tipos de entidade, 29 bi de atualizações/mês) e *Software Factory*, que usa specs para impor padrões nos fluxos agênticos (anunciado em set/2026). Tem também um **Agent Marketplace** (GA em jun/2026) com agentes pré-prontos (Autofix, Code Review...). Foco em DevOps/CI-CD, não na cadeia negócio → arquitetura.

**Grupo C: Spec-driven development e skills com governança**
- **Tessl:** "package manager for agent skills". Tem registry com 3 mil+ skills avaliadas e com nota, avaliação de qualidade e ciclo de vida de skills na organização; permite codificar padrões de segurança como skill. US$ 125 mi captados (seed + Series A).
- **GitHub Spec Kit** (93 mil+ estrelas), **BMAD-METHOD** e **OpenSpec** (48 mil+ cada): método open source e gratuito, agnóstico de agente.
- **AWS Kiro:** IDE com SDD nativo.

**Grupo D: Grafos de código open source**
- **codebase-memory-mcp:** indexa o repo em grafo (158 linguagens; kernel Linux em 3 min); detecta **chamadas HTTP/assíncronas entre serviços**, com score de confiança.
- **Cognee:** memória em grafo a partir de AST, acessível via MCP.
- **Understand Anything** (15 mil+ estrelas): grafo com painel visual.
- **CodeGraph:** 47% menos tokens e 58% menos tool calls, em média.

**Grupo E: Marketplaces de skills e captura de negócio**
- **Marketplaces:** diretório curado da Anthropic + parceiros (Atlassian, Notion, Sentry...), skills.sh, SkillsMP (3 mi+ skills indexadas), Agensi (pagas e verificadas), 2.500+ marketplaces de plugins registrados. Padrão **agentskills.io**, portável para ~40 produtos.
- **BuildBetter:** transforma calls e transcrições em PRDs com citação da fala original; tem o BB-Skills (13 skills open source para agentes).

_Market Leaders:_ nenhum dominante no recorte do harness_corp; Augment e Tabnine lideram "context engine enterprise"; Spec Kit lidera SDD em adoção
_Emerging Players:_ Glen, Tessl, grafos de código open source
_Global vs Regional:_ todos norte-americanos ou europeus (Tessl: Londres); nenhum player brasileiro identificado
_Sources: [Unblocked: context layer](https://getunblocked.com/blog/context-layer-ai-agents/), [Unblocked MCP](https://getunblocked.com/unblocked-mcp/), [Unblocked: next era](https://getunblocked.com/blog/unblocked-context-engine-for-agents/), [Augment Context Engine](https://www.augmentcode.com/context-engine), [Augment MCP docs](https://docs.augmentcode.com/context-services/mcp/overview), [Augment pricing](https://www.augmentcode.com/pricing), [Tabnine Context Engine](https://context.tabnine.com/), [Tabnine pricing](https://www.tabnine.com/pricing-enterprise-context-engine/), [Harness: knowledge graph](https://www.harness.io/blog/why-harness-ai-uses-knowledge-graph), [Harness: worker agents](http://www.prnewswire.com/news-releases/harness-launches-autonomous-worker-agents-for-software-delivery-302814180.html), [DevOps.com: Harness](https://devops.com/harness-previews-revamped-platform-for-the-agentic-engineering-era/), [Tessl registry](https://tessl.io/registry), [Tessl Series A](https://tessl.io/blog/announcing-our-series-a-for-ai-native-software-development/), [Tessl review](https://codemyspec.com/blog/tessl-review), [codebase-memory-mcp (arXiv)](https://arxiv.org/html/2603.27277v1), [Cognee](https://cognee.ai/blog/guides/ai-coding-agent-persistent-codebase-memory), [Understand Anything](https://dev.to/arshtechpro/understand-anything-turn-any-codebase-into-an-interactive-knowledge-graph-37ed), [CodeGraph](https://toknow.ai/posts/codegraph-knowledge-graph-ai-coding-agents-fewer-tokens/), [Agentman: skills ecosystem](https://agentman.ai/blog/agent-skills-ecosystem-report-2026), [Agensi: marketplaces](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026), [SkillsMP](https://skillsmp.com/), [BuildBetter: calls → PRDs](https://blog.buildbetter.ai/best-tools-to-turn-customer-calls-into-prds/)_

### Market Share and Competitive Positioning

Não há dados públicos de participação de mercado no segmento de contexto/harness (confiança: **baixa**). O posicionamento, porém, é claro. Matriz frente à proposta do harness_corp:

| Capacidade | Unblocked | Augment | Tabnine | Harness Inc. | Tessl | Spec Kit / BMAD | Grafos OSS | **harness_corp** |
|---|---|---|---|---|---|---|---|---|
| Fontes corporativas (Confluence, Docs, Slack) | ✅ | 🟡 | 🟡 | 🟡 | ❌ | ❌ | ❌ | ✅ |
| Transcrições de reunião | 🟡 (via Slack) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Grafo multi-repo / cross-service | 🟡 | ✅ | ✅ | ✅ (entrega) | ❌ | ❌ | ✅ | ✅ |
| Cadeia de contexto entre papéis (negócio → arq → TL → dev) | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 (BMAD tem papéis) | ❌ | ✅ |
| Materializa no repo Git (versionado, review) | ❌ | ❌ | ❌ | ❌ | 🟡 (skills instaladas) | ✅ | ❌ | ✅ |
| Agnóstico de ferramenta | ✅ (MCP) | 🟡 | 🟡 | ❌ | ✅ | ✅ | ✅ (MCP) | ✅ |
| Marketplace / registry de skills | ❌ | ❌ | ❌ | ✅ (agentes) | ✅ | ❌ | ❌ | ✅ |
| Curadoria humana antes de entrar | 🟡 | ❌ | 🟡 | 🟡 | ✅ (avaliação) | ✅ (manual) | ❌ | ✅ |

_Legenda: ✅ forte · 🟡 parcial · ❌ ausente. Avaliação baseada em material público; os itens 🟡 exigem verificação em demo._

_Competitive Positioning:_
- **Unblocked, Augment e Tabnine:** "contexto sob demanda" (pull em tempo de consulta, via MCP). O contexto vive **na plataforma deles**
- **Harness Inc.:** "padrões e agentes na esteira de entrega" (DevOps)
- **Tessl:** "skills como pacotes governados"
- **Spec Kit/BMAD:** "método gratuito no repo"
- **harness_corp (proposto):** "contexto construído em cadeia, curado por papel e **materializado no repo**"

_Customer Segments Served:_ Augment, Tabnine e Harness miram a grande empresa (governança, SSO, on-prem); Unblocked mira times de engenharia de médio porte; Spec Kit/BMAD servem indivíduos e times sem orçamento

### Competitive Strategies and Differentiation

_Cost Leadership:_ open source (Spec Kit, BMAD, grafos OSS e marketplaces gratuitos) zera o preço do "método" e do "grafo de código simples"
_Differentiation:_ Unblocked em "contexto de decisão" (o porquê); Augment em escala semântica; Tabnine em governança e privacidade enterprise; Tessl em qualidade avaliada de skills
_Focus/Niche:_ BuildBetter (voz do cliente → PRD); Glen (memória entre agentes); codebase-memory-mcp (grafo cross-service)
_Innovation Approaches:_ todos convergem para **MCP como canal de entrega**; os diferenciais estão migrando da *indexação* para a *qualidade e governança do contexto*

### Business Models and Value Propositions

| Modelo | Quem usa | Faixa de preço |
|---|---|---|
| Assinatura por usuário | Tabnine, Unblocked | US$ 39 a 59/usuário/mês (Tabnine) |
| Uso / tokens + taxa | Augment (Context Engine MCP) | Preço do provedor + 40% |
| Plataforma enterprise | Harness Inc. | Contrato anual (não público) |
| Registry/plataforma de skills | Tessl | Freemium + enterprise (não confirmado) |
| Open source + serviços/consultoria | BMAD, Spec Kit, harness-engineering.ai | Grátis; receita em serviços |

_Nota de dados:_ uma fonte agregou os preços de Tabnine e Unblocked; o valor de US$ 39/59 foi confirmado apenas para a **Tabnine**. O preço da Unblocked **não foi confirmado** publicamente.
_Customer Relationship:_ lock-in via índice/plataforma proprietária (engines) vs portabilidade via arquivos no repo (SDD). O harness_corp fica do lado da **portabilidade**, o que é bom para adoção e mais difícil para retenção.

### Competitive Dynamics and Entry Barriers

_Barriers to Entry:_ baixas para método e skills `.md`; **altas** para conectores enterprise seguros (permissões por fonte, SOC 2, on-prem) e para grafo em escala
_Competitive Intensity:_ muito alta e crescente; vendors de agente absorvem funcionalidades (skills, memória e rules nativos)
_Market Consolidation:_ aquisições bilionárias na camada 2 (SpaceX–Cursor); espera-se M&A de startups de contexto
_Switching Costs:_ baixos quando o contexto está em arquivos abertos no repo, e altos quando está em índice proprietário. Isso é uma faca de dois gumes para o harness_corp

### Ecosystem and Partnership Analysis

_Supplier Relationships:_ dependência de APIs de fontes (Atlassian, Google, GitHub) e de modelos (Anthropic, OpenAI) para inferência
_Distribution Channels:_ MCP, marketplaces de plugins (Claude Code, Copilot), comunidades open source (a de BMAD é um canal natural: o harness_corp já usa BMAD)
_Technology Partnerships:_ Atlassian está no diretório de parceiros de skills da Anthropic, o que permite integrar em vez de reconstruir conectores
_Ecosystem Control:_ vendors de agente controlam o "ponto de consumo"; as plataformas de contexto disputam o "ponto de verdade". **Ninguém controla o "ponto de autoria" do contexto entre papéis.** Essa é a brecha

### ⚠️ Alerta de nome

"Harness" está saturado: **Harness Inc.** (marca registrada, com knowledge graph e agent marketplace) e **harness-engineering.ai** (site de conteúdo e consultoria com knowledge graph do ecossistema). Recomenda-se não usar "harness" como marca principal.

### Implicações competitivas para o harness_corp

1. **Não brigar na indexação.** Grafos de código OSS (codebase-memory-mcp, Cognee) já fazem o micro e até o cross-service. **Usar ou incorporar**, não reconstruir.
2. **A brecha real é a autoria do contexto em cadeia.** Nenhum player modela negócio → arquitetura → tech lead → dev como camadas de contexto com dono, aprovação e versão.
3. **O Unblocked é o concorrente mais próximo** em fontes corporativas. O contraste: *eles respondem perguntas na hora; o harness_corp prepara o repo antes da tarefa, com curadoria e versionamento em Git.*
4. **O Tessl é o concorrente mais próximo no marketplace.** O marketplace do harness_corp deve ser **por papel e por empresa (privado)**, não mais um registry público genérico.
5. **Transcrições são um diferencial raro** no espaço de código. O BuildBetter faz isso para PRD, mas não conecta ao repo nem ao grafo.

---

## Regulatory Requirements

> ⚠️ Esta seção é pesquisa de mercado, **não é aconselhamento jurídico**. Os pontos marcados como risco alto devem ser validados com um advogado.

### Applicable Regulations

**1. Lei do Software (Lei 9.609/98, art. 4º): risco mais imediato para o fundador**
- Regra geral: salvo contrato em contrário, pertence **ao empregador** o software desenvolvido durante o vínculo quando a atividade do empregado é prevista no contrato ou decorre da natureza do cargo.
- Exceção (§ 2º): pertence **ao criador** se o software for feito **sem relação com o contrato** e **sem uso de recursos, informações tecnológicas, segredos, materiais, instalações ou equipamentos do empregador**.
- **Implicação direta:** construir o MVP usando código, Confluence e reuniões da empregadora (e/ou em horário e equipamento dela) pode fazer a titularidade do produto ser reivindicada pela empresa. Como o produto é sobre arquitetura de software, a relação com o cargo de quem trabalha na área é facilmente argumentável.
_Sources: [Planalto: Lei 9.609/98](https://www.planalto.gov.br/ccivil_03/leis/l9609.htm), [FAPESP: PI de software](https://fapesp.br/4512/propriedade-intelectual-para-programas-de-computador), [IODA: jurisprudência](https://ioda.org.br/publicacoes/jurisprudencia-brasileira/programa-de-computador-relacao-de-emprego-titularidade-do-software/)_

**2. LGPD (Lei 13.709/18) + prioridades da ANPD**
- A IA é um dos **quatro eixos prioritários de fiscalização da ANPD para 2026–2027**, com cerca de 20 ações de fiscalização previstas. A ANPD já agiu contra a Meta (suspensão de treino de IA com dados pessoais, multa diária) e a Worldcoin.
- Código e documentação costumam ter **pouco dado pessoal**, mas **transcrições de reunião têm muito**: nomes, opiniões, voz e, às vezes, dados de clientes.
- A LGPD já se aplica ao uso de IA com dados pessoais, independentemente do **PL 2338/2023** (marco de IA, ainda em tramitação). O PL 2775/24 propõe consentimento expresso para treinar IA com dados pessoais.
_Sources: [Confidata: ANPD e IA 2026–27](https://confidata.com.br/blog/anpd-regulacao-ia-brasil-2026-2027), [Macher: fiscalização ANPD](https://www.machertecnologia.com.br/anpd-fiscalizacao-plataformas-ia-empresas-2026/), [Macher: Nota Técnica 12/2025](https://www.machertecnologia.com.br/lgpd-anpd-inteligencia-artificial-nota-tecnica-12-2025/), [Mind Group: LGPD e IA 2026](https://mindconsulting.com.br/2026/09/lgpd-e-inteligencia-artificial-em-2026-o-que-muda-para-empresas/)_

**3. EU AI Act (se vender para a Europa)**
- Assistentes de código comuns tendem a ficar em **risco limitado**, com obrigação de transparência do **art. 50** (informar quando o conteúdo é gerado por IA). Uso comum de desenvolvimento **não está** no Anexo III de alto risco.
- Atenção: **alocação de tarefas ou avaliação de trabalhadores** *pode* disparar o alto risco. Se o harness_corp um dia medir o desempenho de devs individualmente, isso muda.
- O *Digital Omnibus* (em vigor desde 27/07/2026) adiou as obrigações de alto risco para **02/12/2027**.
_Sources: [artificialintelligenceact.eu: art. 50](https://artificialintelligenceact.eu/transparency-rules-article-50/), [Comissão Europeia: AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai), [Augment: EU AI Act 2026](https://www.augmentcode.com/guides/eu-ai-act-2026), [DEV: EU AI Act para devs](https://dev.to/comic_sans/the-eu-ai-act-in-practice-what-applies-to-app-developers-in-20262027-ngb), [Knowlee: crosswalk](https://www.knowlee.ai/blog/ai-security-compliance-framework-2026)_

### Industry Standards and Best Practices

- **Não usar dado do cliente para treinar modelo** virou requisito de mercado, não diferencial
- **Respeitar as permissões da fonte:** quem não pode ver a página do Confluence também não deve vê-la no harness (o Unblocked já faz isso)
- **Controle de acesso por transcrição:** nem todo o time deve ler toda reunião
- **Detecção de segredos:** code e docs frequentemente contêm credenciais, que **não podem ser materializadas** em AGENTS.md ou skills
_Sources: [Unblocked MCP](https://getunblocked.com/unblocked-mcp/), [Ploomes: transcrição com IA](https://blog.ploomes.com/transcricao-de-reunioes-com-ia/), [Probo: AI coding e SOC 2](https://www.probo.com/hub/ai-coding-tools-soc2-compliance)_

### Compliance Frameworks

Questionários de compras enterprise em 2026 citam pelo menos quatro referências:

| Framework | O que cobre | Quando o harness_corp precisa |
|---|---|---|
| **SOC 2 Type II** | Controles de serviço (segurança, disponibilidade, confidencialidade) | Ao vender SaaS para médias e grandes empresas |
| **ISO/IEC 27001** | Gestão de segurança da informação | Grandes empresas, bancos, governo |
| **ISO/IEC 42001** | Gestão de sistemas de IA (impacto, ciclo de vida, supervisão humana) | Diferencial crescente; a curadoria humana do harness_corp conversa bem com ele |
| **EU AI Act** | Transparência e risco de IA | Só se vender na UE |

_Sources: [DEV: checklist de compliance para AI coding](https://dev.to/radotsvetkov/ai-coding-compliance-for-2026-a-working-checklist-for-iso-42001-the-eu-ai-act-soc-2-and-tool-2i3), [Augment: SOC 2](https://www.augmentcode.com/guides/7-soc-2-ready-ai-coding-tools-for-enterprise-security), [soc2auditors: ISO 42001](https://soc2auditors.org/insights/ai-startup-iso-42001/), [Penligent: stack de segurança 2026](https://www.penligent.ai/hackinglabs/ai-soc-iso-27001-soc-2-and-the-security-stack-real-ai-teams-need-in-2026/)_

### Data Protection and Privacy

- **Transcrições de reunião:** avisar e obter ciência ou consentimento no início da gravação; gravar sem conhecimento dos participantes pode gerar responsabilidade por quebra de sigilo, imagem ou confidencialidade. Assistentes de reunião com IA já são tratados como "problema de governança de dados".
- **Minimização:** o harness deve carregar **decisões e regras**, não a transcrição bruta. Extrair "o que foi decidido" e descartar "quem disse o quê" reduz muito a exposição.
- **Shadow AI:** colaboradores enviando dados corporativos a ferramentas públicas é uma preocupação central de compliance. Um produto local ou self-hosted **resolve** essa objeção.
- **Transferência internacional:** enviar código e docs a modelos hospedados fora do Brasil exige base legal e cláusulas, relevante para clientes regulados (bancos, saúde, governo).
_Sources: [Mendonça de Barros: IA em reuniões](https://mbarros.adv.br/ia-em-reunioes-online-privacidade-riscos-e-regulacao/), [TIRIO: gravar sem avisar](https://www.ti.rio/gravar-uma-reuniao-sem-avisar-lgpd-e-direito-de-imagem/), [LETSLETS: assistentes de reunião](https://www.letsmarketing.com.br/en/assistentes-de-reuniao-com-ia-estao-virando-um-problema-de-governanca-de-dados/), [Sys4B: LGPD e IA](https://sys4b.com.br/compliance-2026-lgpd-2-0-e-o-impacto-da-ia-nos-dados-corporativos/)_

### Licensing and Certification

- Não há licença obrigatória para operar ferramentas de desenvolvimento com IA no Brasil
- **Registro de software no INPI** (opcional, mas útil) reforça a prova de autoria e de data, o que é relevante diante do risco do art. 4º
- **Licenciamento de conteúdo do marketplace:** skills de terceiros e de open source (MIT, Apache, CC) precisam ter a licença rastreada; skills privadas de cliente nunca podem vazar entre tenants
- **Termos de API** de Atlassian, Google e dos provedores de modelo impõem limites de uso e armazenamento

### Implementation Considerations

1. **MVP local-first é uma vantagem regulatória:** nada sai da máquina ou da rede do cliente, e isso elimina a maior parte das objeções de LGPD, transferência e Shadow AI.
2. **Permissões herdadas da fonte** desde o primeiro conector.
3. **Scanner de segredos** antes de materializar qualquer coisa no repo.
4. **Pipeline de transcrição com minimização:** extrair decisões e regras, com opção de anonimizar pessoas.
5. **Modelo "traga sua própria chave/modelo"** (BYO LLM): o cliente escolhe o provedor, inclusive local, e a responsabilidade pelo processamento fica clara.
6. **Trilha de auditoria:** quem aprovou qual camada de contexto. Serve à curadoria *e* ao ISO 42001.

### Risk Assessment

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| **Titularidade do produto reivindicada pela empregadora (Lei 9.609/98)** | 🔴 Média-alta se usar dados ou recursos dela | 🔴 Crítico: pode inviabilizar o SaaS | Construir fora do horário, em equipamento próprio, com repos **open source ou sintéticos**; ler contrato e política de PI; ou negociar formalmente a empresa como *design partner* com cláusula de PI clara |
| Vazamento de dado pessoal via transcrições | 🟡 Média | 🔴 Alto (ANPD prioriza IA) | Consentimento, minimização, controle de acesso |
| Segredos materializados no repo | 🟡 Média | 🔴 Alto | Scanner de segredos obrigatório |
| Bloqueio em compras enterprise por falta de SOC 2 / ISO | 🔴 Alta ao virar SaaS | 🟡 Médio | Local/self-hosted primeiro; SOC 2 quando houver receita |
| Obrigação do EU AI Act | 🟢 Baixa | 🟡 Médio | Não fazer avaliação individual de devs; transparência |
| Vazamento de skill privada entre clientes no marketplace | 🟢 Baixa no MVP | 🔴 Alto no SaaS | Isolamento por tenant desde o desenho |

---

## Technical Trends and Innovation

### Emerging Technologies

**Glossário canônico (set/2026)**, com as definições que o harness_corp deve adotar como vocabulário oficial:

| Termo | Definição | Origem / Fonte |
|---|---|---|
| **Harness** | Tudo em um agente exceto o modelo. *Agent = Model + Harness* | Fowler; LangChain |
| **Harness Engineering** | Projetar guides e sensors para gerar confiança real no que o agente produz | Fowler |
| **Context Engineering** | Curar o menor conjunto de tokens de alto sinal que maximiza o resultado desejado | Anthropic |
| **Guides (feedforward)** | Controles antes da ação: AGENTS.md, skills, arquitetura, convenções | Fowler |
| **Sensors (feedback)** | Controles após a ação: testes, lint, type check, review por IA | Fowler |
| **Steering loop** | Humano melhora guides e sensors a partir de falhas recorrentes | Fowler |
| **Harnessability** | Quanto um codebase se deixa guiar (tipos, fronteiras); o legado costuma ter pouca | Fowler |
| **Context rot** | Degradação do desempenho do modelo conforme o contexto cresce, **mesmo com a informação certa presente** | Pesquisa acadêmica 2026 |
| **Progressive disclosure** | Carregar só metadados no início e o conteúdo completo sob demanda | Spec Agent Skills |
| **Context isolation** | Mover trabalho ruidoso para subagentes, que devolvem só um resumo | Anthropic; pesquisa 2026 |
| **SDD (Spec-Driven Development)** | A spec é o artefato primário; o agente implementa a partir dela | Spec Kit, Kiro, BMAD, Tessl |
| **ADR** | Registro de uma decisão arquitetural e sua justificativa; o conjunto forma o log de decisões | adr.github.io |

**Padrões abertos (a "infraestrutura" que o harness_corp deve usar, não reinventar):**

1. **AGENTS.md** (criado pela OpenAI em ago/2025): Markdown com orientações do projeto para agentes. Mais de 60 mil projetos. Lido por Codex, Copilot, Cursor, Claude Code e outros.
   - **Hierarquia aninhada, com o arquivo mais próximo prevalecendo:** um AGENTS.md na raiz e outros em cada subpasta; o mais próximo do arquivo editado tem precedência, e o Codex concatena da raiz para baixo. O repositório principal da OpenAI tem **88 arquivos AGENTS.md**.
2. **Agent Skills / SKILL.md** (Anthropic, open standard desde 18/12/2025, spec em agentskills.io): uma pasta com SKILL.md (frontmatter `name` + `description`) e `scripts/`, `references/` e `assets/` opcionais. Suportado por **~40 plataformas** (Codex, Copilot, Cursor, Gemini CLI, VS Code...).
   - **Progressive disclosure em 3 estágios:** descoberta (~30 a 50 tokens por skill) → ativação (SKILL.md completo) → execução. Cem skills custam só ~3 a 5 mil tokens no início da sessão.
3. **MCP (Model Context Protocol):** protocolo de conexão agente ↔ ferramentas e fontes, com 110 mi+ downloads/mês. Spec **2026-07-28**: HTTP *stateless* (sem handshake nem sessão), autorização gerenciada pela empresa como extensão, e **registry verificado previsto para o 4º tri de 2026**.
4. **Governança neutra:** em dez/2025 a Linux Foundation criou a **Agentic AI Foundation (AAIF)**, com **MCP + AGENTS.md + goose** como projetos fundadores. São mais de 170 membros (abr/2026). Os padrões deixaram de ser de um único vendor.

_Sources: [Linux Foundation: AAIF](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation), [OpenAI: AAIF](https://openai.com/index/agentic-ai-foundation/), [IntuitionLabs: AAIF](https://intuitionlabs.ai/articles/agentic-ai-foundation-open-standards), [agentskills (GitHub)](https://github.com/agentskills/agentskills), [Firecrawl: Agent Skills](https://www.firecrawl.dev/blog/agent-skills), [Atlan: Agent Skills](https://atlan.com/know/ai-agent/ai-agent-skills/what-are-agent-skills/), [DEV: AGENTS.md em monorepo](https://dev.to/promptmaster/agentsmd-in-a-monorepo-nested-files-and-precedence-1b7d), [Codex KB: padrões AGENTS.md](https://codex.danielvaughan.com/2026/03/26/agents-md-advanced-patterns/), [Morph: AGENTS.md spec](https://www.morphllm.com/agents-md-guide), [MCP: spec 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/), [MCP: roadmap](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/), [WorkOS: MCP 2026](https://workos.com/blog/everything-your-team-needs-to-know-about-mcp-in-2026), [adr.github.io](https://adr.github.io/)_

### Digital Transformation

- **De "prompt" para "context" para "harness":** a disciplina migrou de escrever bons prompts para projetar o ambiente do agente
- **Humanos como orquestradores e governança:** o SDLC agêntico reorganiza a entrega em torno do contexto, não do código
- **Observabilidade de agentes:** a AWS lançou o CloudWatch Coding Agent Insights (telemetria de Claude Code, Codex e Copilot); o context rot virou métrica acompanhada por líderes
- **SDD entrando no mainstream:** Spec Kit (93 mil+ estrelas, 30+ agentes suportados), BMAD e OpenSpec (48 mil+ cada), Kiro e Tessl
_Sources: [Cruxdigits: context engineering 2026](https://cruxdigits.nl/blog/context-engineering-ai-agents-2026/), [Codewave: agentic SDLC](https://codewave.com/feeds/blog/latest-updates-trends-coding-agents-sdlc-automation-ai-2026), [MarkTechPost: SDD tools](https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/)_

### Innovation Patterns

**1. Context rot muda a premissa de "o repo tem tudo":**
- A acurácia cai com o tamanho do contexto **mesmo quando toda a informação relevante está presente**. As degradações relatadas vão de 13,9% a 85%.
- Informação no **meio** do contexto rende 15 a 20 pontos percentuais a menos do que no início ou no fim.
- **Implicação:** "materializar tudo no repo" **não pode significar "carregar tudo no contexto"**. O harness precisa ser **em camadas e sob demanda**.

**2. Três técnicas consolidadas de gestão de contexto:**
- **Compactação:** resumir o histórico
- **Poda:** descartar tokens velhos ou redundantes
- **Isolamento:** subagentes que fazem o trabalho ruidoso e devolvem resumos de 1 a 2 mil tokens. O sistema multiagente da Anthropic superou o agente único em **90,2%** nas avaliações internas.

**3. Grafos de código como mapa, não como prompt:** grafos (codebase-memory-mcp, CodeGraph) cortam de 47% a 99% dos tokens porque o agente **consulta** o mapa em vez de ler arquivos.

**4. Convergência em "arquivos + protocolo":** o conteúdo estático e versionável vai para arquivos (AGENTS.md, SKILL.md) e o dinâmico ou volumoso é consultado via MCP.
_Sources: [arXiv: context rot em long-horizon](https://arxiv.org/pdf/2606.29718), [Morph: context rot](https://www.morphllm.com/context-rot), [Stack Underflow: subagent isolation](https://www.thestackunderflow.com/tutorials/subagent-isolation-context-rot/), [Zylos: context rotation](https://zylos.ai/research/2026-08-31-context-rotation-session-handoff-long-running-agents/), [arXiv: Tokalator](https://arxiv.org/pdf/2604.08290), [Digital Applied: reliability playbook](https://www.digitalapplied.com/blog/context-engineering-agent-reliability-playbook-2026), [ToKnow: codebase-memory-mcp](https://toknow.ai/posts/codebase-memory-mcp-knowledge-graph-99-fewer-tokens/)_

### Future Outlook

- **Registry MCP verificado** (4º tri de 2026) e autorização enterprise facilitarão a distribuição de servidores MCP corporativos
- **Agentes nativos absorvendo camadas:** memória, skills, rules e plan mode viram funcionalidades padrão; o valor migra para **o conteúdo do contexto e sua governança**
- **Sensors ainda imaturos:** Fowler aponta que não existe métrica estabelecida de cobertura ou qualidade de harness, e o *behaviour harness* é o menos maduro. É um espaço aberto
- **Gartner já tem um MQ de "Enterprise AI Coding Agents"**, com contexto como critério. A categoria vai se formalizar em 12 a 24 meses (confiança média)

### Implementation Opportunities

**O insight técnico central para o harness_corp: a hierarquia de contexto já existe nos padrões.**

A hierarquia **Empresa → Domínio → Repo → Módulo** que o harness_corp propõe **mapeia diretamente** para mecanismos padrão:

| Camada harness_corp | Mecanismo padrão | Carregamento |
|---|---|---|
| **Empresa** (boas práticas globais) | Plugin ou pacote de skills da empresa (instalado via marketplace privado) | Progressive disclosure: só metadados |
| **Domínio (macro)** | `docs/context/domain.md` curto + **servidor MCP do grafo** para consultas | Resumo fixo + consulta sob demanda |
| **Repo (micro)** | `AGENTS.md` na raiz (+ export para CLAUDE.md, Cursor, Copilot) | Sempre carregado; **deve ser curto** |
| **Módulo** | `AGENTS.md` aninhados (o mais próximo prevalece) | Carregado ao editar a pasta |
| **Definições da cadeia** (regras de negócio, ADRs, PRDs, tarefas) | `docs/` com ADRs e specs + skills que sabem ler esses arquivos | Sob demanda |
| **Código em volta** (vizinhos no grafo) | `docs/context/neighbors/*.md` (contratos resumidos) + MCP para detalhe | Sob demanda |
| **Agentes por papel** | Skills e subagentes por papel (PM, arquiteto, TL, dev) | Isolamento de contexto |

Portanto, **o harness_corp não precisa inventar formato**. O valor está em **gerar, curar, versionar e manter atualizado** esse conteúdo a partir das fontes e da cadeia de papéis.

**Outras oportunidades:**
- **Métrica de "cobertura de harness":** o mercado não tem uma. Criar a sua vira narrativa e funcionalidade (ex.: % de repos com AGENTS.md aprovado, % de vizinhos com contrato resumido, idade média do contexto)
- **Detecção de drift:** avisar quando o código ou a fonte mudou e o harness ficou velho
- **Boa prática → guide + sensor:** gerar a regra no AGENTS.md *e* a checagem correspondente (lint, teste)

### Challenges and Risks

- **Context rot:** "tudo no repo" mal desenhado piora o agente. Mitigação: AGENTS.md curto, progressive disclosure e consulta via MCP
- **Contexto desatualizado:** um harness velho é pior que nenhum. Mitigação: drift detection e regeneração com revisão por PR
- **Fragmentação entre ferramentas:** apesar do AGENTS.md e do SKILL.md, cada ferramenta tem particularidades (CLAUDE.md, `.cursor/rules`, `copilot-instructions.md`). Mitigação: modelo canônico + exportadores
- **Spec em evolução:** o MCP mudou bastante em 2026 (remoção de sessão). Mitigação: depender de SDKs oficiais
- **Harnessability do legado:** codebases sem fronteiras claras geram grafos ruidosos. Mitigação: começar por domínios bem delimitados

---

## Recommendations

### Technology Adoption Strategy

1. **Adotar os padrões da AAIF como base:** AGENTS.md (com aninhamento) + SKILL.md + MCP. Não criar formato proprietário para o que é consumido pelo agente.
2. **Modelo híbrido "materializado + consultável":** o essencial e curado vai **versionado no repo**; o volumoso e dinâmico (grafo do domínio, código vizinho detalhado) vai **via MCP**.
3. **Incorporar, não reconstruir, o grafo de código:** avaliar codebase-memory-mcp, Cognee e similares como motor do micro e do cross-service. A energia própria vai para o **grafo de domínio com semântica de negócio** (donos, decisões, regras) e para a **cadeia entre papéis**.
4. **Vocabulário oficial:** adotar o glossário acima (Fowler + Anthropic) em produto, docs e pitch.

### Innovation Roadmap

| Fase | Foco | Entrega |
|---|---|---|
| **MVP (local)** | Guides do repo + vizinhos | Conectores Git/Confluence/Docs → AGENTS.md hierárquico + skills + contexto dos vizinhos, com aprovação via PR |
| **V1** | Cadeia de papéis | Camadas por papel (negócio, arquiteto, TL) com dono e aprovação; transcrições → decisões/ADRs |
| **V2** | Grafo de domínio via MCP + marketplace privado | Servidor MCP do domínio; catálogo de skills e agentes por empresa e papel |
| **V3** | Sensors + métricas | Boa prática → lint ou teste; métrica de cobertura de harness; detecção de drift |

### Risk Mitigation

- **Risco de PI (Lei 9.609/98):** desenvolver o MVP com repos **open source ou sintéticos**; validar o contrato de trabalho antes
- **Context rot:** orçamento de tokens por camada como requisito do PRD (ex.: AGENTS.md raiz ≤ N linhas)
- **Absorção por vendors:** focar no que eles não fazem: autoria em cadeia entre papéis, fontes corporativas e curadoria
- **Nome:** evitar "harness" como marca principal

---

# Síntese: o gargalo é o contexto, e ninguém é dono da sua autoria

_Pesquisa de domínio sobre Harness Engineering e Context Engineering para desenvolvimento assistido por IA: definições, padrões e concorrência_

## Executive Summary

Em 2026, quase todo dev profissional usa agentes de código (90% toda semana), mas quase ninguém confia no que eles produzem (~3% confiam muito). O consenso da indústria é que **o gargalo não é o modelo, é o contexto**. Em grandes empresas, "context engineering e gestão de contexto em escala" é o principal desafio citado. O benchmark da Sourcegraph mostrou que agentes com **100 mil tokens** de resumo do codebase foram **piores** do que agentes com **5 mil tokens** de recuperação direcionada. Mais contexto não é melhor contexto.

O vocabulário e a infraestrutura se consolidaram rápido. *Harness* (tudo exceto o modelo), *guides/sensors* e *context engineering* têm definições canônicas (Fowler, Anthropic). **AGENTS.md e MCP** estão sob governança neutra da Linux Foundation (AAIF), e o **SKILL.md** é padrão aberto em ~40 ferramentas. A hierarquia de contexto que o harness_corp propõe (Empresa → Domínio → Repo → Módulo) **já tem mecanismo padrão** para ser expressa: AGENTS.md aninhados, skills com *progressive disclosure* e MCP para consulta.

A concorrência é intensa e bem capitalizada nos *context engines* (Augment, Unblocked, Tabnine), nos registries de skills (Tessl) e nas plataformas de entrega (Harness Inc.), e é gratuita no método (Spec Kit, BMAD) e nos grafos de código (codebase-memory-mcp, Cognee). A brecha identificada: **os engines disputam o "ponto de verdade" e os agentes controlam o "ponto de consumo", mas ninguém é dono do "ponto de autoria"**, que é o contexto construído em cadeia entre papéis (negócio → arquiteto → tech lead → dev), curado, versionado e materializado no repo.

**Principais achados:**

- **Mercado:** o mercado-mãe de ferramentas de IA para código vale US$ 9,5 a 16 bi (2026), com CAGR de 22% a 37%; o segmento contexto/harness está em formação e sem medição própria
- **Regulatório:** o risco mais crítico é a **titularidade do produto (Lei 9.609/98, art. 4º)** se ele for construído com dados ou recursos da empregadora; a LGPD pesa sobre transcrições (a ANPD prioriza IA em 2026–27); local-first é uma vantagem de compliance
- **Tecnologia:** context rot (degradação de 14% a 85% com contexto longo) obriga a um harness **em camadas e sob demanda**, não "tudo no prompt"; os padrões abertos resolvem o formato
- **Estratégia:** o valor defensável está em **gerar, curar, versionar e manter** o contexto, não em indexar código nem em definir formato

**Recomendações estratégicas:**

1. **Posicionar como "autoria de contexto em cadeia"**, não como mais um context engine
2. **Adotar AGENTS.md + SKILL.md + MCP** como base; modelo híbrido: essencial versionado no repo, volumoso via MCP
3. **Incorporar grafos de código open source** e investir no grafo de **domínio com semântica de negócio** (donos, decisões, regras)
4. **Resolver o risco de PI antes de codar:** MVP com repos open source ou sintéticos, e revisão do contrato de trabalho
5. **Trocar o nome:** "harness" colide com a Harness Inc. e com o harness-engineering.ai

_Sources: [The New Stack: context is the bottleneck](https://thenewstack.io/context-is-ai-codings-real-bottleneck-in-2026/), [Sourcegraph: context engineering](https://sourcegraph.com/blog/context-engineering), [Dev|Journal: AI bottleneck](https://earezki.com/ai-news/2026-07-24-no-dumb-questions-what-is-the-ai-bottleneck-how-does-context-engineering-fix-it/), [Reactify: context engineering 2026](https://www.reactify-solutions.com/articles/context-engineering-ai-agents-2026)_

## Table of Contents

1. Research Introduction and Methodology (abaixo)
2. Industry Overview and Market Dynamics → seção **Industry Analysis**
3. Technology Landscape and Innovation Trends → seção **Technical Trends and Innovation**
4. Regulatory Framework and Compliance → seção **Regulatory Requirements**
5. Competitive Landscape and Ecosystem → seção **Competitive Landscape**
6. Strategic Insights and Domain Opportunities (abaixo)
7. Implementation Considerations and Risk Assessment (abaixo + **Risk Assessment**)
8. Future Outlook and Strategic Planning (abaixo + **Recommendations**)
9. Research Methodology and Source Verification (abaixo)
10. Appendices: glossário e matriz competitiva (nas seções acima e no `addendum.md` do brief)

## 1. Research Introduction and Methodology

### Research Significance

A pesquisa existe para embasar o brief e o PRD do harness_corp num momento em que (a) a adoção de agentes é universal, (b) o vocabulário de harness e contexto acabou de se formar e (c) os padrões acabaram de ganhar governança neutra. É uma janela em que as categorias ainda estão sendo nomeadas e o posicionamento ainda está disponível.
_Why this research matters now:_ 57% das organizações já rodam agentes em produção (LangChain 2026), e cerca de 65% das falhas de agentes enterprise são atribuídas a *context drift*, não à capacidade do modelo (número amplamente citado; confiança média)
_Source: [Dev|Journal](https://earezki.com/ai-news/2026-07-24-no-dumb-questions-what-is-the-ai-bottleneck-how-does-context-engineering-fix-it/), [The New Stack](https://thenewstack.io/context-is-ai-codings-real-bottleneck-in-2026/)_

### Research Methodology

- **Research Scope:** (a) definições e padrões, (b) concorrência; regulatório e econômico com peso leve
- **Data Sources:** ~30 buscas web (set/2026); fontes primárias quando disponíveis (Linux Foundation, spec do MCP, agentskills, Planalto, Comissão Europeia, blogs oficiais de vendors) e secundárias (relatórios de mercado, análises)
- **Analysis Framework:** camadas da cadeia de valor (modelo → agente → harness → contexto → sensors → fontes) + matriz de capacidades frente à proposta do harness_corp
- **Time Period:** foco em 2025–2026
- **Geographic Coverage:** global, com recorte Brasil para o regulatório (LGPD, Lei do Software)

### Research Goals and Objectives

**Original Goals:** embasar brief e PRD do harness_corp; consolidar definições e padrões; mapear a concorrência; afiar o diferencial e o escopo do MVP

**Achieved Objectives:**

- **Definições consolidadas:** glossário canônico com 12 termos e fontes
- **Padrões mapeados:** AGENTS.md (aninhado), SKILL.md, MCP (spec 2026-07-28), AAIF, com o mapeamento camada ↔ mecanismo
- **Concorrência mapeada:** 5 grupos, mais de 15 players e matriz de capacidades
- **Diferencial afiado:** "ponto de autoria em cadeia"
- **Escopo do MVP informado:** harness híbrido, grafo incorporado, local-first
- **Achados não previstos:** risco de PI (Lei 9.609/98), colisão de nome e context rot como restrição de design

## 6. Strategic Insights and Domain Opportunities

### Cross-Domain Synthesis

_Market-Technology Convergence:_ o mercado converge em **arquivos abertos + protocolo** (AGENTS.md/SKILL.md + MCP). Isso rebaixa o valor de formatos e indexação e eleva o valor de **conteúdo curado e governado**
_Regulatory-Strategic Alignment:_ local-first + BYO LLM + curadoria com trilha de auditoria atende LGPD, Shadow AI e ISO 42001 ao mesmo tempo. **Compliance vira argumento de venda**, não só custo
_Competitive Positioning Opportunities:_ contraste direto com o Unblocked ("eles respondem na hora; nós preparamos o repo antes da tarefa, curado e versionado"); com o Tessl ("registry público vs catálogo privado por papel e por empresa")

### Strategic Opportunities

_Market Opportunities:_ empresas com domínios de 20 a 50 repos, documentação fragmentada e agentes já adotados; Brasil sem player local identificado
_Technology Opportunities:_ (1) **métrica de "cobertura de harness"**, que o mercado não tem; (2) **detecção de drift** entre fontes e harness; (3) **boa prática → guide + sensor**; (4) transcrição → decisão/ADR ligada ao grafo
_Partnership Opportunities:_ comunidade BMAD como canal (o próprio harness_corp usa BMAD); integração com grafos OSS; diretório de parceiros de skills (Atlassian já está lá)

## 7. Implementation Considerations and Risk Assessment

### Implementation Framework

_Implementation Timeline:_ MVP local (guides do repo + vizinhos) → V1 cadeia de papéis + transcrições → V2 MCP do domínio + marketplace privado → V3 sensors + métricas + drift (detalhes em **Recommendations → Innovation Roadmap**)
_Resource Requirements:_ conectores (Git, Confluence, Google Docs), pipeline de extração e curadoria com LLM, exportadores multi-ferramenta, scanner de segredos, integração com um grafo OSS
_Success Factors:_ AGENTS.md curtos e de alto sinal; curadoria humana rápida (aprovação via PR); domínio piloto bem delimitado; medir o acerto na 1ª tentativa antes e depois

### Risk Management and Mitigation

_Implementation Risks:_ context rot por excesso de material → orçamento de tokens por camada; harness desatualizado → drift detection
_Market Risks:_ absorção por vendors de agente → foco em autoria em cadeia e fontes corporativas; concorrentes bem capitalizados → nicho (arquitetos, domínios médios, local-first)
_Legal Risks:_ **PI da empregadora (crítico)** → repos OSS ou sintéticos + revisão contratual; LGPD em transcrições → minimização e consentimento
_Technology Risks:_ specs em evolução (MCP) → SDKs oficiais; legado pouco "harnessável" → começar por domínios com fronteiras claras

## 8. Future Outlook and Strategic Planning

### Future Trends and Projections

_Near-term Outlook (1–2 anos):_ registry MCP verificado (4º tri de 2026); categoria "contexto para agentes" formalizada por analistas (Gartner MQ já existe); M&A de startups de contexto
_Medium-term Trends (3–5 anos):_ o valor migra do agente para o contexto governado; sensors e métricas de qualidade de harness amadurecem
_Long-term Vision (5+ anos):_ o contexto organizacional vira ativo versionado como o código ("context as code")

### Strategic Recommendations

_Immediate Actions (próximos 6 meses):_
1. Resolver o risco de PI (contrato + decisão sobre os dados do piloto)
2. Escolher um nome sem "harness"
3. Montar um domínio piloto com 20 a 50 repos open source ou sintéticos
4. Construir o MVP: fontes → AGENTS.md hierárquico + skills + vizinhos, aprovados via PR
5. Medir o acerto na 1ª tentativa com e sem harness

_Strategic Initiatives (1–2 anos):_ cadeia de papéis; transcrições → decisões; MCP do grafo de domínio; marketplace privado
_Long-term Strategy (3+ anos):_ dono da categoria "autoria de contexto"; sensors gerados a partir de boas práticas; métrica padrão de cobertura de harness

## 9. Research Methodology and Source Verification

### Comprehensive Source Documentation

_Primary Sources:_ Linux Foundation (AAIF), blog/spec do MCP, agentskills (GitHub), Martin Fowler, Anthropic Engineering, Planalto (Lei 9.609/98), Comissão Europeia (AI Act), blogs oficiais (Unblocked, Augment, Tabnine, Tessl, Harness)
_Secondary Sources:_ Grand View, Mordor, Research and Markets, JetBrains Research, Sonar, METR (via agregadores), DEV Community, The New Stack, arXiv
_Web Search Queries:_ ~30 consultas cobrindo mercado, funding, SDD, adoção e confiança, context engines, Tessl, Harness Inc., grafos de código, marketplaces de skills, preços, transcrição → PRD, LGPD/ANPD, Lei do Software, EU AI Act, SOC 2/ISO 42001, consentimento em gravação, AAIF, SKILL.md, context rot, AGENTS.md aninhado, spec do MCP e importância do context engineering

### Research Quality Assurance

_Source Verification:_ afirmações críticas (funding, padrões, lei) com fonte primária ou pelo menos duas fontes
_Confidence Levels:_ **alta** para padrões, governança e lei; **média** para tamanho de mercado e estatísticas de adoção; **baixa** para participação de mercado no segmento de contexto e para os preços da Unblocked (não confirmados)
_Limitations:_ (1) a validação de usuário vem da experiência do fundador e de conversas informais com **arquitetos, devs, tech leads e PMs**, justamente os papéis da cadeia de contexto; relataram **a mesma dor** do fundador e **topariam testar**; sobre pagar, a percepção é de que a compra seria **corporativa** (a empresa paga, não o indivíduo). A quantidade de conversas não foi registrada; (2) funcionalidades de concorrentes avaliadas por material público, sem demo; (3) números de benchmark de vendors são autodeclarados; (4) análise jurídica não substitui parecer de advogado
_Methodology Transparency:_ todas as fontes citadas inline nas seções

---

## Research Conclusion

### Summary of Key Findings

O problema é real e reconhecido pelo mercado: o contexto, não o modelo, é o gargalo. Os padrões para expressar o contexto já existem e são neutros. A concorrência é forte em **recuperar** contexto e fraca em **construir** contexto de forma colaborativa entre papéis. O harness_corp tem uma brecha real se ficar na autoria em cadeia, e riscos reais de PI, nome e context rot que precisam de resposta antes do código.

### Strategic Impact Assessment

A pesquisa **confirma** a tese central do brief (a cadeia de contexto entre papéis materializada no repo), **corrige** três pontos (grafo incorporado em vez de construído; "tudo no repo" como tudo *disponível*, não tudo *carregado*; domínio piloto não pode usar dados da empregadora sem acordo) e **adiciona** o vocabulário e o mapeamento técnico para o PRD.

### Next Steps Recommendations

1. **Atualizar o product brief** com: posicionamento "autoria em cadeia", modelo híbrido, risco de PI, nome e glossário
2. **Registrar as conversas já feitas** com outros profissionais (papel, dor citada, se pagariam) como evidência no brief e no PRD
3. Seguir para o **PRD** (`bmad-prd`) e depois para a **arquitetura** (`bmad-architecture`)

---

**Research Completion Date:** 2026-09-26
**Research Period:** 2025–2026
**Source Verification:** fatos citados com fontes
**Confidence Level:** média-alta (ver Quality Assurance)
