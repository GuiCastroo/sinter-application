# Análise da documentação Online Boutique

Escopo: seis páginas, llms.txt, llm/resumos.md, llm/grafo.json e site/index.html da iteração 2, with_skill/run-1. Inspeção estática; nenhuma alegação de teste visual, deploy ou execução da aplicação. Conferência factual por amostragem na fixture `../fixtures/microservices-demo` (relativa à pasta iteration-2). As notas medem qualidade documental, não maturidade da aplicação demo. Escala: 0 ausente; 5 parcial com lacunas relevantes; 8 bom com lacunas pequenas; 10 completo verificado.

Os caminhos de evidência documental abaixo são relativos a `eval-1-microservices-boutique/with_skill/run-1/outputs/dominio-online-boutique`. Fontes indicadas como fixture são relativas ao repositório microservices-demo.

| Ponto | Nota | Fundamentação |
|---|---:|---|
| Negócio | 8 | Fronteira, propósito demo, atores, regras e parede claros; busca apresentada como jornada disponível sem evidência de UI; validade do cartão incorreta. |
| Arquitetura | 8 | Bom mapa, opcionais e riscos; linguagem “saga” sem compensação e “contratos nunca divergem” é excessivamente categórica. |
| Serviços/contratos | 7 | Cobertura consistente dos 12 componentes com métodos, dados, erros e fontes; consumo SearchProducts não existe no frontend da fixture, tratamento de erro generalizado e ordem do pagamento incorreta num trecho. |
| Jornadas/falhas | 8 | Três jornadas com negócio e sequência; falhas checkout bem tratadas; checkout chamado simultaneamente orquestração e coreografia; ramificações do diagrama merecem precisão. |
| Infraestrutura/operação | 7 | Recursos, portas, componentes e variantes bem apresentados; loadgenerator ligado incorretamente ao LB; faltam comandos de diagnóstico e caminho de recuperação. |
| Referência/onboarding | 7 | Boas trilhas de mudança e dúvidas por papel; comandos de testes genéricos, pré-requisitos e validação de sucesso pouco acionáveis. |
| Rastreabilidade/fidelidade | 6 | Fontes por seção e inferências explícitas, mas sem versão/commit e linhas; amostragem encontra erros de regra, contrato e topologia. |
| IA cartão/resumos | 5 | Degraus úteis, porém cartão trunca justamente conflitos/segredos, tem âncora vazia e outra incorreta; resumos copiam imprecisões. |
| Grafo/consistência | 5 | Arestas e jornadas úteis, porém jornada assistente omite o próprio assistente; contrato frontend→SearchProducts falso; infraestrutura ausente. |
| Site/usabilidade | 5 | Árvore, tema, parede, responsividade e breadcrumb presentes no código; busca só títulos, links entre MD não roteados, IDs repetidos e dependência CDN. |
| Concisão/repetição | 6 | Estrutura previsível ajuda consulta independente; regras, riscos e ressalvas se repetem sem fonte canônica e propagam erro. |

Média aritmética: **6,5/10** (72/11). Não ponderada; site avaliado apenas por inspeção estática.

## Forças verificadas

- Separação padrão versus opcionais evita confundir demonstração local com cloud: `5-infraestrutura.md:19`, `3-servicos.md:439`.
- Inventário de contratos, dados, implementação e falhas por serviço é consistente: `3-servicos.md:90`, `3-servicos.md:252`.
- Checkout mostra perda de consistência e erro não bloqueante em vez de só caminho feliz: `3-servicos.md:278`, `4-jornadas.md:92`. Conferido em fixture `src/checkoutservice/main.go:238`, `:252`, `:258`, `:273`.
- Frete fixo corresponde à fonte: `1-negocio.md:82` e fixture `src/shippingservice/quote.go:34`.
- Identifica divergência README versus taxas estáticas e distingue decisão reconstruída: `6-referencia.md:40`, `:92`.

## Achados prioritários

