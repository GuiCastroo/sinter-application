# Interfaces e contratos

## Interface pública de linha de comando

| Comando | Entradas | Resultado | Efeito |
|---|---|---|---|
| `sinter validate [PASTA]` | `--catalog PATH`, `--json` | ValidateResult: report, filesChecked, summary | Lê catálogo; não modifica manifestos |
| `sinter get ID` | `--level 0/1/2` (padrão 1), `--catalog PATH`, `--json` | GetResult: level, item, omitted, summary | Lê catálogo |
| `sinter schema export [PASTA]` | Destino padrão schemas; `--json` | SchemaExportResult: files, changed, summary | Cria diretórios e grava schemas alterados |

`--debug` é removido em `app.run` antes da chamada Typer e permite traceback de erro inesperado. Busca de catálogo: caminho explícito (no validate, argumento precede opção) → `SINTER_CATALOG` → diretório atual e ancestrais com `organization.yaml`.

Não foram observados endpoints REST, GraphQL, gRPC, MCP ou consumers de eventos no pacote. Não se atribuem autenticação, rate limiting ou status HTTP a uma CLI local.

## JSON e falhas

Modelos serializam nomes camelCase, null explícito e indentação de 2 espaços. Um finding tem `code`, `severity`, `file`, `path`, `message`, `line`, `source`, `related`. Relatório separa errors e warnings, ordenados por arquivo, linha, caminho, código e mensagem.

Erros operacionais produzem `{"error":{"code":"…","message":"…","details":{}}}`. Saídas: 0 para sucesso ou apenas avisos, 1 para erro de validação/recurso, 2 para uso/ambiente inválido, 3 para erro interno. Código estável é o contrato; texto explica a falha.

## Formato do catálogo

Envelope `apiVersion: sinter.dev/v1`, `kind`, `metadata`, `spec`. Kinds registrados: Organization, RepositoryList, Domain, Subdomain, Journey, Relation, Regulation, Standard. Organização suporta schemaVersion até 1; versão maior é recusada. Campos desconhecidos são rejeitados. Campos calculados escritos em spec produzem `CALC_FIELD_WRITTEN`.

IDs e caminhos canônicos são centralizados em `domain/model/registry.py`. Application, Rule, Data, Doc e Decision são itens internos de manifestos com identidade própria; Area é agrupador. Relation implementa apenas `modernized_by` entre aplicações. Jornada permite ciclos nos links de passos.

## Portas internas

| Porta | Operações e semântica |
|---|---|
| CatalogFiles | `list_manifests() -> list[str]` ordenada; `read(path) -> str`; `exists(path) -> bool` |
| ManifestCodec | `split(text) -> list[ManifestText]`, com dados comuns e mapa de linhas; levanta ManifestSyntaxError |
| LocalFiles | `read(path) -> str ou None`; `write(path,text)` para arquivos fora do catálogo |
| Validate | `ValidateRequest → ValidateResult` |
| Get | `GetRequest(id,level) → GetResult` |
| SchemaExport | `SchemaExportRequest(target) → SchemaExportResult` |

## Limitações confirmadas por leitura

`get` aceita nível 2, mas `application/get.py` calcula `min(request.level,1)` para visões detalhadas. `levels.omitted` sugere novamente nível 2 sem implementação correspondente. Carregamento de `Get` descarta findings, e duplicatas são resolvidas pelo primeiro manifesto válido em ordem de arquivo; consultar não equivale a validar.

`published_results()` inclui get-result; a listagem de `sinter/schemas/` ainda contém 11 arquivos, sem get-result.schema.json. A geração esperada agora inclui 12: oito kinds e quatro resultados. Ver [qualidade](code-quality-assessment.md).

## Fontes

`adapters/inbound/cli/{app,catalog_root,errors}.py`, `commands/`, `render/json.py`, `ports/`, `domain/model/{base,registry}.py`, `domain/errors.py`, `application/get.py`, `ports/inbound/schema_export.py` (todos sob `sinter/src/sinter/`).

