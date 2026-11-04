# Plano de código — U1 / Story 2.1

## Summary

- Builds: concluir get de domínio/subdomínio nos níveis 0 e 1, herança com origem e saída determinística.
- Touches: módulos locais de get/visões/herança/níveis/tokens, bootstrap, schema GetResult e testes específicos.
- Tests: 5–8 cenários por componente com contrato, testes de aplicação e CLI, sugestões e limites de tokens.

## Sources

`docs/prd-dominio-2026-10-17/epics.md` Story 2.1; `_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md` AD-25–AD-48; `inception/units-generation/unit-of-work.md`, `unit-of-work-story-map.md` e CodeKB existente. Sem novos requisitos ou camada remota.

## Estado inicial e preservação

A árvore local já contém get.py, render/get.py, application/get.py, views.py, inheritance.py, levels.py, tokens.py e modificações rastreadas em catálogo, summary, bootstrap e exportação. Estender esses arquivos; não substituir por implementação paralela nem restaurar a árvore. Baseline de pytest: 87 passam, 2 falham por GetResult ainda sem schema e contagem fixa 11 vs 12. poe check preserva 3 contratos de importação e interrompe em dois erros Ruff (linha longa no render/get e import em inheritance). Baseline ocorrido antes de qualquer alteração de fonte nesta unidade.

## Impacto

Médio: consultas e serialização públicas, herança e contratos compartilhados. Alterações restritas à Story 2.1 e testes. Não implementar calculados/navegação de 2.2/2.3 antecipadamente. `--level 2` permanece escopo futuro com omitted honesto; não tratar como evidência de 2.3. Layout de Level0 e herança deve cumprir AD-39; preservar compatibilidade onde possível e documentar a decisão com seu teste.

## Passos

- [x] Step 1 — Confirmar pytest e fixtures/configuração existentes; registrar baseline e comandos em evidência, sem alterações de fonte (US2.1).
- [x] Step 2 — Completar modelos em sinter/src/sinter/domain/model/views.py e sinter/src/sinter/ports/inbound/get.py para campos dos níveis 0/1, gaps e origem; alinhar AD-39 e AD-38 sem duplicar visões (US2.1).
- [x] Step 3 — Criar e executar sinter/tests/domain/test_views.py para contratos de campos, serialização e validação após os modelos (US2.1).
- [x] Step 4 — Completar sinter/src/sinter/domain/services/inheritance.py, levels.py e tokens.py: herança efetiva, sumário ordenado, coleções approved, gaps e orçamentos; manter regras puras (US2.1).
- [x] Step 5 — Criar e executar sinter/tests/domain/test_inheritance.py e sinter/tests/domain/test_levels.py após implementação dos serviços; 5–8 cenários por componente, herança/gaps/status/tokens incluídos (US2.1, FR6/FR20/FR21/FR15).
- [x] Step 6 — Completar sinter/src/sinter/application/get.py e ligação sinter/src/sinter/bootstrap.py; tratar item inválido/ausente de modo explícito e sugestões determinísticas, sem assertions como erro de negócio; criar e executar sinter/tests/application/test_get.py após a camada (US2.1).
- [x] Step 7 — Completar sinter/src/sinter/adapters/inbound/cli/commands/get.py e render/get.py, app.py e summary.py onde necessário; texto e JSON mostram fatos equivalentes, não preenchido explícito, origem e omitted. Criar e executar sinter/tests/cli/test_get_cli.py após a borda (US2.1).
- [x] Step 8 — Exportar schemas intencionalmente via uv run --directory sinter poe schemas, incluindo sinter/schemas/get-result.schema.json; atualizar sinter/tests/contract/test_schemas.py para verificar conjunto esperado de resultados sem manter contagem antiga incompatível; criar regressões de contrato, sem afrouxar checagens (US2.1).
- [x] Step 9 — Executar os testes da unidade e uv run --project sinter --directory sinter poe check; corrigir falhas da unidade, incluindo Ruff/tipos; documentar decisões e critérios com evidência. Preencher code-summary.md, source-manifest.json e traceability.json, e marcar apenas passos comprovados (US2.1).

## Critérios de aceite

1. Domain level0: identidade, tipo, domainId, área, propósito e contagens corretas.
2. Domain level1: faz/não faz/não sabemos, subdomínios na ordem, regras, jornadas principais, operação, modernização, glossário, regulações, padrões, decisões e docs.
3. Listas vazias estruturadas e gaps; texto explicita não preenchido.
4. Subdomínio soma conhecimento do domínio/organização com origem; operação herda campos não declarados.
5. JSON determinístico camelCase com omitted e comando para próximo nível.
6. ITEM_NOT_FOUND saída 1 e até 3 sugestões estáveis; inválidos não viram INTERNAL_ERROR por assert.
7. CAMB nível0 ≤ ~300 e nível1 ≤ ~2000 tokens com heurística única.

## Restrições de arquivo

Não alterar fixtures de catálogo de referência para obter orçamento artificial. Não criar golden implicitamente em teste. Listar todos os arquivos de fonte/configuração/schema/testes modificados no source-manifest.json. Não editar documentos de épicos/arquitetura nem outras unidades. Nenhum push/deploy/publicação ou commit na árvore de trabalho.

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "org",
  "ordering": "implement each applicable testable layer, then write and run that layer's tests.",
  "scope": "bugfix",
  "test_strategy": "standard",
  "project_type": "brownfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    }
  ],
  "obligations": {
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Include a targeted regression for the bug or vulnerability.",
      "Keep the existing test suite green."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:734296f7a88d8aa189eebfdcf861c8053ebb1ccf67ac2988fabcdb57707f1982",
  "contract_sha256": "sha256:ff0e124d09df52363fd702db5d680f25984131a5281b88f282d59b045741218f"
}
```

