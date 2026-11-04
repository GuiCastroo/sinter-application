# Resumo da implementação — U4 / História 2.4

## Entrega

- Implementado `sinter read <doc>[#anchor]` com busca por id de documento ou path cadastrado/canônico.
- O serviço Markdown gera anchors no estilo GitHub sem acentos, distingue headings duplicados com sufixos e extrai a seção até o próximo heading do mesmo nível ou superior.
- Anchors duplicados são globalmente únicos; headings dentro de fences não entram no índice e os fechamentos respeitam caractere e tamanho do marcador.
- Sem anchor, a saída contém somente títulos, anchors e tamanho de seção em linhas; não expõe o corpo completo.
- Path local deve ser Markdown sob `docs/`; traversal, paths fora de docs, symlinks e outras extensões são recusados pelo leitor do adaptador com contenção física.
- Documentos só com URL retornam URL e aviso de que Sinter não acessa conteúdo externo.

## Arquivos alterados

Os caminhos de código e teste estão enumerados em `source-manifest.json`.

## Verificações executadas

- `uv run --directory sinter pytest tests/domain/test_markdown.py tests/application/test_read.py tests/cli/test_read_cli.py` — 30 passed.
- `uv run --project sinter --directory sinter poe check` — três contratos de arquitetura, Ruff, formatação, mypy (94 fontes) e suíte completa: 183 passed.
- A opção `--json` produz o contrato estruturado de leitura e os caminhos de erro usam `ANCHOR_NOT_FOUND`/`ITEM_NOT_FOUND` existentes.

## Decisões e desvios

- O tamanho da seção é reportado em linhas, uma métrica compacta para o índice e sem abrir o conteúdo inteiro ao agente consumidor.
- A leitura usa `CatalogFiles` e nunca chama rede nem `LocalFiles`; documentos externos apenas exibem o URL.
- Nenhuma integração de escrita ou commit foi introduzida.
- Nenhuma verificação planejada ficou sem execução.
