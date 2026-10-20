---
title: 'Documentação Sinter v3 — três domínios com informação unificada'
type: refactor
created: 2026-09-26
status: in-review
route: dispatch
baseline_commit: NO_VCS
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="Intenção autorizada pelo pedido: faz uma nova versão assim">

## Intent

Criar uma nova versão das três documentações avaliadas, aplicando a unificação proposta e preservando a versão anterior. Manter seis perspectivas humanas, reduzir cópias integrais e produzir navegação e contexto de IA coerentes.

## Boundaries & Constraints

Preservar iteration-2 e fixtures. Gravar iteration-3 com seis Markdown por domínio, cartão, resumos, grafo, HTML e geradores locais reproduzíveis. Regras, glossário e dúvidas completos ficam em Referência, com sínteses e links nas demais páginas. Infraestrutura mantém inventário canônico. Não alterar PRD nem skill instalada, não publicar nem executar aplicações externas. Os geradores v3 ficam em iteration-3/ferramentas para revisão antes de eventual adoção pela skill. Conteúdo factual deve refletir a fixture ou marcar dúvida.

## I/O & Edge-Case Matrix

| Cenário | Entrada | Resultado |
|---|---|---|
| Títulos repetidos | Consome em vários serviços | IDs únicos com contexto e links roteados |
| Jornada | Participantes explícitos | Grafo utiliza somente participantes declarados |
| Sem dependência | Consome vazio ou travessão | Nenhuma aresta fictícia |
| Dúvida longa | Pergunta completa na Referência | Cartão preserva frase inteira e aponta origem |
| Serviços opcionais/inativos | Estado declarado | Estado preservado sem inventar fluxo de execução |
| Arquitetura | Marcador de mapa principal | Um único mapa de serviços gerado das relações |

</frozen-after-approval>

## Code Map

- Base: `_bmad-output/skill-evals/sinter-documentar-workspace/iteration-2/eval-*/with_skill/run-1/outputs/dominio-*`.
- Relatórios: `iteration-2/analise-documentacoes/`; fontes factuais: `fixtures/` no mesmo workspace.
- `_paginas.py`: parser de cabeçalhos e tabelas; extração anterior usa correspondência parcial e deve ser estrita na v3.
- `gerar_llm.py`: cartão anterior trunca texto e infere participantes por menção; substituir por perguntas e participantes explícitos.
- `gerar_site.py`: preservar estilo, parede e temas; corrigir IDs, links e mapa duplicado.

## Tasks & Acceptance

**Execution:**
- [x] `iteration-3/eval-*/with_skill/run-1/outputs/dominio-*/*.md` — copiar e editar os três conjuntos, centralizar definições, corrigir erros comprovados e índices.
- [x] `iteration-3/ferramentas/` — versionar geradores v3 locais; extrair relações tipadas de Consome e participantes explicitamente declarados; produzir um mapa e links válidos.
- [x] `iteration-3/index.html` e `README.md` — criar entrada única com os três sites e explicar mudanças/limites.
- [x] `iteration-3/verificacao.json` — verificar links, relações, preservação de originais e geração determinística.

**Acceptance Criteria:**
- Dadas as três bases v2, quando a v3 for gerada, então cada domínio mantém seis páginas e a v2 conserva seus hashes.
- Dadas regras e glossário canônicos, quando o leitor abrir páginas de contexto, então encontrará sínteses e links ao detalhe, sem tabelas completas duplicadas.
- Dadas perguntas na Referência, quando gerar cartão, então não haverá cabeçalhos vazios nem truncamento de frases.
- Dado o site, quando navegar entre páginas e subseções repetidas, então o destino corresponderá à página e ao serviço selecionados.
- Dadas as mesmas páginas, quando gerar duas vezes, então todas as saídas serão idênticas.
- Dado o grafo, quando consultar jornadas, então todas terão participantes explícitos conhecidos, sem inferência por mera menção.

## Implementation Notes

Aprovação de execução já consta no pedido do usuário. Trabalho reversível em pasta nova; nenhum efeito externo. Escolha técnica: geradores locais, mantendo a skill instalada intacta. Cartão será um índice curto; resumos acrescentam explicações de serviços/jornadas, preservando funções distintas.

## Spec Change Log

## Review Triage Log

## Verification

Validar todos os links Markdown e âncoras, IDs únicos da árvore, ausência de relações vazias, participantes conhecidos, hashes da v2 e determinismo. Executar smoke de navegação quando houver navegador disponível; informar limites se apenas inspeção estática for possível. Revisão independente dos artefatos finais.
