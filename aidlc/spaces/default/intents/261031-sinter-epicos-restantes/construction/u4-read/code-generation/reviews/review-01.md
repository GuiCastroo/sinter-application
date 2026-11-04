## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Iteration:** 1
**Verdict Dictated:** no
**Date:** 2026-11-03T19:47:09Z

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Critical | sinter/src/sinter/application/read.py > validação de rel e leitura CatalogFiles; sinter/src/sinter/adapters/outbound/yaml_fs/files.py > FsCatalogFiles.read, integração pontual autorizada | A contenção verifica apenas segmentos lexicais. Um path cadastrado como docs/arquivo.md pode ser um link simbólico para um Markdown fora da raiz ou fora do docs permitido; exists e Path.open seguem esse link. Nenhuma camada resolve o destino físico e verifica sua contenção antes de abrir. Assim, a leitura prometida como restrita ao catálogo pode devolver conteúdo externo ao catálogo para o consumidor. A inspeção confirmou o caminho de chamada; nenhum arquivo externo real foi aberto para testar a exposição. | Fazer o adaptador verificar o destino físico resolvido contra a raiz e o diretório docs autorizado antes da leitura, recusando escapes por arquivo ou diretório symlink. Manter a I/O no adaptador e adicionar regressões com alvo sintético fora do catálogo e alvo dentro do catálogo mas fora de docs; ambos devem ser recusados sem devolver conteúdo. | New |
| R-02 | Major | sinter/src/sinter/domain/services/markdown.py > geração de anchors em index_markdown | A contagem de duplicatas é feita por título-base, sem reservar os anchors já emitidos. Para '# Regras', '# Regras', '# Regras-1', a reprodução devolve regras, regras-1, regras-1. O terceiro título fica inacessível por uma âncora única e section_content retorna sempre a seção anterior. | Garantir unicidade global dos anchors gerados, inclusive colisões entre nomes naturais com sufixo e sufixos criados por duplicação. Acrescentar casos Regras/Regras/Regras-1 e Regras-1/Regras/Regras e verificar que cada seção é recuperável por seu próprio anchor. | New |
| R-03 | Major | sinter/src/sinter/domain/services/markdown.py > controle de fence em index_markdown | O parser guarda somente os três primeiros marcadores de um fence e fecha o bloco ao ver qualquer linha com os mesmos três caracteres. Em um bloco válido aberto com quatro backticks que contém um exemplo com três, '# codigo' é indexado como título real. A reprodução gerou Intro/codigo/Real e a seção Intro terminou antes do código. Também não verifica se a linha de fechamento contém apenas marcador e whitespace. | Guardar tipo e comprimento do fence de abertura; fechar apenas com o mesmo marcador, comprimento suficiente e restante da linha permitido como fechamento. Acrescentar regressões com fence de quatro caracteres contendo três, fences de til e backtick, linha de código parecida com fechamento e extração da seção completa. | New |
| R-04 | Minor | sinter/src/sinter/domain/services/text.py > gh_anchor; sinter/src/sinter/domain/services/markdown.py > remoção de fechamento ATX | O normalizador remove underscores apesar de eles fazerem parte de anchors GitHub; gh_anchor('API_client') produz apiclient, em vez de api_client. O parser também transforma o título válido '# C#' em 'C', removendo um hash que não é fechamento ATX, pois não é precedido por whitespace. O índice pode alterar nomes técnicos e apresentar âncoras incompatíveis com o documento. | Preservar underscores no slug e remover hashes de fechamento de título somente quando obedecerem à sintaxe ATX. Acrescentar testes para API_client, C#, fechamento separado por espaço e pontuação/acento já suportados. | New |

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| uv run --directory sinter pytest tests/domain/test_markdown.py tests/application/test_read.py tests/cli/test_read_cli.py | 23 passed in 1.84s; exit 0 | Os cenários principais passam, mas não cobrem as colisões, fences longas e contenção física identificadas. |
| uv run --project sinter --directory sinter poe check | 3 contratos kept; Ruff passa; 151 arquivos formatados; mypy sem erros em 92 fontes; 176 passed in 8.31s; exit 0 | Verificação completa executada. O aviso do uv sobre o argumento project relativo a directory permanece sem impedir a execução correta. |
| Reprodução independente sem I/O de catálogo | Anchors [('Regras','regras'), ('Regras','regras-1'), ('Regras-1','regras-1')]; headings de fence Intro/codigo/Real; seção Intro truncada; API_client vira apiclient; C# vira título C | Confirma as falhas de parsing sem alterar fonte ou fixtures. |
| Inspeção pontual do adaptador de leitura autorizada pelo responsável | read usa (root / path).open sem resolve/relative_to; exists também segue o alvo | Sustenta a ausência de contenção física. Não houve leitura de dados externos reais. |

### Acceptance Coverage

ID de documento e path cadastrado/canônico são resolvidos; a consulta sem âncora devolve índice de headings, anchors e contagem de linhas com content nulo. A âncora ausente usa ANCHOR_NOT_FOUND com disponíveis, e URL-only devolve URL e aviso sem chamada de rede. Os casos comuns de corte por heading de nível igual/superior passam. As visões e o caso de uso mantêm os contratos camelCase e as fronteiras hexagonais.

Os casos de segurança por links físicos e de parsing acima impedem considerar a Story 2.4 concluída. O manifesto inclui os caminhos da implementação principal e seus três arquivos de teste; o adaptador foi consultado apenas como integração explicitamente autorizada, não foi modificado por esta revisão. A rastreabilidade FR16 aponta para o teste CLI existente, mas a aprovação final exige fechar as lacunas comportamentais identificadas.

### Summary

A entrega funciona nos exemplos atuais e todas as verificações solicitadas passaram, mas há uma falha de contenção física com risco de leitura fora do catálogo e duas falhas de parsing que tornam seções inacessíveis ou truncadas. Corrigir esses pontos com regressões antes de encerrar U4.
