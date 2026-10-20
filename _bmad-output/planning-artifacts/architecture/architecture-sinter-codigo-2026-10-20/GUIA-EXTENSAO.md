# Como acrescentar algo novo ao Sinter

Guia para quem programa no Sinter: pessoa ou agente de código. As regras completas estão na [espinha](ARCHITECTURE-SPINE.md). Aqui estão as **receitas**.

## Antes de tudo: onde mora o quê

| Se você vai… | Mexa em… | Nunca em… |
|---|---|---|
| Mudar o formato de um arquivo do catálogo | `domain/model/` | adaptadores |
| Criar uma regra de negócio, um cálculo ou uma herança | `domain/services/` ou `domain/validation/rules/` | `application/`, CLI |
| Criar um comando | `application/` + `ports/inbound/` + `adapters/inbound/cli/` | `domain/` (a não ser que precise de regra nova) |
| Falar com disco, YAML ou Git | `adapters/outbound/` atrás de uma porta | `domain/`, `application/` |
| Ligar peças | `bootstrap.py` | qualquer outro lugar |
| Escrever na tela ou decidir código de saída | `adapters/inbound/cli/` (`render/`, `errors.py`) | `domain/`, `application/` |
| Criar um código de erro | tabela de `domain/errors.py` (AD-37) | `raise Exception(...)` solto |
| Normalizar texto (acento, slug, âncora) | `domain/services/text.py` | qualquer outro lugar |

**Três proibições** (o `poe check` pega todas: import-linter pega a 2, ruff `T20` pega a 3, ruff `banned-api` pega relógio e arquivo na 1):
1. `domain/` não importa nada do projeto fora de si, não lê arquivo e não lê o relógio.
2. Ninguém grava no catálogo fora de `application/apply.py`, `catalog_init.py` e `fmt.py` (AD-36). Fora do catálogo, só `skills_install.py` e `schema_export.py`.
3. Ninguém faz `print` fora de `adapters/inbound/cli/`.

---

## Receita 1: um comando novo

Exemplo: `sinter list areas`.

1. **Contrato** em `ports/inbound/list_areas.py`:
   ```python
   class ListAreasRequest(SinterModel):
       pass                     # nunca catalog_root: a raiz é do Container (AD-27)

   class AreaSummary(SinterModel):
       id: str
       name: str
       description: str | None
       domain_count: int        # sai como "domainCount" no --json (AD-38)

   class ListAreasResult(SinterModel):
       areas: list[AreaSummary]
   ```
   Um caso de uso por **subcomando folha** (`list areas` → `list_areas`). Se um tipo é usado por mais de um `Result`, ele vai para `ports/inbound/common.py` ou é uma visão do domínio (`domain/model/views.py`, como o `Level0`).
2. **Caso de uso** em `application/list_areas.py`: uma classe com `__call__(request) -> result`. Ela recebe as portas no construtor, chama `load` no início e usa funções do `domain`. **Não tem lógica de negócio aqui**: se precisar, crie a função em `domain/services/`.
3. **Montagem** em `bootstrap.py`: acrescente o caso de uso ao `Container`.
4. **CLI**:
   - `adapters/inbound/cli/commands/list_areas.py` lê os argumentos e chama `container.list_areas(...)`. A raiz já vem resolvida (AD-47).
   - `adapters/inbound/cli/render/list_areas.py` formata o texto. Ele imprime fatos e o `summary`, sem montar frase nova.
   - O `--json` sai sozinho do `Result`, pelo `to_json`.
   - Se precisar de erro novo, acrescente o código na tabela de `domain/errors.py`, com o `exit` (AD-37).
   - Registre o comando em `adapters/inbound/cli/app.py`.
5. **Testes:**
   - `tests/application/test_list_areas.py`, com adaptadores `memory`.
   - `tests/cli/test_list_areas.py`, com o `CliRunner` sobre o exemplo.
   - Golden file novo em `tests/golden/list_areas.json`, gerado com `pytest --update-golden`. **Leia o arquivo antes de commitar.**
6. **Contrato publicado:** rode `uv run poe schemas` para que o `ListAreasResult` entre em `schemas/`.

## Receita 2: uma regra de validação nova

Exemplo: "todo subdomínio tem pelo menos uma aplicação" (aviso).

1. Crie o arquivo `domain/validation/rules/subdomain_applications.py`:
   ```python
   @rule(code="SUBDOMAIN_WITHOUT_APPLICATION", severity=WARNING)
   def subdomain_has_application(catalog: Catalog, facts: FileFacts) -> Iterable[Problem]:
       for m in catalog.valid_manifests("Subdomain"):
           if not m.model.spec.applications:
               yield problem(m, "spec", "applications",
                             message="Subdomínio sem aplicação: a IA não saberá onde está o código.")
   ```
2. O código é **`<ASSUNTO>_<PROBLEMA>`**, em SCREAMING_SNAKE. **Não mude o código de uma regra que já existe**, porque testes e skills dependem dele. A mensagem você pode mudar à vontade.
3. **Erro ou aviso?** É erro se o catálogo fica inconsistente ou a IA recebe um link quebrado. É aviso se é só uma má prática ou algo que ainda vai ser preenchido.
4. **Teste** em `tests/domain/validation/test_subdomain_applications.py`, com um caso que passa e um que falha. Os testes verificam o **`code`**, nunca a mensagem.
5. Confira que o exemplo-catalogo continua com **zero erros** (o teste do SM-1). Se a regra nova acusar algo no exemplo, corrija o exemplo ou reveja a regra.
6. Nunca monte o `path` à mão: use sempre `problem(manifesto, *segmentos)` ou `problem_at(entrada)`. O motor carimba o código e a severidade da regra. Ele faz o caminho com o id dos itens de lista (`spec.applications[app-x]`), como manda a AD-35.
7. Se a regra precisa saber algo do arquivo (se está formatado, se um `path` existe), use o `FileFacts` que a regra recebe. Não leia disco.
8. Não precisa registrar a regra em nenhum outro lugar: o `@rule` já coloca no registro, e o `validate` e o `apply` passam a usá-la.

