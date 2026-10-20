# Sinter

Catálogo de contexto para agentes de código: a estrutura dos domínios da empresa em YAML, validada e navegável pela CLI `sinter`.

```bash
uv sync
uv run sinter validate <pasta-do-catalogo>
uv run poe check        # import-linter, ruff, mypy, pytest
```

- Arquitetura: `../_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md`
- Como acrescentar comando, regra, campo ou kind: `GUIA-EXTENSAO.md` na mesma pasta.
- Testes e exemplos usam só dados sintéticos.
