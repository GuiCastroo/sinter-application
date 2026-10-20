# Addendum — Catálogo, passo 1 (Domínio)

Detalhes técnicos que não cabem no PRD. O **formato dos arquivos** está no [Apêndice A do PRD](prd.md#apêndice-a--esqueleto-dos-arquivos) (fonte única); a referência executável é o [exemplo-catalogo/](exemplo-catalogo/README.md). As decisões de arquitetura estão na [espinha](../../_bmad-output/planning-artifacts/architecture/architecture-harness_corp-2026-09-26/ARCHITECTURE-SPINE.md) (AD-1 a AD-24).

## Stack

- **Back-end em Python** (núcleo + CLI): Pydantic 2.14 para os schemas, Typer 0.27 para a CLI, ruamel.yaml 0.19 para ler e gravar YAML preservando comentários, pytest 9, projeto gerido por uv 0.13 com build hatchling. Instalação para o usuário: `uv tool install sinter`.
- **Front em TypeScript** (só na fatia 2). Front e back conversam por **JSON Schema** gerado dos modelos Pydantic (`schemas/*.json`); o front gera seus tipos a partir dele (AD-12).

## Ordem de construção

1. **Núcleo:** schemas (o Apêndice A em Pydantic) → carregar o catálogo → validação → herança e calculados.
2. **CLI:** os comandos abaixo, todos chamando o núcleo.
3. **Skills:** `sinter-find` e `sinter-domain`, por cima da CLI (FR-24).

## Formato das skills

- Padrão aberto **[Agent Skills](https://agentskills.io/specification)**, para funcionar em Claude Code e em outros agentes que seguem o padrão:
  ```text
  skills/
    sinter-find/
      SKILL.md            # name: sinter-find · description: o que faz + quando usar
      references/         # saída do get --json explicada, níveis 0/1/2
    sinter-domain/
      SKILL.md            # name: sinter-domain
      references/         # obrigatórios por kind, fluxo buscar → rascunho → dry-run → apply
      assets/             # modelos de rascunho (domain, subdomain, journey)
  ```
- `SKILL.md` < 500 linhas; o resto em `references/` e `assets/`, um nível só (divulgação progressiva, como o próprio catálogo).
- `compatibility: Requer a CLI sinter (uv tool install sinter)`; a skill só chama a CLI com `--json`, nunca grava YAML direto no catálogo.
- Validação de formato com `skills-ref validate skills/<nome>`.
- **Criadas com a skill-creator da Anthropic** (instalar o plugin antes do Épico 4): ela gera a pasta, roda **evals** (pedidos de teste contra o `exemplo-catalogo`, ex.: "onde fica a boleta?", "cadastra o domínio Câmbio" → tem de achar o existente) e ajusta a `description` para a skill disparar nos pedidos certos e não nos errados.

## Comandos da CLI nesta história

| Comando | O que faz | FR |
|---|---|---|
| `sinter catalog init [pasta]` | Cria a estrutura do catálogo e o `organization.yaml` | FR-1 |
| `sinter new <domain\|subdomain\|journey> [--flags]` | Gera um rascunho a partir do esqueleto, com os obrigatórios marcados; com flags, já preenche | FR-3, FR-7, FR-11, FR-18 |
| `sinter find <texto>` | Busca no catálogo por nome, id-domínio, apelidos, termos do glossário, propósito e repo; devolve ids ordenados | novo |
| `sinter list domains [--area]` | Lista domínios (id-domínio, nome, área, propósito) | novo |
| `sinter get <id> --raw` | Devolve o YAML atual como rascunho de edição (editar = `get --raw` → muda → `apply`) | novo |
| `sinter apply <arquivo\|-> [--dry-run]` | **Caminho único de escrita.** Valida, mostra o resumo em linguagem natural e, sem `--dry-run`, grava no lugar canônico e faz um commit | FR-17, FR-18 |
| `sinter validate [pasta] [--ci]` | Valida o catálogo inteiro (schema, ids, referências, ciclos, camadas) | FR-17 |
| `sinter get <id> --level 0\|1\|2` | Navega com herança e campos calculados | FR-13, FR-15 |
| `sinter read <doc>[#âncora]` | Lê só uma seção de um `.md` | FR-16 |

Todos aceitam `--json` (saída no formato de `schemas/`, chaves camelCase) e terminam com código `0` (ok), `1` (erro de validação ou item não encontrado), `2` (uso errado ou ambiente) ou `3` (erro interno). Mais `sinter fmt [--check]`, `sinter list areas`, `sinter schema export` e `sinter skills install` (ver épicos).

### Os três jeitos de criar, um caminho só

```text
Terminal:      sinter new subdomain → edita o arquivo → sinter apply arquivo.yaml
Edição manual: edita um YAML do catálogo         → sinter apply arquivo.yaml
Skill (IA):    conversa / lê fontes → rascunho    → sinter apply - --dry-run → confirma → sinter apply -
```

### O que acontece num `sinter apply`

1. Lê o(s) manifesto(s) do arquivo ou da entrada padrão.
2. Valida cada um contra o schema do seu `kind` (Pydantic).
3. Carrega o catálogo atual e valida referências, unicidade, hierarquia e camadas de dados.
4. Calcula a diferença (cria / altera / sem mudança) e monta o resumo em linguagem natural.
5. Com `--dry-run`, para aqui e devolve o resumo e os erros.
6. Sem `--dry-run`: grava cada manifesto em `domains/<d>/<pasta do kind>/<id>.yaml`, preservando comentários, e faz **um** commit com os trailers `Sinter-*`.
7. Responde em texto ou `--json`, com o código de saída.

## Estrutura do projeto

Definida na **espinha de código** ([architecture-sinter-codigo-2026-10-20](../../_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md), AD-25 a AD-48), que vence este addendum: hexagonal com `domain/`, `application/`, `ports/{inbound,outbound}`, `adapters/{inbound/cli, outbound/…}` e `bootstrap.py`. Para acrescentar comando, regra, campo ou kind, siga o [guia de extensão](../../_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/GUIA-EXTENSAO.md).

## Notas de formato

- Chaves em inglês, valores no idioma da empresa (questão aberta 4 do PRD).
- `metadata.domainId` guarda o id-domínio; `metadata.area` aponta para `organization.yaml → areas`.
- Aplicações, dados e docs são listas embutidas, não arquivos; ainda assim, aplicações e dados têm id único no catálogo, para jornadas e relações poderem citá-los.
- Campos `(calc)` do Apêndice A nunca são gravados; se aparecerem num arquivo, o `validate` acusa.
