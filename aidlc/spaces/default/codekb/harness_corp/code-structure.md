# Estrutura do código

## Pacote principal

Raiz de projeto Python: `sinter/`. Pacote distribuído: `src/sinter`, versão declarada 0.1.0. Entrada: `sinter.adapters.inbound.cli.app:main`.

| Caminho relativo ao repositório | Papel |
|---|---|
| `sinter/src/sinter/bootstrap.py` | Composição e versão instalada |
| `sinter/src/sinter/adapters/inbound/cli/` | CLI, resolução de catálogo, erros e apresentação |
| `sinter/src/sinter/application/` | load, validate, get, schema_export |
| `sinter/src/sinter/ports/inbound/` | Requests, Results, Report e envelope de erro |
| `sinter/src/sinter/ports/outbound/` | Protocolos CatalogFiles, ManifestCodec e LocalFiles |
| `sinter/src/sinter/domain/model/` | Modelos YAML, registro de kinds, catálogo e visões |
| `sinter/src/sinter/domain/services/` | Níveis, herança, referências, schemas, resumos, texto e tokens |
| `sinter/src/sinter/domain/validation/` | Parse, finding, motor e 11 módulos de regras |
| `sinter/src/sinter/domain/errors.py` | Tabela de erros de operação e códigos de saída |
| `sinter/src/sinter/domain/drafts/` | Namespace sem implementação substantiva observada |
| `sinter/src/sinter/adapters/outbound/git/` | Namespace sem integração Git implementada observada |
| `sinter/tests/` | Testes por camada, contratos, CLI, fixture e desempenho |
| `sinter/schemas/` | Schemas JSON versionados; conteúdo derivado |
| `sinter/skills/` | Pasta sem arquivos na listagem |

## Padrões

Módulos e funções snake_case; classes PascalCase; modelos Pydantic com aliases camelCase, extra proibido e frozen. Protocolos usam `typing.Protocol`; catálogo e fatos usam dataclasses frozen. `Report.from_findings` ordena erros/avisos; `Finding` preserva arquivo, linha, caminho e referências relacionadas. Regras são funções geradoras registradas por decorador `@rule`.

A organização por camada é verificada por import-linter; não há importação de Typer, Click ou ruamel em domínio/aplicação/portas. O domínio usa Pydantic por decisão estrutural observável.

## Demais materiais do repositório

`docs/prd-dominio-2026-10-17/` contém PRD, epics e exemplo; `prd-yaml.md` é proposta mais ampla; `_bmad-output/` guarda planejamento e avaliações. `_bmad/` e skills BMAD são ferramentas de apoio, não módulos importados pelo Sinter. `.agents/skills/sinter-documentar/` contém geradores independentes de documentação, cartão para IA e site. `scripts/with-aidlc.sh` é conveniência local de abertura das ferramentas.

Esses materiais auxiliares foram vistos superficialmente; não se afirma cobertura profunda de todo o repositório. A instalação AI-DLC e caches foram excluídos. A cobertura exata está em [registro da análise](reverse-engineering-timestamp.md).

## Fontes

Leitura de `sinter/src/sinter/`, manifestos e CI; listagens de testes, schemas, skills e planejamento. Inventário funcional em [componentes](component-inventory.md).