## Receita 3: um campo ou bloco novo num arquivo do catálogo

Exemplo: `sla` no bloco `operation`.

1. **O PRD manda.** Primeiro acrescente o campo no **Apêndice A** do PRD, depois no código.
2. Acrescente o campo ao modelo em `domain/model/`, **na posição em que deve aparecer no arquivo**. A ordem dos campos no modelo é a ordem que o `fmt` usa.
3. Se o campo é obrigatório, decida o que acontece com os catálogos que já existem: subir `schemaVersion` + migração, ou começar como opcional.
4. Se o campo é **calculado**, ele não entra no arquivo: veja a Receita 5.
5. Se o campo vale por herança (o subdomínio herda do domínio), acrescente-o **só** em `domain/services/inheritance.py`.
6. Se o campo cita outro item, crie a regra de referência (Receita 2).
7. Rode `uv run poe schemas` e atualize os golden files que mudarem. **Leia o diff dos golden files antes de commitar.**
8. Acrescente o campo a pelo menos um arquivo do exemplo-catalogo (SM-1: todo campo tem exemplo).
9. Se a skill `sinter-domain` precisa perguntar pelo campo, atualize `skills/sinter-domain/references/entrevista-<kind>.md`.

## Receita 4: um `kind` novo

Exemplo: `Team`.

1. Faça a Receita 3 inteira, criando `domain/model/team.py`.
2. Acrescente o `kind` na tabela "onde é gravado" do FR-18 e em `domain/model/registry.py` (modelo, prefixo e `canonical_path`). É o único lugar, e o `load`, o `validate`, o `new`, o `apply` e o `fmt` leem dele.
3. Acrescente o prefixo de id (Apêndice A.8) e a regra de formato.
4. O `Catalog` precisa indexar o kind novo: um teste em `tests/domain/test_catalog.py`.
5. Se o kind aparece no `get`, acrescente o que ele mostra em cada nível em `domain/services/levels.py`. Lembre do limite de tokens do NFR-1.
6. Se o `sinter new` deve gerar um rascunho do kind novo, crie `domain/drafts/<kind>.py`. Comentários explicativos começam com `#~`, porque o `apply` os remove. Escreva um teste. Nunca copie o modelo para dentro de uma skill: ela pega o rascunho por `sinter new <kind> --json`.

## Receita 5: um campo calculado

Exemplo: "quantos dados com dado pessoal o domínio tem".

1. Implemente o cálculo **só** em `domain/services/calculated.py`, como função pura de `Catalog`.
2. Nunca grave o valor em arquivo: no Apêndice A ele fica marcado `(calc)`, e a regra `CALC_FIELD_WRITTEN` acusa quem escrever.
3. Mostre o campo no nível certo em `domain/services/levels.py`.
4. Escreva um teste de domínio e atualize o golden file.

## Receita 6: uma porta ou um adaptador de saída novo

Exemplo: `SecretScanner` com betterleaks.

1. **Uma porta nova exige uma AD nova na espinha.** Converse antes de criar.
2. Crie a interface em `ports/outbound/<nome>.py` (`typing.Protocol`). Ela recebe e devolve **só** tipos da biblioteca padrão e do `domain`, nunca objetos de biblioteca externa.
3. Implemente em `adapters/outbound/<nome>/`. Se a porta faz I/O, crie também a versão `memory` para os testes. Uma porta pura, como o `ManifestCodec`, não precisa.
4. Ligue no `bootstrap.py`.
5. Escreva testes do adaptador real em `tests/adapters/`. Se ele depende de um programa externo, o teste pula quando o programa não está instalado.

## Receita 7: uma skill nova

1. Crie a skill com a **skill-creator** em `skills/sinter-<verbo>/`, no padrão [Agent Skills](https://agentskills.io/specification).
2. A skill **só** chama `sinter … --json`. Se ela precisa de uma regra que a CLI não tem, a regra vai para a CLI (Receitas 1 e 2), não para o prompt.
3. Toda escrita segue o fluxo `apply - --dry-run` → mostra o resumo → confirmação → `apply -`.
4. Para preencher dados, use a **entrevista guiada**:
   - uma pergunta por vez, com exemplo;
   - opções numeradas vindas da CLI;
   - "não sei" vira pendência;
   - nenhum valor inventado.
5. Escreva os evals contra o exemplo-catalogo, ao lado da skill, e rode `skills-ref validate`.
6. Acrescente a skill ao `sinter skills install`.

---

## Antes de abrir o PR

- [ ] `uv run poe check` passa: import-linter, ruff, mypy e pytest.
- [ ] O exemplo-catalogo continua com zero erros.
- [ ] Os golden files que mudaram foram **lidos**, e a mudança é a esperada.
- [ ] `schemas/` foi regenerado, se algum modelo ou `Result` mudou.
- [ ] O PRD (Apêndice A ou FR) foi atualizado, se o formato ou o comportamento mudou.
- [ ] Nenhum dado real de empresa entrou em teste ou exemplo: só dado sintético.
