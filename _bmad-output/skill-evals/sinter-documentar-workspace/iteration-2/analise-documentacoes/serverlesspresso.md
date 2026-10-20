# Avaliação da documentação Serverlesspresso

Data: 2026-09-26. Escopo: os seis Markdown, `llms.txt`, `llm/resumos.md`, `llm/grafo.json` e `site/index.html` em `eval-2-serverless-coffee/with_skill/run-1/outputs/dominio-serverlesspresso`. Conferência amostral com `fixtures/serverless-coffee`. Leitura estática; não foi executado navegador, deploy ou jornada real. Notas editoriais, não percentuais de testes: 0 ausente, 5 parcial com lacunas relevantes, 8 bom com lacunas pequenas, 10 completo e verificado. Caminhos abaixo relativos ao domínio, salvo os prefixados com `fixture:`.

## Notas

| Ponto | Nota /10 | Evidência e motivo |
|---|---:|---|
| Negócio | 8 | `1-negocio.md:34` delimita faz/não faz/dúvidas; parede explica atores e regras (`:42`). KPIs explicitamente desconhecidos (`:102`). FIFO anunciado no resumo sem prova apontada; classificação como não comercial é inferida. |
| Arquitetura | 7 | `2-arquitetura.md:91` explica REST, eventos, tokens e riscos com clareza. Visão de nove serviços mistura código inativo e métricas opcionais; resumo de sincronismo omite leituras de dados compartilhados. Mapa gerado no site não mantém a semântica do mapa autoral. |
| Serviços e contratos | 8 | `3-servicos.md:69`, `:209`, `:273` inventariam endpoints, consumidores, handlers e falhas. Faltam exemplos de payload e respostas para uso direto; extensões assumidas (`:396`). CountingTable aparece como consumo de um serviço declarado inativo (`:152`, `:361`). |
| Jornadas e falhas | 7 | `4-jornadas.md:44` e `:122` conectam negócio à sequência técnica; timeout e indisponibilidade explícitos. Cliente chama GET restrito a admin (`:55`); recibo prometido não aparece na sequência. Timeout diz não passar pelo manager (`:90`), embora handler do manager trate o evento (`3-servicos.md:231`). |
| Infraestrutura e operação | 6 | Inventário detalhado com origem e ordem de deploy (`5-infraestrutura.md:26`, `:81`). Resumo informa quatro tabelas e duas máquinas (`:3`), mas o próprio inventário lista cinco tabelas e três máquinas (`:39`–`:47`), confirmado na fixture. Faltam procedimento de diagnóstico, recuperação e validação do deploy. |
| Referência e onboarding | 7 | `6-referencia.md:65` informa onde mudar e como publicar; decisões são corretamente rotuladas como reconstruídas (`:40`). Pré-requisitos, exemplo de teste com resultado esperado e validação pós-deploy são insuficientes; dúvidas têm papel, não responsável/critério de resolução. |
| Rastreabilidade e fidelidade | 6 | Arquivos/estados/handlers nomeados permitem checar; distinção de inferências é boa (`6-referencia.md:40`). Referências geralmente por página ou glob, sem commit/linha. Contradições objetivas de ator/contagens e repetição delas nos resumos reduzem confiança. |
| IA: cartão e resumos | 6 | Boa progressão por páginas e seções (`llm/resumos.md:24`). Cartão tem trechos truncados e títulos vazios tratados como dúvidas (`llms.txt:49`–`:54`); links de serviços usam slugs incompletos (`:14` vs título em `3-servicos.md:60`). Resumos em `llm/` apontam `3-servicos.md` sem `../`. Tamanho aproximado chars/4 do cartão: 1.385, não tokenização real. |
| Grafo e consistência | 3 | JSON sintaticamente válido, mas `jornada_usa_servico` vazio (`llm/grafo.json:156`) apesar das duas sequências. `chamadas` mistura consumo de evento, acesso a dados e callback sem tipo explícito; seta do consumidor para produtor conflita com mapa de fluxo (`:60` vs `2-arquitetura.md:83`). Há dependência de serviço inativo (`:35`) e destino `—` (`:125`). |
| Site e usabilidade — estática | 5 | Tem navegação em árvore, tema, parede visual e responsividade (`site/index.html:60`, `:76`, `:93`). Conteúdo embutido das seis páginas coincide exatamente com Markdown. Scripts CDN obrigatórios (`:4`), busca só em títulos (`:153`), links Markdown não são interceptados pelo roteador e âncoras de h3 repetem (`:118`). Arquitetura recebe mapa adicional sem retirar o original (`:120`). Sem teste visual/interativo. |
| Concisão e repetição | 6 | Resumos e seis perspectivas ajudam leitura gradual. Mesmas regras repetidas em negócio, jornadas, referência, cartão e resumos; código órfão repetido em arquitetura/serviços/infra/referência. Algumas repetições dão contexto, outras multiplicam manutenção. A maior perda é propagação de erro, não tamanho absoluto. |

Média aritmética ilustrativa: **6,3/10** (69/11). Critérios têm peso igual apenas para esta síntese.

## Achados prioritários e prova

