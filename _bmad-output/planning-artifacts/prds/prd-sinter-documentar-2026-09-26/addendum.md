# Addendum — Documentação de domínio

Detalhe técnico e fontes que não cabem no PRD.

## Onde está cada coisa

| Artefato | Caminho |
|---|---|
| Esqueleto v2 | `_bmad-output/planning-artifacts/padrao-documentacao/esqueleto-v2.md` |
| Exemplo de página de negócio | `_bmad-output/planning-artifacts/padrao-documentacao/exemplo-1-negocio-serverlesspresso.md` |
| Padrão v1 (substituído) | `_bmad-output/planning-artifacts/padrao-documentacao/padrao-documentacao-sinter.md` |
| Skill | `.agents/skills/sinter-documentar/` (link em `.claude/skills/`) |
| Snapshot da skill v1 | `_bmad-output/skill-evals/sinter-documentar-workspace/skill-snapshot-v1/` |
| Testes | `_bmad-output/skill-evals/sinter-documentar-workspace/iteration-1/` e `iteration-2/` (`benchmark.json`, `review.html`) |
| Critérios | `grade.py` (v1), `grade2.py` (v2, 11 critérios) |

## Como a skill está montada

- **SKILL.md**:
  - estrutura da página
  - regras de honestidade: "(a confirmar)", sem segredos
  - fluxo de baixo para cima
  - parede de eventos
  - "quem orquestra"
  - chamada dos geradores
  - teste de suficiência
- **references/**:
  - `paginas.md`: modelos das 6 páginas mais o exemplo real
  - `extracao.md`: onde achar infra, serviços, eventos e sinais de orquestrador
  - `diagramas.md`: padrões Mermaid por página
- **scripts/** (Python puro):
  - `_paginas.py`: lê as páginas (título, resumo, "Nesta página", seções, fontes, pasta dividida) e extrai as arestas das tabelas "Consome"
  - `gerar_llm.py`: gera o cartão, os resumos e o grafo, e avisa quando o orçamento estoura (`--cartao`, `--resumos`)
  - `gerar_site.py`: gera o site num único arquivo:
    - árvore H1 › H2 › H3 com IntersectionObserver
    - tema claro (`--bg #F4F6F8`, `--accent #0E8A4F`, `--link #1F5FD1`) e escuro via `data-tema="escuro"`
    - post-its da parede
    - mapa Mermaid na arquitetura
    - nó "Para IA"

## Fontes da pesquisa

- **Bounded Context Canvas** (DDD Crew): propósito, fronteira, comunicação.
- **Event Storming** (Brandolini): cores e níveis Big Picture, Process e Design.
- **Domain Storytelling vs BPMN:** no negócio usamos a narrativa; o BPMN fica para a orquestração.
- **Inception Deck, lista NOT:** faz, não faz, não sabemos.
- **Diátaxis:** tutorial, how-to, referência, explicação. Inspirou a página de referência e "como começar".
- **C4, arc42, ADRs:** arquitetura e decisões.
- **llms.txt** (llmstxt.org): cartão com seção "Optional".
- **Gartner BOAT** (primeiro MQ em 2026; Appian, UiPath e Pega como líderes, Camunda como visionária): orquestração de processo como sinal de "quem orquestra".

## Alternativas descartadas

- **Um arquivo por item (v1).** Ficou granular demais para pessoas. A IA lia muitos arquivos, e a navegação era ruim.
- **Menu à direita.** Foi um mal-entendido: o pedido era a navegação à esquerda.
- **Tema todo escuro por padrão.** Era cansativo de ler, então o claro virou o padrão.
