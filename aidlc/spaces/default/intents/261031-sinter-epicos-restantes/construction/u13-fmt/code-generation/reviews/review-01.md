## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Iteration:** 1
**Verdict Dictated:** no
**Date:** 2026-11-03T18:21:19Z

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Major | sinter/src/sinter/adapters/outbound/yaml_fs/files.py > FsCatalogFiles.read; sinter/src/sinter/application/fmt.py > comparação source/formatted | A leitura por Path.read_text usa tradução universal de newlines. Um arquivo que já tem ordem/recuo canônicos, mas usa CRLF, chega ao formatador como LF e é comparado como inalterado: fmt --check não o acusa e fmt não o regrava. Portanto a garantia de LF nos bytes não é cumprida, apesar do teste do codec com uma string CRLF passar. A reprodução do mesmo modo de leitura sobre bytes CRLF resultou em actual_bytes_have_CRLF=True, Fs_read_default_normalizes=True, Fmt_detects_change=False. | Ler o texto sem tradução de newlines ou fornecer ao caso de uso fatos que preservem a distinção dos bytes; acrescentar regressão com arquivo real em CRLF, exigindo check=1 sem escrita e fmt convertendo os bytes para LF, com segunda execução idempotente. | New |
| R-02 | Major | sinter/src/sinter/application/fmt.py > Fmt.__call__ antes de write_all | A aplicação grava o resultado de codec.format sem verificar que os dados YAML antes/depois são iguais. A restrição de segurança de AD-36 exige essa comparação, além do round-trip. Uma reprodução usando a porta em memória e um codec que altera schemaVersion de 1 para 2 terminou sem erros e gravou a alteração de negócio. Os testes de igualdade sobre a fixture comprovam o codec nesses exemplos, mas não estabelecem a proteção obrigatória no ponto de escrita. | Comparar os documentos parseados antes/depois antes de incluir cada destino no lote; recusar escrita quando houver diferença semântica e registrar diagnóstico. Acrescentar teste de aplicação com codec que altera dados, verificando erro e nenhum destino gravado. Preservar a igualdade dos valores de escalares em bloco. | New |
| R-03 | Major | sinter/src/sinter/ports/outbound/catalog_files.py > CatalogFiles.write_all; sinter/src/sinter/application/fmt.py > porta de escrita | write_all foi incluído na porta genérica CatalogFiles, que também é recebida pelos leitores do catálogo. Isso elimina a separação explícita de leitura e escrita prevista por AD-34: a operação deveria estar no módulo catalog_writer e ser importada apenas por apply, catalog_init e fmt. O próprio cabeçalho de catalog_files ainda afirma que a escrita fica separada. As três regras atuais de importação passam, mas não verificam essa restrição e não impedem novos leitores de escrever pelo mesmo contrato. | Separar a capacidade de escrita em ports/outbound/catalog_writer.py, injetá-la somente nos casos de uso autorizados e compô-la em bootstrap. Acrescentar a verificação de arquitetura que impeça os demais consumidores de importar a operação de escrita, sem duplicar a implementação do adaptador. | New |
| R-04 | Minor | sinter/src/sinter/adapters/outbound/yaml_fs/codec.py > RuamelCodec.format | A serialização preserva espaços no fim de linhas de comentário. O manifesto válido com `apiVersion: sinter.dev/v1   # envelope   ` sai com os mesmos espaços finais e passa a ser considerado canônico. A normalização de espaços finais prevista na Story 3.7 não está completa. | Remover whitespace final fora de valores de escalares em bloco, preservando seu conteúdo semântico; acrescentar teste de comentário inline e teste de escalar literal com espaços significativos. | New |

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| uv run --directory sinter pytest tests/application/test_fmt.py tests/cli/test_fmt_cli.py tests/adapters/test_yaml_fs.py tests/test_fmt_fixture.py | 20 passed in 1.73s; exit 0 | A suíte cobre a fixture e os caminhos principais; não cobre CRLF no adaptador real nem a recusa de mudanças semânticas antes da escrita. |
| uv run --project sinter --directory sinter poe check | 3 contratos kept; Ruff passa; 143 arquivos formatados; mypy sem erros em 87 fontes; 147 passed in 5.63s; exit 0 | Verificação completa executada. O uv avisa sobre project sinter relativo ao directory sinter, mas executa a configuração do projeto e termina com sucesso. |
| Reprodução em memória de normalização e whitespace | CRLF nos bytes é invisível após leitura universal; Fmt_detects_change=False; a primeira linha de comentário permanece com espaços finais | Confirma duas lacunas da normalização, sem alterar arquivos do catálogo. |
| Reprodução de proteção semântica pela porta | format_succeeded=True, business_data_changed=True, changed=['organization.yaml'] após codec alterar schemaVersion | Confirma que a aplicação não impede alterações de dados produzidas por um formatador incorreto. A reprodução foi somente em memória. |

### Acceptance and Integration

A organização dos campos segue os modelos do registro; o envelope é canônico inclusive para manifesto inválido, a ordenação mantém metadados de comentário do ruamel e os testes da fixture verificam idempotência e igualdade dos dados. O check lista caminhos e devolve erro sem chamar write_all. O caminho sem argumento enumera os manifestos e informa a quantidade; não contém porta de Git nem chamada de commit. O validate reporta FILE_NOT_FORMATTED como warning e os testes confirmam código 0 em catálogo válido. Os três achados Major acima impedem considerar a formatação segura e totalmente canônica.

O critério de integração com apply permanece explicitamente pendente: apply ainda não existe, como registra o resumo da própria unidade. ManifestCodec.format fornece o ponto de integração, mas U9 ainda precisa provar gravação canônica e ausência de diff apenas por layout no dry-run. Isso não foi contado como novo defeito da implementação de apply, que está fora deste passe; tampouco foi tratado como critério já executado. A linha FR18 marcada OK na rastreabilidade cobre os testes atuais de formato, não essa evidência futura.

### Summary

As verificações atuais passam e o núcleo do formatador está implementado, mas há três achados Major: newlines dos arquivos reais, ausência da proteção semântica antes de escrever e capacidade de escrita exposta aos leitores. Corrigir esses pontos e seus testes antes de encerrar U13; manter o critério de integração com U9 rastreado até uma execução real.
