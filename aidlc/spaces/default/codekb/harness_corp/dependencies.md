# Dependências

## Grafo interno principal

```text
CLI -> bootstrap
CLI -> ports.inbound, domain.errors
bootstrap -> application, adapters.outbound
application -> ports.outbound, ports.inbound, domain
adapters.outbound -> ports.outbound, domain.validation.finding
ports -> domain
domain.model.catalog -> model.registry, validation.finding
domain.validation -> model, services
domain.services -> model
```

Não há dependência observada do pacote Sinter para BMAD, AI-DLC ou os scripts de documentação auxiliares.

## Adjacência dos fluxos centrais

| Módulo (sob src/sinter) | Dependências internas diretas relevantes |
|---|---|
| application/load | model.catalog, model.registry, services.references, validation.engine/finding/schema, ports.outbound |
| application/validate | application.load, services.summary, validation.engine, ports.inbound.validate/common |
| application/get | application.load, domain.errors, model.views, services.levels/summary, portas de leitura |
| application/schema_export | services.schemas, ports.inbound.schema_export, ports.outbound.local_files |
| services/levels | model.catalog/domain/journey/organization/subdomain/views, services.inheritance |
| services/inheritance | model.blocks/catalog/domain/subdomain/views, services.references |
| validation/engine | model.catalog, validation.finding, imports dinâmicos de rules |
| validation/schema | model.catalog/registry, validation.finding |
| model/registry | modelos dos oito kinds |
| adapters/outbound/yaml_fs/codec | ports.outbound.manifest_codec, validation.finding, ruamel.yaml |

A dependência catálogo → finding → model.base permanece interna ao domínio. Não foi identificado ciclo estático nesses fluxos lidos; isso não substitui executar import-linter.

## Dependências externas

Runtime: Pydantic, Typer e ruamel.yaml. Lock inclui transitivas como pydantic-core 2.50.1, Click 8.5.0, Rich 15.0.0, typing-extensions 4.16.0 e bibliotecas de terminal/Markdown. Ferramentas de desenvolvimento e versões estão em [stack](technology-stack.md).

O build usa hatchling, separado do conjunto runtime; a CI instala pelo `uv sync --locked`. Não houve resolução nova nem análise de segurança de pacotes.

## Dados e infraestrutura

Arquivos do catálogo são lidos localmente. URLs em RepositoryRef/Doc e referências a aplicações/eventos externos representam fatos catalogados; não são conexões de execução. Não há driver de banco, SDK de nuvem ou cliente HTTP nas dependências diretas do Sinter. Os geradores auxiliares de documentação usam bibliotecas padrão Python e o site gerado depende de CDN no navegador.

## Impacto de mudanças

- Novo kind: alterar modelo/registry e schema export, conferir testes contratuais e caminhos canônicos.
- Nova referência: ajustar services.references e regras específicas; preservar IDs e diagnósticos.
- Novo campo de consulta: atualizar model.views, levels/herança, GetResult/render e schemas publicados.
- Novo comando: registrar CLI, caso de uso/DTO e composição; preservar fronteiras de importação.
- Mudança no YAML: verificar fixtures e exemplo do PRD, que têm teste de igualdade.

Fontes: imports de `sinter/src/sinter/`, `pyproject.toml`, lock e testes contratuais/fixture lidos. Não foram calculados grafos de ferramentas auxiliares inteiras.

