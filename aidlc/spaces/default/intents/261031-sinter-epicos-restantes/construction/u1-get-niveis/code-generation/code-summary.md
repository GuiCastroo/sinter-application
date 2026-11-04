# U1 — Story 2.1: consulta nos níveis 0 e 1

## Resultado

Implementação local existente concluída e preservada: consultas de domínio/subdomínio, herança com origem, status, gaps, omitted, JSON e texto determinísticos. 43 novos cenários executáveis; 132 testes na suíte integrada passam.

## Arquivos

- `sinter/src/sinter/domain/model/views.py`
- `sinter/src/sinter/ports/inbound/get.py`
- `sinter/src/sinter/domain/services/inheritance.py`
- `sinter/src/sinter/domain/services/levels.py`
- `sinter/src/sinter/domain/services/summary.py`
- `sinter/src/sinter/application/get.py`
- `sinter/src/sinter/adapters/inbound/cli/commands/get.py`
- `sinter/src/sinter/adapters/inbound/cli/render/get.py`
- `sinter/schemas/get-result.schema.json`
- `sinter/tests/domain/test_views.py`
- `sinter/tests/domain/test_inheritance.py`
- `sinter/tests/domain/test_levels.py`
- `sinter/tests/application/test_get.py`
- `sinter/tests/cli/test_get_cli.py`
- `sinter/tests/contract/test_schemas.py`

Bootstrap, registro do comando em app.py, índice em catalog.py, registro de exportação GetResult e tokens.py já existiam no trabalho local e foram reutilizados sem descartar alterações da pessoa. O manifesto lista os 15 arquivos efetivamente criados/modificados nesta unidade; não reivindica alterações de outros autores.

## Decisões técnicas

- Level0 usa união discriminada por kind com campos próprios: domínio tem domainId/area; subdomínio tem identidade, propósito, status e contagem fixa de aplicações. Removidos nulls de atributos de outros kinds e contagens extras não exigidas para Level0. O domínio pai aparece no nível 1 do subdomínio.
- Nível 1 expõe fatos e conhecimento diretamente, sem wrappers JSON level0/knowledge redundantes. Propriedades Python mantêm acesso às projeções para renderer e serviços. O schema exportado representa essa forma real.
- Docs com id declarado usam IdentifiedDocView; docs anônimos não inventam id. Null explícito é preservado para campos existentes como path/url.
- Mantida a heurística original fixa ceil(len(text)/4). A alternativa de alterar heurística ou truncar fatos foi rejeitada. Também rejeitado manter todos os campos irrelevantes no Level0 porque excedia o orçamento JSON.
- Operação herda somente campos não declarados, distinguindo ausência de lista vazia explícita; inheritedFrom identifica o domínio de origem dos campos herdados.
- Get não usa manifesto inválido como modelo válido: informa ITEM_NOT_FOUND com orientação para validate. Findings de carregamento dos demais arquivos aparecem no Report e conduzem saída 1, em vez de serem descartados.
- Regulações/padrões no texto mostram origem completa; decisões exibem data/decisão; filhos mostram nome, propósito, status e contagem.
- Nível 2 continua escopo da U3: uma requisição level2 informa nível 1 entregue e omitted para a vizinhança, sem fingir cumprimento da Story 2.3.

## Evidência por critério de aceite

| Critério Story 2.1 | Evidência executada |
|---|---|
| Identidade/contagens nível 0 | tests/domain/test_levels.py e tests/cli/test_get_cli.py |
| Nível 1 e ordem do sumário | tests/domain/test_levels.py; tests/application/test_get.py; CLI com regras, docs, termos e ADR |
| Listas vazias explícitas | teste de gaps em levels e test_empty_lists_are_explicit na CLI |
| Herança marcada | tests/domain/test_inheritance.py, aplicação e CLI; regra/regulação/glossário/operação |
| JSON/omitted | testes de união discriminada, camelCase, round-trip, determinismo e comandos omitidos |
| Item ausente, saída 1 e sugestões | aplicação e CLI com até três sugestões; manifesto inválido também testado |
| Orçamento CAMB níveis 0/1 | teste sobre a fixture intacta, medindo JSON real indentado |

## Comandos e resultados

- Baseline recebido antes das mudanças: pytest 87 passed, 2 failed; poe check interrompia em dois erros Ruff locais após 3 contratos de importação íntegros.
- `uv run --directory sinter pytest tests/domain/test_views.py tests/domain/test_inheritance.py tests/domain/test_levels.py tests/application/test_get.py tests/cli/test_get_cli.py tests/contract/test_schemas.py`: **46 passed in 2.64s**.
- `uv run --directory sinter poe schemas`: **12 schemas, 1 alterado**, get-result.schema.json. Teste compara todo o conjunto esperado e exige GetResult.
- `uv run --project sinter --directory sinter poe check`: **3 contratos kept, Ruff passa, 135 arquivos formatados, mypy 82 fontes sem erros, 132 passed in 3.43s**.
- Medição CAMB (nível, JSON, texto) em tokens: **(0, 174, 98), (1, 1996, 1014)**.
- Ruff check --fix e Ruff format foram executados somente nos arquivos desta unidade para organização de imports/formatação.
- Falhas intermediárias de testes revelaram dois valores incorretos do próprio teste: fixture PAGV tem 4 aplicações e não declara operação no domínio. As asserções foram corrigidas consultando a fixture; herança de operação usa pai sintético válido, sem alterar fixture de referência.

## Limitações e riscos

- **Margem do orçamento JSON nível 1 é de apenas 4 tokens** no CAMB atual. U2 deve integrar calculados mantendo o NFR1 e reavaliar o tamanho; esta unidade não adicionou antecipadamente esses campos nem ocultou fatos para simular sua futura integração.
- O comando protegido aprovado emite aviso uv de diretório project relativo inexistente após --directory, mas executa poe check no projeto correto e termina 0. Não foi alterado por esta unidade.
- Testes/evals LLM não são critérios da U1; nenhum resultado de modelo foi simulado.
- Nenhum teste planejado deixou de executar. Nenhum push, publicação, deploy, commit ou limpeza de árvore foi feito.

