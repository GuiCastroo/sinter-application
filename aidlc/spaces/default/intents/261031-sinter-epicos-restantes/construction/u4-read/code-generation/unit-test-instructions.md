# Instruções de teste — U4 / História 2.4

## Estratégia

Test-after, Standard, escopo bugfix. Executar testes do serviço Markdown, aplicação e CLI, e manter a suíte existente verde. O teste dirigido precisa cobrir tanto a extração interna como o caminho da CLI sobre documentos cadastrados.

## Comando direcionado

Executar da raiz do workspace:

```bash
uv run --directory sinter pytest tests/domain/test_markdown.py tests/application/test_read.py tests/cli/test_read_cli.py
```

## Comando de verificação completa

Executar da raiz do workspace:

```bash
uv run --project sinter --directory sinter poe check
```

## Cenários obrigatórios

- Extração pela âncora GitHub sem acento, com acentos, pontuação e headings duplicados.
- O corte para em heading de nível igual/superior, mantendo headings de nível inferior dentro da seção.
- Sem âncora, retorna somente âncoras e tamanhos; âncora inexistente informa as disponíveis e sai com código 1.
- Resolução por ID, caminho cadastrado e caminho canônico, incluindo rejeição de traversal/path fora de `docs/` e não Markdown.
- Documento URL-only retorna URL e aviso, sem tentar acesso remoto.
