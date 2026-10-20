# Análise da documentação PetClinic

Escopo: seis páginas Markdown, cartão, resumos, grafo e inspeção estática do HTML em `eval-3-petclinic-negocio-contratos/with_skill/run-1/outputs/dominio-clinica-veterinaria`. Amostras confrontadas com `../fixtures/spring-petclinic-microservices` (a partir de iteration-2). Não houve execução do sistema ou teste visual do site. Notas medem qualidade documental, não qualidade do software; 0 ausente, 5 parcial com lacunas relevantes, 8 bom com lacunas pequenas, 10 completo verificado.

| Ponto | Nota | Fundamentação |
|---|---:|---|
| Negócio | 8 | Fronteira clara, atores, eventos e hipóteses explícitas; regra de memória não suficientemente comprovada e terminologia CRUD contraditória em outras superfícies. |
| Arquitetura | 7 | Mapa e riscos úteis; texto confunde processamento reativo com chamadas paralelas. |
| Serviços/contratos | 7 | Oito serviços, rotas, dados e falhas; faltam exemplos completos de payload/erro e detalhes da atualização de pet. |
| Jornadas/falhas | 7 | Cinco jornadas com sequências e degradação; caminho do chat incorreto e dúvida que o código local já resolve. |
| Infraestrutura/operação | 7 | Ambientes e dependências claros, produção desconhecida explicitada; faltam procedimento de diagnóstico, persistência/recuperação e pré-requisitos do chat. |
| Referência/onboarding | 7 | Comandos e caminhos úteis; mistura regras de negócio e configuração técnica, interpreta comentário como comportamento confirmado. |
| Rastreabilidade/fidelidade | 6 | Fontes por página, sem commit/linhas por afirmação; amostras revelam deriva semântica. |
| IA cartão/resumos | 6 | Boa leitura progressiva; seção de dúvidas foi extraída incorretamente, texto truncado e erros repetidos. |
| Grafo/consistência | 4 | JSON válido e entidades existentes, mas relações falsas e chamada real ausente. |
| Site/usabilidade (estática) | 5 | Árvore, temas e conteúdo incorporado; links internos sem roteamento, busca só em títulos, dependência CDN. |
| Concisão/repetição | 7 | Estrutura previsível e resumos úteis; glossário/regras/riscos reaparecem sem fonte canônica e mapa duplicado. |

Média aritmética descritiva: 6,5/10. Não representa probabilidade de correção.

## Evidências principais

1. **A narrativa de paralelismo conflita com o código e com o próprio diagrama.** `2-arquitetura.md:93`, `4-jornadas.md:76` e `llm/resumos.md:38` falam em paralelo. A fixture `spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java:56` primeiro busca owner e, no `flatMap`, chama visitas em lote; o diagrama em `4-jornadas.md:95` representa corretamente essa dependência sequencial. O fallback de visitas vazias está confirmado na fixture, linhas 60 e 80, e é bem explicado no documento.
2. **O grafo não preserva a semântica das jornadas.** `llm/grafo.json:70` liga registrar visita a customers, embora `4-jornadas.md:58` e seu diagrama mostrem só visits; `llm/grafo.json:98` liga consultar veterinários a config-server, sem distinguir dependência de inicialização de participação na jornada. `3-servicos.md:259` agrupa vets e genai na mesma célula; o JSON extrai apenas vets (`llm/grafo.json:52`), perdendo gateway → genai. O mapa gerado incorporado ao HTML reproduz a perda.
3. **Chat documentado com caminho direto e dúvida desnecessária.** `4-jornadas.md:158` mostra cliente → genai e `4-jornadas.md:173` deixa o caminho do front-end a confirmar. A fixture `spring-petclinic-api-gateway/src/main/resources/static/scripts/genai/chat.js:42` usa explicitamente `/api/genai/chatclient`: o gateway deve aparecer na jornada da interface fornecida.
4. **“CRUD completo” promete exclusão inexistente na própria documentação.** `3-servicos.md:10` e `llms.txt:13` dizem CRUD completo; `1-negocio.md:52` diz que não há exclusão e as rotas listadas em `3-servicos.md:32` não incluem DELETE. Preferir “cria, consulta e atualiza”.
5. **Memória de dez mensagens precisa de confirmação da configuração real.** `6-referencia.md:39` atribui limite a `MessageChatMemoryAdvisor.order(10)`. A fixture `spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/PetclinicChatClient.java:47` contém um comentário com essa intenção e `.order(10)`, mas não configura ali capacidade de memória; a dependência ChatMemory é injetada. Não tratar o comentário como prova do limite. A afirmação se propaga a negócio, jornada e cartão.
6. **Contrato de edição de pet perde um detalhe essencial.** `3-servicos.md:38` sugere identificação pelo caminho. Na fixture `spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java:70`, o método lê o ID do corpo (`petRequest.id()`), não da variável de caminho. Exemplos de request mostrariam essa exigência e evitariam integração incorreta.
7. **Cartão não preserva as dúvidas prioritárias.** `llms.txt:49` reúne localização de variáveis e “nenhum conflito”, com linhas truncadas, sob “Ainda não se sabe”; perde as perguntas por papel de `6-referencia.md:94`. São referências a variáveis de segredo, não evidência de valores secretos vazados.
8. **Links do conteúdo não navegam no site.** `site/index.html:117` renderiza Markdown sem reescrever/interceptar links `4-jornadas.md`, que apontarão para dentro de `site/`, onde esses arquivos não existem; só links da árvore têm handlers (`site/index.html:91`). Links de página merecem teste funcional e roteamento. A busca (`site/index.html:153`) filtra títulos da árvore, não texto; “telefone” no corpo não será encontrado. CDNs nas linhas 4 e 5 são dependências de carregamento, portanto o HTML não é autossuficiente offline. Avaliação estática, sem alegação de renderização visual.

