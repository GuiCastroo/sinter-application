# Plano de entrega — histórias restantes

## Sources

- `../units-generation/unit-of-work.md`: fronteiras e entregas.
- `../units-generation/unit-of-work-dependency.md`: DAG técnico aprovado.
- `../units-generation/unit-of-work-story-map.md`: histórias e requisitos atribuídos.
- `docs/prd-dominio-2026-10-17/epics.md` e `_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md`: critérios e contratos existentes.

## Estratégia e execução

Um Bolt, uma passagem de construção de uma história que termina em resultado verificável, contém exatamente uma unidade. Execução serial, unidade por unidade, sem agrupamento ou paralelismo. Primeiro concluir a consulta já iniciada; depois completar a leitura do catálogo, medir sua fidelidade e construir autoria sobre formatação canônica. Skills entram depois dos comandos que consomem. A ordem abaixo respeita o DAG; a seleção em tempo de execução usa o DAG aprovado e as configurações registradas, não este documento para alterar dependências.

## Sequência

| Bolt | Unidade | História | Entrega e demonstração | Hipótese verificável |
|---|---|---|---|---|
| B01 | U1 — u1-get-niveis | 2.1 | get dom-pagv --level 1 --json, com origem herdada | Níveis 0/1 e herança atende todos os critérios da história 2.1 sem quebrar capacidades concluídas |
| B02 | U2 — u2-calculados | 2.2 | get dom-pagv/sub-camb-carteira com calculados corretos | Repos, fronteiras, modernização e dados atende todos os critérios da história 2.2 sem quebrar capacidades concluídas |
| B03 | U3 — u3-jornadas | 2.3 | get jornada e vizinhança level 2 sem repetir ciclos | Jornadas, navegação e nível 2 atende todos os critérios da história 2.3 sem quebrar capacidades concluídas |
| B04 | U4 — u4-read | 2.4 | read doc e doc#âncora sem conteúdo externo | Seções Markdown atende todos os critérios da história 2.4 sem quebrar capacidades concluídas |
| B05 | U5 — u5-find-areas | 2.5 | find cambio/boleta, list areas/domains e get area | Busca, listas e áreas atende todos os critérios da história 2.5 sem quebrar capacidades concluídas |
| B06 | U6 — u6-avaliacao-ia | 2.6 | gabarito recuperável; rodadas reais Sinter/base e Q9 | Avaliação SM-2 atende todos os critérios da história 2.6 sem quebrar capacidades concluídas |
| B07 | U7 — u7-catalog-init | 3.1 | init em diretório vazio; repetição idempotente | Início de catálogo atende todos os critérios da história 3.1 sem quebrar capacidades concluídas |
| B08 | U13 — u13-fmt | 3.7 | fmt --check e segunda formatação sem mudança | Formatação canônica atende todos os critérios da história 3.7 sem quebrar capacidades concluídas |
| B09 | U8 — u8-apply-dry-run | 3.2 | apply --dry-run sem modificar árvore/HEAD | Conferência de rascunho atende todos os critérios da história 3.2 sem quebrar capacidades concluídas |
| B10 | U9 — u9-apply | 3.3 | apply em Git sintético com commit único e rollback | Gravação transacional atende todos os critérios da história 3.3 sem quebrar capacidades concluídas |
| B11 | U10 — u10-new-domain | 3.4 | new domain preenchido e aplicado | Rascunho de domínio atende todos os critérios da história 3.4 sem quebrar capacidades concluídas |
| B12 | U11 — u11-new-subdomain-journey | 3.5 | new subdomain/journey, sumário válido e comentários | Rascunhos de subdomínio e jornada atende todos os critérios da história 3.5 sem quebrar capacidades concluídas |
| B13 | U12 — u12-get-raw | 3.6 | get --raw exato e edição com aviso de contador | Edição pelo conteúdo atual atende todos os critérios da história 3.6 sem quebrar capacidades concluídas |
| B14 | U14 — u14-sinter-find | 4.1 | sinter-find resolve boleta sem escrever | Skill de consulta atende todos os critérios da história 4.1 sem quebrar capacidades concluídas |
| B15 | U15 — u15-entrevista | 4.2 | entrevista trata resposta vaga e não sei | Entrevista guiada atende todos os critérios da história 4.2 sem quebrar capacidades concluídas |
| B16 | U16 — u16-skill-criar | 4.3 | criação busca antes e confirma dry-run | Criação guiada atende todos os critérios da história 4.3 sem quebrar capacidades concluídas |
| B17 | U17 — u17-skill-estruturar | 4.4 | nova aplicação/subdomínio/jornada com validate zero erros | Estruturação guiada atende todos os critérios da história 4.4 sem quebrar capacidades concluídas |
| B18 | U18 — u18-skills-install | 4.5 | install/update/force em diretórios sintéticos e wheel | Instalação de skills atende todos os critérios da história 4.5 sem quebrar capacidades concluídas |

## Definition of Done

Para cada Bolt: todos os critérios Dado/Quando/Então da história têm teste ou evidência real identificada; código segue AD-25–AD-48; schemas e golden atualizados intencionalmente, sem criação automática de baseline; revisão independente e correções automáticas; verificações de importação, lint, formatação, tipos e testes passam; nenhuma regressão fica escondida; evidência e decisões técnicas registradas nos artefatos da unidade. Um artefato ou roteiro sem execução exigida não prova conclusão. Confirmar critérios de token, determinismo e dados sintéticos quando aplicáveis. Ao final, executar verificação integrada.

## Política de conclusão

Construção unit-major, serial e autônoma conforme pedido. Revisões de código e testes permanecem automáticos. Não solicitar revisão humana entre histórias salvo pergunta protegida ou informação indispensável. Não publicar, fazer push ou deploy. O plano base bugfix tem skeleton off; B01 é incremento funcional real, sem impor nova aprovação de skeleton.

## Preservação

Antes de qualquer fonte alterada, registrar git status e baseline na árvore atual, incluindo módulos não rastreados. Preservar alterações locais existentes; sem stash/reset/restore/clean. Não fazer commits no repositório de trabalho apenas para limpar a árvore. Commits da funcionalidade init/apply são ensaiados em catálogos sintéticos.

## Verificação proposta

`uv run --project sinter --directory sinter poe check` executa contratos de importação, ruff check, ruff format --check, mypy e pytest (unitários, integração, CLI, contratos, golden e skills incluídos na suíte conforme criados). Evals com LLM são separados e exigem evidência própria; esta chamada não os substitui. A seleção desta chamada aguarda autorização protegida, não foi presumida pela autonomia.

