# Inventário de componentes

Cada seção nomeia um componente lógico observado; todos pertencem ao único pacote Sinter. Ferramentas auxiliares são registradas ao fim sem supor integração de execução.

## CLI

`adapters/inbound/cli/`: Typer, comandos validate/get/schema export, resolução da raiz, erros e renderização. Depende de bootstrap, DTOs e domínio de erros. Não instancia adaptadores de saída diretamente.

## Composição

`bootstrap.py`: lê versão do pacote, monta Container, instancia FsCatalogFiles, RuamelCodec e FsLocalFiles ou recebe substitutos de teste. Validate/Get são propriedades que exigem catálogo; SchemaExport independe dele.

## Carregamento

`application/load.py`: enumera e decodifica YAML, confere organização/versão, preserva findings, cria Catalog e FileFacts. Depende das portas de leitura/codec e de schema/registry/referências.

## Validação

`application/validate.py`, `domain/validation/`: duas fases (schema e regras de catálogo), registro dinâmico por módulo e relatório ordenado. Famílias: docs, domains, glossary, ids, inheritance, journeys, paths, references, regulations, relations, subdomains. Cada código registra severidade e função pura.

## Consulta e herança

`application/get.py`, `domain/services/{levels,inheritance,references,summary,text,tokens}.py`: resolve IDs, monta nível 0/1 e origem do conhecimento/operação. `references` mapeia ligações e docs para regras e consulta. `tokens` é heurística isolada de quatro caracteres por token; não foi observado enforcement de orçamento no fluxo Get.

## Modelos do catálogo

`domain/model/`: SinterModel, blocos comuns, oito kinds, registry e visões. Catalog guarda tuplas de manifestos e entradas; consultas percorrem coleções, sem banco ou índice externo.

## Contratos e portas

`ports/inbound/`: DTOs imutáveis, Report e ErrorEnvelope.
`ports/outbound/`: CatalogFiles, ManifestCodec, LocalFiles e ManifestText. Não dependem de frameworks de CLI/YAML.

## Adaptadores de arquivos

`adapters/outbound/{yaml_fs,local_fs,memory}/`: sistema de arquivos, ruamel round-trip e memória para testes. Apenas LocalFiles escreve; CatalogFiles é leitura. `git/` é namespace vazio observado.

## Exportação de schemas

`application/schema_export.py`, `domain/services/schemas.py`: deriva JSON Schemas de KINDS e resultados publicados; grava somente diferenças usando LocalFiles. Contratos versionados vivem em `sinter/schemas/`.

## Verificação e distribuição

`sinter/pyproject.toml`, `sinter/tests/`, `.github/workflows/sinter-check.yml`: hatchling, uv, Poe, pytest, Ruff, mypy e import-linter. Testes não foram executados nesta análise.

## Ferramentas de documentação (cobertura superficial)

`.agents/skills/sinter-documentar/`: `_paginas.py` lê seis páginas Markdown; `gerar_llm.py` deriva llms.txt/resumos/grafo; `gerar_site.py` monta HTML com bibliotecas de navegador. Independente do pacote e não ligado aos casos de uso. BMAD e seu material de configuração/skills foram apenas reconhecidos como apoio. Ver limitações de cobertura no [registro](reverse-engineering-timestamp.md).

