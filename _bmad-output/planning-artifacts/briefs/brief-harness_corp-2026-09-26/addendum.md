---
title: "Addendum — Product Brief harness_corp"
created: 2026-09-26
updated: 2026-09-26
---

# Addendum — Product Brief harness_corp

## Glossário de referência (mercado, set/2026)

| Termo | Definição | Fonte |
|---|---|---|
| **Harness** | Tudo em um agente exceto o modelo: regras, ferramentas, contexto, checagens, orquestração. "Agent = Model + Harness". | Fowler; LangChain |
| **Harness Engineering** | Projetar os controles ao redor do agente para gerar confiança real no que ele produz. | Fowler |
| **Context Engineering** | Curar o menor conjunto de tokens de alto sinal que maximiza a chance do resultado desejado. Harness engineering é uma forma específica disso. | Anthropic; Fowler |
| **Guides (feedforward)** | Controles antes da ação: architecture.md, convenções, AGENTS.md, skills, templates. Aumentam acerto na 1ª tentativa. | Fowler |
| **Sensors (feedback)** | Controles após a ação: linters, testes, type checkers, review por IA. Permitem autocorreção. | Fowler |
| **Computacional vs inferencial** | Controles determinísticos e baratos (testes, lint) vs semânticos e caros (LLM judge, AI review). | Fowler |
| **Steering loop** | Humano melhora guides/sensors iterativamente a partir de problemas recorrentes. | Fowler |
| **Harnessability** | Quanto um codebase se deixa controlar (tipos, fronteiras de módulo). Legado é menos "harnessável". | Fowler |
| **Harness template** | Pacote pré-pronto de guides+sensors para uma topologia comum de serviço. | Fowler |
| **AGENTS.md / SKILL.md** | Padrões abertos lidos por Claude Code, Cursor, Copilot e outros. | agents.md; Anthropic |

## Métricas usadas pelo mercado

- **DORA (5)**: deployment frequency, lead time, change failure rate, recovery time, **rework rate** (adicionada em 2024).
- **First-pass acceptance**: % de mudanças do agente aceitas sem retrabalho. Deve ser lida junto com lead time e rework.
- **Indicadores implícitos de harness (Fowler)**: menos toil de review humano, menos tokens desperdiçados, menos problemas recorrentes.
- **Lacuna**: não existe métrica estabelecida de "cobertura/qualidade de harness". É uma oportunidade.

## Panorama competitivo (pesquisa rápida)

> Substituído pela pesquisa de domínio completa (seção Competitive Landscape, com matriz de capacidades): `../../research/domain-harness-engineering-context-engineering-definicoes-e-concorrencia-research-2026-09-26.md`. Mantido aqui como histórico.

- **Unblocked**: context engine sobre Confluence/Slack/Jira/GitHub, serve qualquer agente. Sobreposição alta com consolidação de fontes.
- **Augment Code**: context engine em escala, impacto cross-service.
- **Sourcegraph Cody**: busca/navegação de código.
- **Harness Inc.**: Software Factory + knowledge graph; colisão de nome.
- **Marketplaces open source** (wshobson/agents etc.): skills multi-ferramenta gratuitas.
- Padrão comum: contexto recuperado na hora (RAG/busca). Pouco foco em harness como artefato curado, versionado e governado.

## Análise de Decoupling (Thales Teixeira) — rascunho para validação

**Lente:** a disrupção vem de desacoplar a cadeia de valor do cliente (CVC) e remover as atividades que **erodem valor** (custo em dinheiro, tempo e esforço), sem tentar substituir a cadeia inteira.

**Tese:** o harness_corp não substitui Confluence, Jira, IDE nem agente. Ele **desacopla uma única atividade que erode valor e atravessa toda a jornada: o transporte de contexto entre papéis.**

### CVC: da intenção ao código

| # | Etapa | Quem | Cria valor (fica com o humano) | **Erode valor (atrito a remover)** |
|---|---|---|---|---|
| 1 | Capturar a intenção | Negócio / PM | Decidir o que e por quê | Escrever ata; decisões perdidas em reunião; "quem estava lá sabe" |
| 2 | Desenhar a solução | Arquiteto de solução | Decidir o como no todo | Reconstruir como os 20 a 50 repos se conversam; caçar docs em Confluence/Docs; perguntar para pessoas |
| 3 | Especificar | PM | Priorizar, fatiar | Repetir contexto de negócio e arquitetura em cada PRD e tarefa |
| 4 | Preparar o repo | Tech lead | Definir padrões locais | Escrever e manter AGENTS.md, skills e regras à mão; explicar vizinhos |
| 5 | Codificar | Dev / agente | Implementar | Re-explicar contexto ao agente; abrir outros repos; errar padrão ou decisão → retrabalho |
| 6 | Revisar | Tech lead / par | Julgar a solução | Checar à mão se o código respeita decisões, padrões e contratos |
| 7 | Manter | Todos | — | Docs e harness ficam velhos; ninguém atualiza; drift silencioso |