1. **Alta — derivados de IA perdem informação e relações.** `llms.txt:50`–54 contém frases interrompidas (“Banco”, “variável”), não as dúvidas completas. `llms.txt:29` liga a `4-jornadas.md#` e `:23` omite `-opcional` da âncora. `llm/grafo.json:195`–198 associa jornada assistente somente a frontend, embora `4-jornadas.md:187`–200 explicite assistente, Gemini e AlloyDB. Isso prejudica recuperação e análise de impacto justamente no formato de máquina.
2. **Alta — regra de cartão errada em múltiplas saídas.** `1-negocio.md:81`, `3-servicos.md:313`, `4-jornadas.md:96`, `6-referencia.md:34` dizem validade estritamente posterior ao mês atual; fixture `src/paymentservice/charge.js:80` rejeita apenas quando mês atual é maior, portanto aceita o mês atual. O comentário da própria fonte é impreciso: a documentação precisa priorizar a condição executada.
3. **Alta — site não trata links de conteúdo como navegação interna.** `site/index.html:117` renderiza Markdown; handlers de navegação são ligados apenas à árvore (`:91`), sem interceptação dos links do artigo. Assim links como `4-jornadas.md#...` resolvem sob `/site/`, onde não existem os MD. Além disso `:118` cria o mesmo ID para cada “Expõe”, “Consome”, “Dados” etc. ao longo de Serviços e `:132` usa getElementById, que pode levar à primeira ocorrência. Constatação estática, sem execução no navegador.
4. **Média — funcionalidade disponível no catálogo confundida com consumo/UI.** `3-servicos.md:50` e `llm/grafo.json:26` atribuem SearchProducts ao frontend. Fixture `src/frontend/rpc.go:45`–55 implementa ListProducts/GetProduct, e busca textual nos três arquivos frontend main/handlers/rpc não encontra SearchProducts. `1-negocio.md:39`, `4-jornadas.md:121` apresentam busca ao cliente sem distinguir capacidade RPC da exposição na UI.
5. **Média — contradições e topologia.** `3-servicos.md:319`–321 diz recusa de pagamento antes de cotar frete, mas cotação ocorre antes da cobrança (fixture `src/checkoutservice/main.go:238`, `:252`). `5-infraestrutura.md:72` conecta gerador ao LoadBalancer; fixture `kubernetes-manifests/loadgenerator.yaml:83` usa frontend:80 interno. `3-servicos.md:71` diz única exceção de erro é anúncio, contradizendo recomendação best-effort em `:393` e `4-jornadas.md:89`.
6. **Média — busca e portabilidade do site limitadas.** `site/index.html:153`–157 busca somente textos da árvore; termos de conteúdo como regra de Visa não são pesquisáveis. CDN externo em `:4`–5 e chamada de mermaid em `:73` antes de montar conteúdo impedem tratar HTML como totalmente offline. O mapa gerado é inserido sem remover mapa autoral (`:120`–125), produzindo repetição de mapas.
7. **Baixa — precisão conceitual.** `4-jornadas.md:7` chama todo fluxo de coreografia apesar do checkout orquestrado; `2-arquitetura.md:121` e `6-referencia.md:47` prometem “contratos nunca divergem”, sem verificar geração/versionamento dos clientes. `3-servicos.md:6` chama demais serviços de folhas embora frontend e recommendation chamem outros.

## Repetição útil, desperdício e sinergias

- **Útil:** regra de negócio na parede, serviço e jornada atende perguntas diferentes. Resumo inicial e catálogo padronizado permitem leitura independente. Não remover toda repetição.
- **Desnecessária:** mesma lista Visa/Mastercard, frete, email e cookie em `1-negocio.md:77`, `4-jornadas.md:92`, `6-referencia.md:30`, cartão e resumo; não há registro central da regra. Erro do vencimento prova o custo de manutenção.
- **Desnecessária:** “sem filas / gRPC / checkout orquestra” reaparece nas aberturas de arquitetura, serviços e jornadas; poderia ser um resumo breve com link ao detalhe. Explicações repetidas de demo, “a confirmar” e inexistência de motor adicionam ruído quando já comprovadas.
- **Sinergia reutilizável nas três documentações:** mesmos serviços, contratos, jornadas e regras deveriam alimentar páginas humanas, grafo, resumos e navegação com IDs estáveis e proveniência única. Neste domínio, a discrepância entre assistente no diagrama e ausência no grafo mostra por que a geração precisa validar relações, não apenas formato.
- **Sinergia de apresentação:** manter parede em linguagem de negócio + sequência técnica + falhas, com links entre essas três perspectivas; inventário de infraestrutura como extensão dos mesmos IDs de serviço.

## Cinco oportunidades

| Prioridade | Oportunidade | Impacto | Esforço | Aceite concreto |
|---|---|---|---|---|
| 1 | Validar cartão/grafo/âncoras contra conteúdo original | Alto | Baixo–médio | Nenhuma frase cortada, todas âncoras existentes, jornada assistente inclui assistente. |
| 2 | Corrigir gerador do site: roteamento, IDs qualificados, busca no corpo | Alto | Médio | Clique entre páginas permanece no site; cada Expõe navega ao serviço correto; busca Visa encontra regra. |
| 3 | Fatos e regras com ID, símbolo e commit de origem | Alto | Médio | Regra de validade representada corretamente uma vez, derivados consistentes; contratos consumidos conferidos contra chamadas. |
| 4 | Transformar infraestrutura e onboarding em trilha operacional curta | Médio | Baixo–médio | Pré-requisitos, comandos por serviço, resultado esperado, diagnóstico Redis e procedimento de recuperação com limitações. |
| 5 | Reduzir duplicação preservando camadas de leitura | Médio | Baixo | Um mapa principal; resumos remetem à fonte da regra; ressalvas distinguem desconhecido, inferido e verificado. |

Nenhum original foi alterado. A análise factual é amostral: ausência de achado não significa validação exaustiva.
