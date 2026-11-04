# Qualidade e limitações observadas

Avaliação estática em 2026-10-31. Nenhum teste, build, CLI da aplicação ou programa de geração foi executado. Presença de testes e configuração não comprova aprovação nem cobertura medida.

## Indicadores

| Aspecto | Avaliação | Evidência |
|---|---|---|
| Nomes e responsabilidades | good | Casos de uso pequenos e protocolos explícitos |
| Organização e isolamento de I/O | good | bootstrap único, import-linter e adaptadores de memória |
| Erros de fronteira | good | SinterError, tabela de saídas, finding com linhas e envelope JSON |
| Tamanho/complexidade | fair | Motor simples; funções de regras e montagem de visões mais extensas |
| Testes presentes | fair | Forte conjunto validate; não foram vistos testes de Get na listagem |
| Consistência entre contrato e artefatos | poor | Divergência estática de schema de Get abaixo |
| Documentação | fair | README do pacote útil, raiz quase vazia, múltiplas propostas/versões de produto |
| Duplicação/código sem uso | fair | Helpers de regras repetidos e namespaces futuros vazios; ausência de uso não foi provada globalmente |

Os rótulos descrevem a superfície lida; não são pontuação automatizada do repositório inteiro.

## Achados concretos

### Q1 — nível 2 aceito sem implementação

`adapters/inbound/cli/commands/get.py` permite 0..2, mas `application/get.py` usa apenas visões Level0/DomainLevel1/SubdomainLevel1 e `min(request.level, 1)`. `services/levels.py` sugere nível 2 como continuação. Pode induzir agentes a repetir comando sem obter o detalhe prometido.

### Q2 — exportação e schemas/teste fora de sincronia

`ports/inbound/schema_export.py:published_results` inclui GetResult, totalizando oito kinds e quatro resultados. `sinter/schemas/` tem 11 schemas e não contém get-result.schema.json. `tests/contract/test_schemas.py` compara o conjunto inteiro e ainda espera 11 no primeiro export. Pela leitura, esses testes tendem a falhar com o código atual; não se afirma uma execução falha.

### Q3 — leitura tolerante de catálogo na consulta

`application/get.py` ignora load findings. `Catalog.manifest` pega o primeiro manifesto válido pelo ID; catálogo ordena por arquivo. Duplicatas, campos calculados ou manifestos inválidos podem não impedir consulta a um item válido, enquanto validate informa problemas. Documentar ou testar a política esperada antes de mudar comportamento.

### Q4 — contenção de caminhos não é verificada pelo adaptador

`FsCatalogFiles.read/exists` e `FsLocalFiles.read/write` fazem join com raiz/base. Não há rejeição explícita de caminho absoluto, .. ou symlink após resolução. Docs apenas consultam existência, mas ainda podem consultar fora da raiz. Avaliar de acordo com a confiança na entrada; nenhuma exploração foi feita.

### Q5 — golden pode nascer no próprio teste

`tests/conftest.py:golden` grava se `--update-golden` estiver ativo **ou se o arquivo não existir**. Uma remoção acidental pode gerar o baseline e passar, reduzindo o sinal de regressão.

## Verificação configurada e lacunas

`poe check` encadeia import-linter, Ruff lint/format, mypy e pytest. CI roda matriz Ubuntu/macOS × Python 3.13/3.14 com uv --locked. Testes cobrem schema, IDs, referências, docs, jornadas, relações, saída JSON, filesystem, sintaxe YAML, exportação, sincronismo de fixture e desempenho de 500 itens em menos de 3 segundos. Esse limite é asserção escrita, não medição desta análise.

Não foi encontrada configuração de cobertura percentual no pyproject lido. Não há resultado atual de testes, cobertura, desempenho ou type checking neste relatório. Busca estática em src/tests não retornou TODO/FIXME/HACK; retornou um `type: ignore[no-untyped-def]` em fixture. Não se investigaram versões remotas ou vulnerabilidades.

## Próximos passos sugeridos

Priorizar alinhar contrato/exportação/testes de schema; definir comportamento de nível 2; adicionar testes de Get e política para catálogos inválidos; avaliar contenção de caminhos. São oportunidades, não mudanças executadas.

## Fontes

`sinter/src/sinter/`, `sinter/tests/{contract/test_schemas,conftest,test_perf}.py`, listagem/testes de validação, `sinter/pyproject.toml` e CI. Cobertura em [registro](reverse-engineering-timestamp.md).

