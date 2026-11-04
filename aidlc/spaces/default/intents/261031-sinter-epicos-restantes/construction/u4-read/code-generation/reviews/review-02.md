## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Iteration:** 2
**Verdict Dictated:** no
**Date:** 2026-11-03T19:54:43Z

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Critical | sinter/src/sinter/application/read.py > validação de rel e leitura CatalogFiles; sinter/src/sinter/adapters/outbound/yaml_fs/files.py > FsCatalogFiles.read, integração pontual autorizada | A contenção verifica apenas segmentos lexicais. Um path cadastrado como docs/arquivo.md pode ser um link simbólico para um Markdown fora da raiz ou fora do docs permitido; exists e Path.open seguem esse link. Nenhuma camada resolve o destino físico e verifica sua contenção antes de abrir. Assim, a leitura prometida como restrita ao catálogo pode devolver conteúdo externo ao catálogo para o consumidor. A inspeção confirmou o caminho de chamada; nenhum arquivo externo real foi aberto para testar a exposição. | Fazer o adaptador verificar o destino físico resolvido contra a raiz e o diretório docs autorizado antes da leitura, recusando escapes por arquivo ou diretório symlink. Manter a I/O no adaptador e adicionar regressões com alvo sintético fora do catálogo e alvo dentro do catálogo mas fora de docs; ambos devem ser recusados sem devolver conteúdo. | Resolved (reviewer) |
| R-02 | Major | sinter/src/sinter/domain/services/markdown.py > geração de anchors em index_markdown | A contagem de duplicatas é feita por título-base, sem reservar os anchors já emitidos. Para '# Regras', '# Regras', '# Regras-1', a reprodução devolve regras, regras-1, regras-1. O terceiro título fica inacessível por uma âncora única e section_content retorna sempre a seção anterior. | Garantir unicidade global dos anchors gerados, inclusive colisões entre nomes naturais com sufixo e sufixos criados por duplicação. Acrescentar casos Regras/Regras/Regras-1 e Regras-1/Regras/Regras e verificar que cada seção é recuperável por seu próprio anchor. | Resolved (reviewer) |
| R-03 | Major | sinter/src/sinter/domain/services/markdown.py > controle de fence em index_markdown | O parser guarda somente os três primeiros marcadores de um fence e fecha o bloco ao ver qualquer linha com os mesmos três caracteres. Em um bloco válido aberto com quatro backticks que contém um exemplo com três, '# codigo' é indexado como título real. A reprodução gerou Intro/codigo/Real e a seção Intro terminou antes do código. Também não verifica se a linha de fechamento contém apenas marcador e whitespace. | Guardar tipo e comprimento do fence de abertura; fechar apenas com o mesmo marcador, comprimento suficiente e restante da linha permitido como fechamento. Acrescentar regressões com fence de quatro caracteres contendo três, fences de til e backtick, linha de código parecida com fechamento e extração da seção completa. | Resolved (reviewer) |
| R-04 | Minor | sinter/src/sinter/domain/services/text.py > gh_anchor; sinter/src/sinter/domain/services/markdown.py > remoção de fechamento ATX | O normalizador remove underscores apesar de eles fazerem parte de anchors GitHub; gh_anchor('API_client') produz apiclient, em vez de api_client. O parser também transforma o título válido '# C#' em 'C', removendo um hash que não é fechamento ATX, pois não é precedido por whitespace. O índice pode alterar nomes técnicos e apresentar âncoras incompatíveis com o documento. | Preservar underscores no slug e remover hashes de fechamento de título somente quando obedecerem à sintaxe ATX. Acrescentar testes para API_client, C#, fechamento separado por espaço e pontuação/acento já suportados. | Resolved (reviewer) |

> R-01 Reviewer note: Read usa agora CatalogDocumentReader para o conteúdo. FsCatalogDocumentReader recusa symlink em cada componente, resolve raiz/docs/destino e verifica destino dentro de docs e docs dentro da raiz antes de abrir. Os testes com arquivo apontando para fora do catálogo e para fora de docs passaram, esperando recusa; não há leitura do conteúdo externo nesses testes. A mesma inspeção de componentes cobre links de diretório. FsCatalogFiles continua usado para manifestos/exists, não para devolver o conteúdo do documento.

> R-02 Reviewer note: O conjunto de anchors já emitidos é global. As duas ordens de colisão natural/sufixo têm regressões e passaram. A reprodução independente gerou regras, regras-1 e regras-1-1 e recuperou três seções distintas.

> R-03 Reviewer note: O fence ativo guarda caractere e comprimento; fecha somente com o mesmo caractere, comprimento suficiente e cauda vazia/whitespace. Testes cobrem marcador curto, cauda com texto e til versus backtick. A reprodução independente indexou somente Intro/Real e preservou o heading de código dentro da seção Intro.

> R-04 Reviewer note: gh_anchor preserva underscore. A remoção de hashes finais exige whitespace antes deles. Regressão e reprodução confirmaram API_client → api_client, título C# preservado e fechamento Closing ### reduzido ao título Closing.

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| uv run --directory sinter pytest tests/domain/test_markdown.py tests/application/test_read.py tests/cli/test_read_cli.py | 30 passed in 1.74s; exit 0 | Executado exatamente como solicitado; inclui regressões das falhas anteriores e os caminhos principais da Story 2.4. |
| uv run --project sinter --directory sinter poe check | 3 contratos kept; Ruff passa; 153 arquivos formatados; mypy sem erros em 94 fontes; 183 passed in 7.51s; exit 0 | Verificação completa executada; permanece o aviso uv sobre project relativo a directory, sem impedir a execução correta. |
| Reprodução independente sem I/O | Anchors regras/regras-1/regras-1-1; três seções distintas; headings de fence Intro/Real; código preservado; underscore e títulos técnicos preservados | Confirma diretamente as correções de parsing sem modificar fonte ou fixture. |

### Acceptance Coverage

Os caminhos por id e por path cadastrado/canônico mantêm resolução para documentos do catálogo. A consulta sem anchor entrega índice, anchors e tamanhos com content nulo, sem corpo completo. Seção solicitada é limitada pelo próximo heading do mesmo nível ou superior; anchor ausente retorna ANCHOR_NOT_FOUND, disponíveis e saída 1. URL-only informa link e aviso sem chamada de rede. A leitura efetiva de Markdown está na borda, por porta específica composta em bootstrap, com rejeição lexical e física de destinos não permitidos.

O manifesto da U4 inclui a nova porta de leitura de documentos, seu adaptador e os testes alterados. O único arquivo adicional consultado foi a integração FsCatalogFiles autorizada pelo responsável. Não houve leitura de diretório de outra unidade nem alteração de arquivos do produto.

### Summary

Os quatro achados anteriores foram corrigidos e as duas verificações solicitadas passaram. Não há novos achados materiais neste passe; a Story 2.4 está pronta dentro do escopo revisado.