9. **Âncoras repetidas dos serviços levam ao primeiro bloco.** A página repete subtítulos como “Consome” em oito serviços. `site/index.html:118` gera o mesmo ID por título; `site/index.html:132` usa `getElementById`, portanto navegar para “Consome” de um serviço posterior encontra o primeiro. O ID precisa incluir o serviço pai. Achado cruzado confirmado pelo agente coordenador na estrutura incorporada.

## Repetição, sinergia e forças

- A sequência negócio → arquitetura → serviço → jornada conecta propósito, implementação e falhas; a degradação das visitas é um bom exemplo de risco técnico explicado em consequência de negócio (`2-arquitetura.md:111`, `4-jornadas.md:106`).
- Resumo em cada página e em cada serviço permite leitura por camadas. A repetição curta no cartão é útil quando funciona como índice com links.
- Glossário em `1-negocio.md:94` e `6-referencia.md:17`, regras em `1-negocio.md:74` e `6-referencia.md:31`, além das cópias no cartão, criam múltiplos locais para corrigir uma mesma afirmação. O limite de dez mensagens mostra como um erro se multiplica.
- O HTML incorpora exatamente as seis páginas originais (igualdade textual conferida por script). Isso é uma boa propriedade de geração. Porém injeta um segundo mapa em `site/index.html:120`, conservando o Mermaid original: dois mapas concorrentes, um deles incompleto.
- Hipóteses de negócio e ausência de produção/config externa são normalmente identificadas com clareza. Não se penaliza a inexistência de evidência; penaliza-se deixar dúvidas resolvíveis pelo código ou afirmar inferências como fatos.

## Cinco oportunidades priorizadas

| Prioridade | Oportunidade | Impacto | Esforço | Critério de aceite |
|---|---|---|---|---|
| 1 | Validar afirmações sensíveis com símbolo, linha e revisão da fonte | Alto | Médio | Paralelismo, memória, CRUD e caminho do chat corrigidos ou marcados como hipótese, com evidência específica. |
| 2 | Gerar grafo a partir de relações explícitas, separando execução, inicialização e configuração | Alto | Médio | Gateway → genai presente; nenhuma ligação inferida só por menção textual; diagramas e JSON concordam. |
| 3 | Implementar navegação de links Markdown no HTML e busca no conteúdo | Alto | Médio | Todos os links entre páginas/âncoras abrem o trecho certo; busca encontra “telefone”; dependências offline definidas. |
| 4 | Extrair dúvidas por categoria e manter regras em fonte canônica | Alto | Baixo a médio | Cartão mostra questões reais com links, sem truncamentos e sem confundir variável de segredo com dúvida. |
| 5 | Completar contratos e onboarding com exemplos mínimos verificáveis | Médio | Médio | Um exemplo de criação/edição/falha por contrato crítico, ID de pet no corpo explicado, pré-requisitos do chat e verificação de saúde documentados. |
