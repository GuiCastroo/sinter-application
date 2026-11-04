# Plano de geração — U13 / História 3.7

## Escopo

Implementar a formatação canônica da História 3.7 (`sinter fmt`), rastreada em FR18 e NFR4. A unidade deve formatar um manifesto ou todos os manifestos do catálogo, preservar comentários com seus campos/itens, usar ordem dos modelos, recuo de dois espaços, LF e linha final, ser idempotente, oferecer `--check` sem escrita e sem commit, integrar o caminho de gravação do `apply` e emitir aviso (não erro) no `validate` quando encontrar formato não canônico.

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

## Etapas

- [x] Inspecionar modelos do Apêndice A e convenções existentes; manter mudanças restritas ao formatador e aos pontos de integração de FR18.
- [x] Confirmar runner/configuração existente (pytest/poe) e preservar a configuração do projeto.
- [x] Implementar serialização round-trip com `ruamel.yaml`, ordem canônica derivada dos modelos, recuo 2, LF e newline final; preservar comentários junto ao campo/item e ordem estável dos documentos.
- [x] Implementar aplicação/porta de escrita do formatador com seleção de arquivo ou catálogo; não criar commit e não escrever em `--check`.
- [x] Implementar `sinter fmt [arquivo] [--check]`: listar arquivos fora do padrão e retornar código 1 no check; formatar todos os manifestos do catálogo sem argumento e informar quantidade alterada.
- [ ] Integrar `apply` para gravar o rascunho no formato canônico e comparar dados de negócio, ignorando diferenças apenas de layout no dry-run.
- [x] Integrar `validate` com aviso para formato não canônico, sem elevar o aviso a erro.
- [x] Escrever testes unitários e de aplicação (5–8 cenários por componente aplicável) para ordem, comentários, whitespace, LF/newline, round-trip de dados, check não destrutivo, idempotência, diretório do catálogo, caminho inválido e erros de leitura/escrita.
- [x] Escrever testes CLI/integrados sobre todos os manifestos do exemplo-catalogo: segunda formatação sem mudança, check sem escrita/código 1, formatação em lote e saída/contagem.
- [x] Rodar os testes direcionados e a verificação completa autorizada; corrigir regressões sem enfraquecer checks.
- [x] Registrar resumo, manifesto de fontes e rastreabilidade de FR18/NFR4.

## Verificação prevista

- Teste direcionado: `uv run --directory sinter pytest tests/application/test_fmt.py tests/cli/test_fmt_cli.py tests/adapters/test_yaml_fs.py tests/test_fmt_fixture.py`
- Verificação completa autorizada: `uv run --project sinter --directory sinter poe check`

## Critérios de aceite

Cobrir os seis cenários da Story 3.7 em `docs/prd-dominio-2026-10-17/epics.md`; validar preservação dos comentários e dos dados YAML, ausência de escrita no check e ausência de commit, compatibilidade round-trip, integração com `apply` e aviso de `validate`.
