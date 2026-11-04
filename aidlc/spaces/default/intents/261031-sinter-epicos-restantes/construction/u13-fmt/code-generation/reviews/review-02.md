## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Iteration:** 2
**Verdict Dictated:** no
**Date:** 2026-11-03T18:27:42Z

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Major | sinter/src/sinter/adapters/outbound/yaml_fs/files.py > FsCatalogFiles.read; sinter/src/sinter/application/fmt.py > comparação source/formatted | A leitura por Path.read_text usa tradução universal de newlines. Um arquivo que já tem ordem/recuo canônicos, mas usa CRLF, chega ao formatador como LF e é comparado como inalterado: fmt --check não o acusa e fmt não o regrava. Portanto a garantia de LF nos bytes não é cumprida, apesar do teste do codec com uma string CRLF passar. A reprodução do mesmo modo de leitura sobre bytes CRLF resultou em actual_bytes_have_CRLF=True, Fs_read_default_normalizes=True, Fmt_detects_change=False. | Ler o texto sem tradução de newlines ou fornecer ao caso de uso fatos que preservem a distinção dos bytes; acrescentar regressão com arquivo real em CRLF, exigindo check=1 sem escrita e fmt convertendo os bytes para LF, com segunda execução idempotente. | Resolved (reviewer) |
| R-02 | Major | sinter/src/sinter/application/fmt.py > Fmt.__call__ antes de write_all | A aplicação grava o resultado de codec.format sem verificar que os dados YAML antes/depois são iguais. A restrição de segurança de AD-36 exige essa comparação, além do round-trip. Uma reprodução usando a porta em memória e um codec que altera schemaVersion de 1 para 2 terminou sem erros e gravou a alteração de negócio. Os testes de igualdade sobre a fixture comprovam o codec nesses exemplos, mas não estabelecem a proteção obrigatória no ponto de escrita. | Comparar os documentos parseados antes/depois antes de incluir cada destino no lote; recusar escrita quando houver diferença semântica e registrar diagnóstico. Acrescentar teste de aplicação com codec que altera dados, verificando erro e nenhum destino gravado. Preservar a igualdade dos valores de escalares em bloco. | Resolved (reviewer) |
| R-03 | Major | sinter/src/sinter/ports/outbound/catalog_files.py > CatalogFiles.write_all; sinter/src/sinter/application/fmt.py > porta de escrita | write_all foi incluído na porta genérica CatalogFiles, que também é recebida pelos leitores do catálogo. Isso elimina a separação explícita de leitura e escrita prevista por AD-34: a operação deveria estar no módulo catalog_writer e ser importada apenas por apply, catalog_init e fmt. O próprio cabeçalho de catalog_files ainda afirma que a escrita fica separada. As três regras atuais de importação passam, mas não verificam essa restrição e não impedem novos leitores de escrever pelo mesmo contrato. | Separar a capacidade de escrita em ports/outbound/catalog_writer.py, injetá-la somente nos casos de uso autorizados e compô-la em bootstrap. Acrescentar a verificação de arquitetura que impeça os demais consumidores de importar a operação de escrita, sem duplicar a implementação do adaptador. | Resolved (reviewer) |
| R-04 | Minor | sinter/src/sinter/adapters/outbound/yaml_fs/codec.py > RuamelCodec.format | A serialização preserva espaços no fim de linhas de comentário. O manifesto válido com `apiVersion: sinter.dev/v1   # envelope   ` sai com os mesmos espaços finais e passa a ser considerado canônico. A normalização de espaços finais prevista na Story 3.7 não está completa. | Remover whitespace final fora de valores de escalares em bloco, preservando seu conteúdo semântico; acrescentar teste de comentário inline e teste de escalar literal com espaços significativos. | Resolved (reviewer) |
| R-05 | Major | sinter/src/sinter/application/fmt.py > construção de summary e files_changed depois da condição de escrita | Quando um manifesto tem erro e outro precisaria formatar, a nova condição not findings impede corretamente qualquer escrita, mas o resultado ainda usa o lote planejado como se tivesse sido gravado. Reprodução com broken.yaml inválido e organization.yaml válido fora de ordem devolveu YAML_SYNTAX_ERROR, files_changed=['organization.yaml'] e summary='1 manifesto(s) formatado(s).', enquanto organization.yaml permaneceu byte a byte igual. A CLI e consumidores JSON recebem uma confirmação falsa de alteração. | Separar alterações propostas das efetivamente persistidas; se o lote foi recusado, files_changed deve estar vazio e summary deve informar zero gravados e a interrupção. Acrescentar regressão de lote misto, conferindo relatório, mensagem, lista e ausência de alteração nos dois destinos. | New |

