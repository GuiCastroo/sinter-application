# Instruções de teste — U13 / História 3.7

## Estratégia

Test-after, estratégia Standard, escopo bugfix. Manter a suíte existente verde e acrescentar regressão dirigida para formatação canônica. Cobrir comportamento da serialização, aplicação, CLI e fixture completa. Não alterar limiares de qualidade nem ignorar diferenças que mudem dados.

## Comando direcionado

Executar da raiz do workspace:

```bash
uv run --directory sinter pytest tests/application/test_fmt.py tests/cli/test_fmt_cli.py tests/adapters/test_yaml_fs.py tests/test_fmt_fixture.py
```

## Comando de verificação completa

Executar da raiz do workspace:

```bash
uv run --project sinter --directory sinter poe check
```

## Cenários obrigatórios

- Chaves fora de ordem, recuo irregular, espaços finais, LF e newline final.
- Comentários de topo, de chave e de item continuam associados ao conteúdo correto após reorder.
- Dados parseados antes e depois são iguais; formato canônico é idempotente.
- `--check` enumera arquivos não canônicos, retorna 1 e deixa bytes/mtime intactos.
- Sem argumento, percorre os manifestos elegíveis do catálogo, informa a quantidade alterada e não cria commit.
- `apply` não anuncia diff quando a única diferença é layout; saída persistida é canônica.
- `validate` reporta aviso de layout sem falhar validação válida.
- Arquivo inválido, caminho ausente e erro de escrita são comunicados sem sucesso silencioso.
