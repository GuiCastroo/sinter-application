---
title: "Addendum — PRD Sinter"
created: 2026-09-26
updated: 2026-09-26
---

# Addendum — PRD Sinter

Detalhe técnico e alternativas para a arquitetura. O PRD define capacidades; aqui ficam os "comos" candidatos.

## Superfícies

| Superfície | Papéis | Uso |
|---|---|---|
| App visual (web, roda local) | Arquiteto, PM, Tech lead | Domínio, mapa, curadoria, conversas guiadas, pacote de contexto, catálogo |
| CLI (`sinter`) | Dev e agente | `init`, `task pull`, `sync`, `export`, `status` |

## Stack candidata (validar em `bmad-architecture`)

Ver a tabela completa no [addendum do brief](../../briefs/brief-harness_corp-2026-09-26/addendum.md#stack-candidata-ferramentas-avaliadas-a-validar-na-arquitetura). Resumo:
- **Graphify**: motor do grafo de código e documentos; arestas extraídas vs inferidas mapeiam para a proveniência (FR-3, FR-10). Usar atrás de uma camada de abstração.
- **Archify**: comparação de mapa atual vs proposto (FR-13).
- **Obsidian**: compatibilidade opcional do repo do domínio (Markdown + wikilinks) para quem quiser navegar fora do app.
- **BMAD Method (MIT)**: base das conversas guiadas (FR-17 a FR-20).
- **MCP**: canal para o agente consultar o grafo do domínio sob demanda (FR-29), a avaliar se entra no MVP.

## Estrutura do repo do domínio (proposta)

```
dominio-pagamentos/
├── README.md                  visão, fronteiras, donos
├── glossario.md
├── mapa/                      contexto e sistemas (C4 níveis 1 e 2)
├── sistemas/<repo>.md         ficha por sistema
├── integracoes/<contrato>.md  API, evento, fila, arquivo
├── regras-de-negocio/<regra>.md
├── decisoes/ADR-NNN.md
├── padroes/
├── tarefas/<id>/              pacote de contexto por camada
└── fontes.md                  proveniência
```

## Estrutura do `.sinter/` (proposta)

```
.sinter/
├── sinter.yaml          domínio, sistema, vizinhos, versão do padrão
├── context/
│   ├── domain.md        resumo do domínio (curto)
│   ├── neighbors/*.md   contratos dos vizinhos
│   ├── business-rules.md
│   └── decisions.md
├── tasks/<id>.md        pacote de contexto da tarefa atual
├── standards/
├── skills/              SKILL.md
├── agents/
└── flows/               nova-feature.md, bugfix.md
```

Exports gerados na raiz do repo: `AGENTS.md` (+ aninhados), `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`.

## Orçamento de contexto (referência inicial para NFR-3)

`[SUPOSIÇÃO: calibrar com testes]`
- AGENTS.md raiz: até ~150 linhas, com ponteiros para `.sinter/`
- `domain.md`: até ~1 página
- Cada vizinho: só o contrato e o essencial (até ~1/2 página)
- Pacote de contexto da tarefa: até ~5 mil tokens
- Skills: só nome e descrição carregados no início (progressive disclosure)

Base: benchmark da Sourcegraph (5 mil tokens direcionados superaram 100 mil de resumo) e pesquisa sobre *context rot*.
