# Resumo da implementação — U13 / História 3.7

## Entrega

- Implementado `sinter fmt [arquivo] [--check]`, para formatar um manifesto ou todos os manifestos elegíveis do catálogo; o comando informa a quantidade de arquivos alterados e não cria commit.
- O `RuamelCodec` serializa em round-trip, preserva comentários e quotes, organiza envelope e campos pela ordem dos modelos Pydantic e usa LF, recuo canônico e newline final.
- A leitura preserva newlines originais para o modo de comparação detectar CRLF nos bytes do arquivo; a escrita canônica emite LF.
- A aplicação compara os documentos YAML antes e depois da serialização e recusa a gravação se qualquer valor mudar. A porta `CatalogWriter` fica separada da porta genérica de leitura e é injetada somente no caso de uso `Fmt` neste incremento.
- `--check` não grava bytes, lista manifestos fora do padrão e retorna código 1 quando encontra diferenças.
- `validate` adiciona `FILE_NOT_FORMATTED` como aviso, mantendo código de saída 0 quando o catálogo é válido.
- Acrescentado `ManifestCodec.format` como contrato canônico de serialização para o futuro `apply`.

## Arquivos alterados

Os caminhos de código e teste alterados estão enumerados em `source-manifest.json`.

## Verificações executadas

- `uv run --directory sinter pytest tests/application/test_fmt.py tests/cli/test_fmt_cli.py tests/adapters/test_yaml_fs.py tests/test_fmt_fixture.py` — 26 passed.
- `uv run --project sinter --directory sinter poe check` — três contratos de importação, Ruff, formatação, mypy (88 fontes) e suíte completa: 153 passed.
- Os testes sobre a fixture cobrem idempotência, preservação dos dados YAML, formatação em lote e ausência de escrita no modo `--check`.

## Pendência de integração entre histórias

O `apply` da História 3.3 ainda não existe neste ponto da execução; portanto, a integração exigida pelo critério de aceite de aplicar rascunhos formatados e ignorar diffs apenas de layout no dry-run continua aberta. U9 depende de U13 e deve chamar `ManifestCodec.format`; seus testes precisam comprovar esse critério antes de considerá-lo fechado. A caixa correspondente no plano permanece desmarcada até essa integração ser implementada e verificada.

## Decisões e desvios

- A ordem dos campos vem dos modelos já existentes, sem duplicar uma tabela de esquema no formatador.
- Dados desconhecidos são preservados depois do envelope/campos conhecidos para evitar perda de conteúdo em manifestos inválidos ou com extensões.
- Não foi criada lógica de commit; formatar continua sendo uma alteração manual como define a história.
- A suíte completa foi executada nesta unidade; a integração futura com U9 segue pendente e está explicitamente marcada no plano.