### Funcionalidades candidatas (cada uma desacopla um atrito)

| ID | Funcionalidade | Atrito removido | Etapa |
|---|---|---|---|
| F1 | **Reunião → Decisões**: transcrição vira decisões, regras e ADRs propostos, com dono, para aprovação | Ata e decisões perdidas | 1 |
| F2 | **Mapa vivo do domínio**: grafo gerado automaticamente das fontes | Reconstruir o todo | 2 |
| F3 | **Pacote de contexto que viaja com a tarefa**: cada passagem herda o contexto acumulado e o próximo papel só adiciona a sua camada | Repetir contexto a cada passagem | 2→3→4→5 |
| F4 | **Repo pronto para decolar**: um PR materializa o harness (AGENTS.md hierárquico, skills, regras, vizinhos) | Setup manual do harness | 4 |
| F5 | **Contexto sob medida para a tarefa**: localiza a tarefa no grafo e monta só o contexto relevante | Re-explicar ao agente; context rot | 5 |
| F6 | **Boas práticas consolidadas**: junta Confluence e Docs, detecta duplicatas e conflitos, e o arquiteto decide | Caçar e reconciliar documentação | 2 |
| F7 | **Harness que se atualiza**: detecta drift entre fontes, código e harness e abre PR de atualização | Manutenção; contexto velho | 7 |
| F8 | **Revisão guiada por decisões**: checa o PR contra ADRs, regras e contratos | Checagem manual no review | 6 |
| F9 | **Catálogo privado por papel**: skills e agentes da empresa reutilizáveis | Reinventar skills por projeto | 4, 5 |

## Modelo mental do produto (fundador, 2026-09-26)

**Domínio é o objeto central.**

1. Criar um **domínio** (ex.: "Pagamentos")
2. Adicionar os **repos** do domínio, sejam de código moderno ou de **mainframe** (COBOL, JCL, copybooks...)
3. A ferramenta **entende como eles se relacionam** e gera o **mapa**
4. Adicionar **documentos**: .docx, .pdf, Confluence, Google Docs, transcrições
5. Tudo é normalizado em um **padrão de documentação**, para o conhecimento não virar uma "bola de lama"

**Proposta de padrão de documentação por domínio** (inspirado em C4, arc42 e ADR; a validar):

```
dominio-pagamentos/
├── README.md                  # visão do domínio: propósito, fronteiras, donos
├── glossario.md               # linguagem do negócio (termos únicos, sem ambiguidade)
├── mapa/
│   ├── contexto.md            # C4 nível 1: domínio e vizinhos externos
│   └── sistemas.md            # C4 nível 2: repos/sistemas e integrações
├── sistemas/<repo>.md         # ficha por repo: responsabilidade, stack (inclusive mainframe), dono, expõe/consome
├── integracoes/<contrato>.md  # APIs, eventos, arquivos batch, filas: contrato + produtor/consumidor
├── regras-de-negocio/<regra>.md
├── decisoes/ADR-NNN.md        # decisões com contexto, opção escolhida, consequências
├── padroes/                   # boas práticas aprovadas → viram skills
└── fontes.md                  # rastreabilidade: de onde veio cada informação
```

Regras anti-bola-de-lama:
- Toda informação nova é **classificada em um lugar** do padrão, nunca "solta"
- **Uma verdade por assunto:** duplicatas são fundidas e conflitos vão para decisão humana
- **Toda afirmação tem fonte** (arquivo, página, trecho da reunião)
- O harness dos repos (AGENTS.md, skills, vizinhos) é **gerado a partir desse padrão**, e nunca escrito à parte

**Marketplace de skills dentro da ferramenta:** skills e agentes `.md` (padrão SKILL.md) disponíveis para instalar em um domínio ou repo, organizados por papel (PM, arquiteto, TL, dev) e por tipo (ex.: "ler COBOL", "gerar ADR", "revisar contra contratos"). Origem: skills da própria empresa (privadas) + curadas da comunidade.

## Uso no dia a dia: dois pontos de entrada

**(a) Novo projeto:** ao criar o repo, ele já nasce com a pasta `.harness/` pronta, gerada a partir do domínio:

```
novo-servico/
├── .harness/                      # modelo canônico (fonte da verdade do harness)
│   ├── harness.yaml               # domínio, papel do serviço, vizinhos, stack, versão do padrão
│   ├── context/
│   │   ├── domain.md              # resumo do domínio (vem do repo do domínio)
│   │   ├── neighbors/*.md         # contratos dos serviços com que ele fala
│   │   ├── business-rules.md      # regras de negócio relevantes
│   │   └── decisions.md           # ADRs que se aplicam
│   ├── standards/                 # padrões da empresa e da stack
│   ├── skills/                    # skills prontas (SKILL.md), vindas do marketplace
│   ├── agents/                    # agentes/subagentes por papel
│   └── flows/                     # fluxos: nova feature, bugfix, PRD → tarefa → código...
├── AGENTS.md                      # gerado a partir de .harness/ (curto)
├── CLAUDE.md / .cursor/rules / .github/copilot-instructions.md   # exports gerados
└── ...
```

