# Testes da unidade U1 — get níveis 0/1

## Comando da unidade

`uv run --directory sinter pytest tests/domain/test_views.py tests/domain/test_inheritance.py tests/domain/test_levels.py tests/application/test_get.py tests/cli/test_get_cli.py tests/contract/test_schemas.py`

## Preparação

Pytest e configuração já existem em sinter/pyproject.toml. Usar a fixture sintética oficial copiada por tests/conftest.py e adaptadores memory pelo mesmo bootstrap. Os arquivos de teste previstos são criados após a respectiva camada implementada, conforme test-after. Não executar rede nem modelo de IA.

## Cobertura esperada

5–8 cenários por componente e integração de CLI/caso de uso/codec real nos pontos relevantes; happy path e ao menos duas bordas/erros por arquivo de teste. Incluir cada critério de aceite da Story 2.1, regressão de schema ausente, origem herdada, dados vazios, status approved, item inexistente, esquema camelCase e orçamento token da fixture CAMB. Não há piso percentual de cobertura desta configuração bugfix; manter suíte existente verde e não reduzir as obrigações Standard.

## Dados e isolamento

Só dados sintéticos. Usar cópias de fixture para variantes; não editar fixture fonte nem gabarito para fazer teste passar. Portas memory para casos de erro determinísticos; teste CLI com Typer exercita integração real local. Nenhum teste depende das capacidades futuras 2.2/2.3.

## Baseline

Antes das mudanças: 87 passed, 2 failed (tests/contract/test_schemas.py). A nova exportação GetResult local introduziu ausência de arquivo e contagem antiga. Corrigir ambos e acrescentar regressões. poe check: 3 contratos íntegros, 2 findings Ruff locais. Verificação completa final é separada e autorizada no intent; este documento mantém somente o comando específico da unidade.