> R-01 Reviewer note: FsCatalogFiles.read abre com newline vazio, preservando CRLF no texto comparado. O teste real test_fmt_detecta_crlf_no_check_e_grava_lf confirma check com saída 1 sem mudar bytes, gravação em LF e check posterior com saída 0.

> R-02 Reviewer note: Fmt compara os documentos parseados antes/depois e gera FMT_SEMANTIC_CHANGE sem gravar o lote. test_fmt_recusa_codec_que_altera_dados_sem_escrever passou com codec que muda schemaVersion.

> R-03 Reviewer note: CatalogFiles voltou a ser somente leitura; CatalogWriter está em módulo próprio. Fmt recebe a capacidade separada e bootstrap compõe FsCatalogWriter. A regressão AST em tests/application/test_fmt.py verifica os consumidores autorizados da porta e passou na suíte direcionada.

> R-04 Reviewer note: O codec remove whitespace de CommentToken, mantendo os escalares fora dessa transformação. Teste e reprodução independente confirmaram comentário inline sem espaços finais e valor do escalar literal preservado, inclusive espaços significativos.

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| uv run --directory sinter pytest tests/application/test_fmt.py tests/cli/test_fmt_cli.py tests/adapters/test_yaml_fs.py tests/test_fmt_fixture.py | 25 passed in 1.97s; exit 0 | Executado exatamente como solicitado; inclui regressões para os quatro achados anteriores. |
| uv run --project sinter --directory sinter poe check | 3 contratos kept; Ruff passa; 144 arquivos formatados; mypy sem erros em 88 fontes; 152 passed in 6.14s; exit 0 | Verificação completa executada; o aviso uv sobre project sinter relativo a directory sinter permanece, sem impedir a execução correta. |
| Reprodução independente de comentário e escalar literal | inline_comment_trailing_removed=True; idempotent=True; block_scalar_value_preserved=True; block_trailing_spaces_preserved=True | Confirma que a correção não sacrifica valores literais para limpar comentários. |
| Reprodução de lote com arquivo inválido | errors=['YAML_SYNTAX_ERROR']; reported_changed=['organization.yaml']; summary='1 manifesto(s) formatado(s).'; file_unchanged=True | Confirma o novo achado de comunicação incorreta do resultado, sem escrita em disco na reprodução. |

### Acceptance and Integration

O formatador deriva a ordem dos modelos, mantém o envelope, comentários e dados dos exemplos, emite recuo de dois espaços e LF com newline final e é idempotente na fixture. O check permanece sem escrita e informa os caminhos não canônicos. O validate mantém o diagnóstico de layout como aviso. Não há caminho de commit no caso de uso.

Aplicar o rascunho formatado e ignorar diferença apenas de layout no dry-run ainda não foi testado: apply não existe neste ponto e o resumo registra essa integração como pendente para U9. O contrato format está disponível; a história inteira só pode ter esse critério encerrado com a evidência integrada futura.

### Summary

Os quatro achados anteriores foram corrigidos e as verificações passaram. Há um novo achado Major localizado na mensagem/lista de resultados quando um lote é recusado; não há achado Critical nem mais de dois Major abertos, portanto a avaliação arquitetural é READY com a correção indicada e com a integração U9 ainda pendente.
