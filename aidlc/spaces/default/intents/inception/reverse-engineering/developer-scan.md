## Developer Code Scan Results

### Scan Coverage

- **Analyzed deeply**:
  - sinter/src/ — modelos, portas, casos de uso, validação, CLI e adaptadores escritos à mão; caches excluídos.
  - sinter/pyproject.toml
  - sinter/README.md
  - sinter/.gitignore
  - .github/workflows/sinter-check.yml
  - scripts/with-aidlc.sh
  - docs/ai-dlc.md
- **Skimmed only**:
  - sinter/tests/ — listagem completa e leitura de testes representativos; fixtures/golden não lidos integralmente.
  - sinter/schemas/ — inventário de arquivos derivados.
  - sinter/uv.lock — nomes e versões.
  - .agents/skills/ — inventário não-AI-DLC; leitura da skill sinter-documentar, dois scripts e início do gerador de site.
  - _bmad/ e _bmad-output/ — organização de apoio e planejamento, sem leitura integral.
  - docs/prd-dominio-2026-10-17/ — índice e início do PRD, sem todos os requisitos/exemplos.
  - prd-yaml.md — títulos da proposta ampla.
  - Exemplo.drawio.xml — presença, sem interpretar diagrama.
  - README.md — tamanho mínimo observado; skills-lock.json lido.
- **Left out**:
  - .git/
  - .claude/, .codex/ e aidlc/ (instalação/registros AI-DLC; instruções e manifests lidos apenas para executar esta tarefa, não como aplicação).
  - .agents/skills/aidlc*/ e runners gerados pelo AI-DLC.
  - .aidlc-tools/ ignorado.
  - sinter/.venv/, .import_linter_cache/, .mypy_cache/, .pytest_cache/, .ruff_cache/ e __pycache__/.
  - fixtures de repositórios de avaliações ignoradas pela raiz.
  - Seções gerenciadas AI-DLC de AGENTS.md e .gitignore.

### Packages Found

- sinter — CLI Python 0.1.0 de catálogo YAML local.
- Ferramentas de documentação independentes em .agents/skills/sinter-documentar/scripts/; sem dependência de importação observada pelo pacote.
- BMAD e skills são materiais de apoio; não foram confundidos com serviços do produto.

### Build System

- **Type**: hatchling, uv e Poe.
- **Config Files**: sinter/pyproject.toml, sinter/uv.lock, .github/workflows/sinter-check.yml.
- **Build Dependencies**: único pacote src/sinter; console script aponta para adapters.inbound.cli.app:main. Contratos hexagonais por import-linter.

### APIs Discovered

- CLI — sinter/src/sinter/adapters/inbound/cli/commands/ — validate, get e schema export.
- Portas — sinter/src/sinter/ports/ — DTOs de entrada/saída e protocolos CatalogFiles/ManifestCodec/LocalFiles.
- Contratos YAML — oito kinds em domain/model/registry.py; JSON Schemas derivados.
- Sem endpoints HTTP ou clientes de integração remota observados no pacote.

### Frameworks & Libraries

- Pydantic 2.14.1, Typer 0.27.3 e ruamel.yaml 0.19.1 conforme lock.
- Python >=3.13; pytest, Ruff, mypy, import-linter e Poe para desenvolvimento.

### Test Coverage

- **Test Directories**: sinter/tests/{domain,application,adapters,cli,contract,fixtures,golden}; test_perf.py e test_fixture_em_dia.py.
- **Test Frameworks**: pytest.
- **Coverage Config**: não observada no pyproject; sem percentual medido.
- Testes e builds não executados por este scan.

### Code Quality Indicators

- **Linting**: Ruff e import-linter em sinter/pyproject.toml; mypy strict para src.
- **CI/CD**: .github/workflows/sinter-check.yml, Ubuntu/macOS × Python 3.13/3.14, uv sync --locked e poe check.
- **Documentation**: README do pacote e extensos documentos de produto; raiz com README mínimo.
- Erros e relatórios estruturados, separação de I/O por protocolos e adaptadores de memória.

### Technical Debt Signals

- application/get.py limita a saída a nível 1 embora CLI e DTO aceitem nível 2.
- ports/inbound/schema_export.py publica GetResult, mas schemas/ não contém get-result.schema.json; tests/contract/test_schemas.py ainda espera 11 arquivos (agora seriam 12).
- Get ignora findings do load; política de consulta em catálogo inválido requer cuidado.
- Filesystem não verifica contenção de caminhos após join; examinar confiança em catálogo/destinos.
- golden fixture cria baseline quando arquivo está ausente.
- Busca em fontes/testes não encontrou TODO/FIXME/HACK; um type ignore na fixture foi observado.

## Handoff Summary

- **Intent-relevant finding**: implementação real é CLI local hexagonal de consulta/validação; propostas de criação/edição/descoberta não devem ser tratadas como funcionalidades prontas. Evidência: sinter/src/sinter/adapters/inbound/cli/app.py registra apenas validate/get/schema; application/get.py entrega até nível 1.
- **Risks / follow-up**: cobertura profunda parcial, explicitamente declarada; possível quebra estática de contrato de schemas, sem testes executados. Preservar trabalho local e não corrigir código nesta análise.
- **Publication**: nove candidatos produzidos em staging e publicados somente pela ferramenta transacional; root registra a conclusão do link.