**(b) Nova funcionalidade em projeto existente:** a tarefa/PRD entra, o pacote de contexto é montado (repos afetados, contratos, regras, decisões), passa pelos papéis e chega ao repo, que já tem o `.harness/`.

`.harness/` é o **modelo canônico** versionado; os arquivos de cada ferramenta são **exports gerados** (nunca editados à mão).

## Funcionalidades práticas (como se usa) — proposta

> Nota: esta tabela é anterior ao modelo "domínio como objeto central". O corte oficial do MVP está no brief (seção Escopo do MVP): no MVP entram também criar domínio, conversas guiadas, `.harness/`, fluxos e o catálogo (item 8 antecipado da V2); transcrições ficam na V1. Os caminhos `docs/context/...` foram substituídos por `.harness/context/...`.

| # | Funcionalidade | Como o usuário usa | O que sai | Quem | Fase |
|---|---|---|---|---|---|
| 1 | **Conectar fontes** | Aponta a pasta dos repos, um espaço do Confluence, uma pasta do Google Drive e uma pasta de transcrições | Inventário das fontes do domínio | Arquiteto | MVP |
| 2 | **Mapa do domínio** | Roda "mapear domínio" | `domain-map.md` + visual: repos, o que cada um expõe e consome (APIs, eventos), donos | Arquiteto | MVP |
| 3 | **Boas práticas consolidadas** | Roda "consolidar"; revisa a lista de regras com duplicatas e conflitos marcados; aprova, edita ou descarta | Pacote de skills "padrões da empresa" | Arquiteto | MVP |
| 4 | **Preparar repo** | Escolhe um repo; revisa e faz merge do PR gerado | PR com AGENTS.md curto + aninhados, exports (CLAUDE.md, Cursor, Copilot), `docs/context/domain.md`, `docs/context/neighbors/*.md`, regras de negócio, skills | Tech lead | MVP |
| 5 | **Pacote de contexto da tarefa** | Cola o PRD ou a tarefa; cada papel adiciona a sua camada (passagem de bastão) | `docs/tasks/<id>/context.md`: repos afetados, contratos, decisões e regras relevantes | PM → Arquiteto → TL → Dev | MVP |
| 6 | **Reunião → decisões** | Solta a transcrição; revisa as decisões propostas (com o trecho de origem); aprova | ADRs em `docs/decisions/` + regras de negócio atualizadas | PM / Arquiteto | V1 |
| 7 | **Atualizar harness** | Roda "verificar" (ou agenda); revisa o PR | Alerta de drift + PR de atualização | Tech lead | V1 |
| 8 | **Catálogo por papel** | Navega e instala skills ou agentes da empresa em um repo | Skills em `.claude/skills` / `.agents/` | Todos | V2 |
| 9 | **Revisão guiada por decisões** | Roda no PR (local ou CI) | Comentários: "viola ADR-012", "contrato do serviço X mudou" | Tech lead / par | V2 |

## Stack candidata (ferramentas avaliadas, a validar na arquitetura)

| Ferramenta | Papel no produto | Pontos fortes | Riscos |
|---|---|---|---|
| **Graphify** (Graphify-Labs, Apache-2.0/MIT) | Motor do grafo de código + documentos | 37 linguagens via AST (sem LLM); lê MD, SQL, PDF e áudio; arestas `EXTRACTED` vs `INFERRED`; grafo global multi-repo; servidor MCP; git hooks; exporta para Obsidian/Neo4j/JSON | Empresa YC S26 com app hospedado: pode virar concorrente → usar atrás de camada de abstração; qualidade das relações entre serviços precisa de teste |
| **Obsidian** | Interface humana do repo do domínio (vault Markdown) | Local-first; wikilinks; graph view de graça | Núcleo do app não é open source; verificar termos para uso embutido em produto comercial |
| **Archify** (tt-a1i, MIT) | Diagramas curados + delta de arquitetura (atual vs proposto) | JSON tipado e validado (versionável); componentes ligados a arquivo/linha em SHA fixo; compare base vs head | Projeto de um autor só; UI do visualizador em EN/ZH |
| **BMAD Method** (MIT) | Conversas guiadas na etapa 2 (processo, funcionalidade, solução) | Personas e workflows maduros | "BMad" é marca registrada: usar só "Works with BMad Method" |
| **codebase-memory-mcp / Cognee** | Alternativas ao Graphify | Open source; grafo via MCP | Menos cobertura de documentos |

## Pendências para o PRD

- Validar as três métricas de sucesso e definir linha de base
- Registrar as conversas de validação (quantidade, objeções, dor mais citada)
- Decidir o nome do produto (sem "harness" e sem "BMad")
- Testar o Graphify em um conjunto de repos com relações entre serviços
- Definir o orçamento de tokens por camada do `.harness/` (context rot)
- Revisar o contrato de trabalho do fundador (Lei 9.609/98) antes de construir
