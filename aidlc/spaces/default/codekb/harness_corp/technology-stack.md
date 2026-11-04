# Tecnologias

## Runtime e dependências diretas

| Tecnologia | Declaração | Versão no lock lida | Uso observado |
|---|---|---|---|
| Python | >=3.13 | CI: 3.13 e 3.14 | Pacote e scripts |
| Sinter | 0.1.0 | 0.1.0 | CLI local |
| Pydantic | >=2.14,<3 | 2.14.1 | Validação, DTOs, schemas |
| Typer | >=0.27,<0.28 | 0.27.3 | Comandos CLI |
| ruamel.yaml | >=0.19,<0.20 | 0.19.1 | Decodificação YAML com posições |
| hatchling | >=1.32 no build-system | Não fixada em uv.lock observado | Construção wheel |

Valores são declarações do checkout, não consulta a versões atuais nem prova de instalação.

## Desenvolvimento

| Ferramenta | Lock | Função |
|---|---|---|
| pytest | 9.1.1 | Testes funcionais/contratos/performance |
| Ruff | 0.17.1 | Lint e formato; alvo py313; linha 100 |
| mypy | 2.4.0 | strict no src, plugin Pydantic |
| import-linter | 2.15 | Restrições de camadas e bibliotecas de borda |
| poethepoet | 0.49.0 | Tarefas de qualidade |
| uv | Sem versão fixada na CI | Resolução/instalação com lock |

CI usa GitHub Actions `actions/checkout@v4` e `astral-sh/setup-uv@v6`; matriz Ubuntu/macOS e duas versões Python. Não há imagem de container ou infraestrutura de aplicação observada na superfície principal.

## Formatos e ferramentas auxiliares

YAML é fonte do catálogo; Markdown contém narrativa; JSON Schema deriva dos modelos. Python padrão suporta filesystem, dataclasses, typing e CLI auxiliar. A ferramenta de documentação separada gera HTML/CSS/JavaScript e referencia marked 15 e Mermaid 11 por CDN (faixas major, sem patch fixado no trecho lido). BMAD é apoio instalado em arquivos locais, fora do runtime Sinter. `scripts/with-aidlc.sh` usa shell POSIX.

## Fontes

`sinter/pyproject.toml`, pares name/version em `sinter/uv.lock`, CI, imports dos fontes e trecho inicial de `gerar_site.py`. Sem auditoria de vulnerabilidades, acesso de rede ou execução de programas.

