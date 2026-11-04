# Plano de geração — U4 / História 2.4

## Escopo

Implementar `sinter read <doc>[#<âncora>]` para documentos Markdown locais do catálogo. Sem âncora, devolver índice compacto de títulos, âncoras e tamanho das seções; com âncora, devolver o trecho até o próximo título do mesmo nível ou superior. Aceitar documento por id ou caminho, listar âncoras ao falhar, e para documentos só com URL mostrar o link com aviso, sem fazer leitura externa. Rastreabilidade: FR16 e NFR5.

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

- [x] Inspecionar modelo Doc, indexação de documentos, resolução de paths, CLI e utilitários de texto; preservar as fronteiras do hexágono.
- [x] Confirmar pytest/poe existentes e registrar comandos direcionado e completo.
- [x] Implementar serviço de Markdown: headings ATX, slug compatível com âncoras GitHub (normalização sem acentos), headings duplicados com sufixos, níveis e tamanhos de seção.
- [x] Implementar extração da seção alvo incluindo o heading e parando antes do próximo heading do mesmo nível ou superior; listar âncoras válidas no erro.
- [x] Implementar resolução de documento por id, path declarado e path canônico; rejeitar traversal, paths fora de `docs/` e extensões não Markdown.
- [x] Implementar caso de uso `Read` com índice de docs ligados ao catálogo; URL-only retorna URL e aviso, sem acesso de rede.
- [x] Expor `sinter read <doc>[#anchor]` e render textual/JSON usando os padrões de comando e erros existentes.
- [x] Criar testes de serviço (5–8 casos) para slugs, acentos, pontuação, duplicatas, tamanho, hierarquia, headings sem seção e finais de arquivo.
- [x] Criar testes de aplicação e CLI (5–8 por componente) para id/path, âncora, sem âncora, erro e âncoras disponíveis, URL-only, segurança de path e saída/código.
- [x] Executar testes direcionados e `poe check`; corrigir as regressões sem afrouxar checks.
- [x] Registrar resumo, manifesto de fontes e rastreabilidade FR16/NFR5.

## Verificação prevista

- Teste direcionado: `uv run --directory sinter pytest tests/domain/test_markdown.py tests/application/test_read.py tests/cli/test_read_cli.py`
- Verificação completa autorizada: `uv run --project sinter --directory sinter poe check`

## Critérios de aceite

Implementar os quatro cenários de Story 2.4 em `docs/prd-dominio-2026-10-17/epics.md`. Seções são delimitadas por headings Markdown; URL-only não consulta rede; saída sem âncora contém só índice e tamanhos, não o documento inteiro.