1. **Grafo perde a relação jornada–serviço e induz dependência de código inativo.** `llm/grafo.json:156` vazio; `:35`–`:39` liga processor a counting-service, embora `3-servicos.md:361` diga que não é implantado. Evento consumido vira seta consumidor→produtor (`grafo.json:60`) sem atributo que diferencie dependência de fluxo, enquanto mapa autoral usa produtor→consumidor (`2-arquitetura.md:83`). No site, o mapa gerado só agrupa `00-baseCore`; demais nomes com caminhos não coincidem com os nomes curtos dos subdomínios. Os rótulos de contratos são truncados no campo `D.mapa` (`site/index.html:67`).
2. **Resumo de infraestrutura contradiz inventário e código.** `5-infraestrutura.md:3`–`:5` e diagrama `:96`: duas máquinas/quatro tabelas. Existem cinco `AWS::DynamoDB::Table` em `fixture:01-appCore/template.yaml:143,197,317,497,648`, e três `AWS::Serverless::StateMachine` em `:67,759,791`. A contradição é copiada em `llm/resumos.md:45` e cartão. Não confundir “duas orquestradoras do pedido” com total de máquinas.
3. **Jornada atribui ação administrativa ao cliente.** `4-jornadas.md:55`: cliente chama `GET /qr-code`; `3-servicos.md:83` diz “Só admin”. `fixture:backends/9-validator/code/getCode.js:11`–`:28` verifica grupo `admin` e retorna 403. Inserir Admin/Display na sequência resolve a contradição.
4. **Navegação tem destino inconsistente.** Links de `llms.txt:14` apontam `#validator-service`, mas título gera `#validator-service-backends9-validator`. Em `site/index.html:91`, somente links da árvore recebem handler; links de conteúdo renderizado ficam como `./4-jornadas.md` relativos a `site/`, onde não existem. `:118` cria o mesmo ID para cada “Expõe”, “Consome” e “Quando falha”, tornando navegação por subseção ambígua. A inspeção identifica problema estrutural; não executou clique em browser.
5. **Compressão remove qualificadores úteis.** `llms.txt:50`–`:54` preserva títulos e frase cortada no lugar de perguntas completas. `llm/resumos.md:30` afirma que recibo grava todo evento, enquanto `3-servicos.md:317` registra o filtro por `userId`. Prosa comprimida deve preservar restrições.

## Repetições e sinergias

- **Útil:** explicar a mesma jornada em linguagem de negócio, sequência e máquina de estados; cada representação serve uma pergunta diferente (`1-negocio.md:42`, `4-jornadas.md:44`, `3-servicos.md:167`). Preservar, mas derivar regras de catálogo único.
- **Útil:** resumo inicial de página e camada curta para IA; permite decidir o que abrir sem absorver catálogo inteiro.
- **Desnecessária:** tabela completa de limites em `1-negocio.md:72`, `4-jornadas.md:92` e `6-referencia.md:31`, mais cartão e resumo. Manter fonte canônica com IDs de regra e projeções breves.
- **Desnecessária:** achado de código órfão em `2-arquitetura.md:124`, `3-servicos.md:192`, `5-infraestrutura.md:74`, `6-referencia.md:92`; manter registro único com links de contexto.
- **Sinergia a comparar nos três domínios:** o mesmo esquema deve gerar navegação, grafo e cartões usando IDs estáveis; cada domínio mantém suas particularidades (eventos/tokens aqui). A adaptação ao domínio é forte; o extrator que converte tabelas “Consome” em relações universais é frágil.

## Cinco oportunidades

| Prioridade | Oportunidade | Impacto | Esforço | Resultado verificável |
|---|---|---|---|---|
| 1 | Modelo com IDs estáveis, tipos de relação (publica/consome/chama/lê), status ativo/opcional/inativo e vínculos jornada–serviço | Alto | Médio | Grafo explica as duas jornadas; nenhum destino `—`; inativo não vira serviço chamado; mapa autoral e derivado concordam. |
| 2 | Checagem cruzada de fatos e atores antes de gerar resumos | Alto | Baixo–médio | Cinco tabelas/três máquinas no inventário total; ação de GET atribuída ao admin; summaries preservam escopo e ressalvas. |
| 3 | Corrigir links, slugs por serviço e navegação do site; validar sem depender só de contagem de elementos | Alto | Médio | Toda ligação interna resolve, cada h3 tem ID único, busca encontra termos do corpo; smoke de navegação confirma. |
| 4 | Transformar regras, riscos e dúvidas em registros canônicos com origem precisa e resolução | Alto | Médio | Projeções reutilizam o mesmo valor/regra; cada dúvida tem evidência, papel responsável e critério de fechamento. |
| 5 | Completar operação e contratos com exemplos mínimos | Médio–alto | Médio | Um pedido demonstrável com payload/status esperado; autenticação e pré-requisitos claros; diagnóstico de token perdido, timeout e falha de publicação IoT. |

Limites: nenhuma conclusão sobre qualidade visual em tela, acessibilidade completa ou comportamento real AWS. A maioria do conteúdo técnico é sólida e localizável, mas as falhas de representação e navegação impedem nota alta para o conjunto.
