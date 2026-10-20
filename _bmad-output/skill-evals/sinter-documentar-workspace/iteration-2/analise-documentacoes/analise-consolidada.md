# Análise comparativa das três documentações Sinter v2

Data: 2026-09-26. Escopo: as três saídas `with_skill/run-1/outputs` da iteração 2. Um subagente por domínio, com a mesma rubrica; o coordenador conferiu propriedades comuns dos artefatos e dos geradores. Foram analisadas as seis páginas de cada domínio, cartão, resumos, grafo e HTML, com conferência amostral nas fixtures locais. As versões `old_skill` não fazem parte desta avaliação.

**Parecer:** a estrutura de seis páginas organiza bem o entendimento humano. As maiores oportunidades estão na fidelidade de fatos e na transformação desse conteúdo em grafo, cartão e navegação. A média descritiva é **6,4/10**; os 11/11 testes anteriores não equivalem a qualidade documental plena.

## Notas por ponto

Escala comum: 0 = ausente; 5 = parcial com lacunas relevantes; 8 = bom com lacunas pequenas; 10 = completo e verificado. As notas são julgamentos fundamentados, não medições de precisão. Médias aritméticas sem pesos. O site foi inspecionado estaticamente: não houve teste visual/interativo, auditoria completa de acessibilidade ou execução das aplicações.

| Ponto | Online Boutique | Serverlesspresso | PetClinic |
|---|---:|---:|---:|
| Negócio | 8 | 8 | 8 |
| Arquitetura | 8 | 7 | 7 |
| Serviços e contratos | 7 | 8 | 7 |
| Jornadas e falhas | 8 | 7 | 7 |
| Infraestrutura e operação | 7 | 6 | 7 |
| Referência e onboarding | 7 | 7 | 7 |
| Rastreabilidade e fidelidade | 6 | 6 | 6 |
| Cartão e resumos para IA | 5 | 6 | 6 |
| Grafo e consistência | 5 | 3 | 4 |
| Site e usabilidade — inspeção estática | 5 | 5 | 5 |
| Concisão e repetição | 6 | 6 | 7 |
| **Média** | **6,5** | **6,3** | **6,5** |

Justificativas e evidências por nota: [Boutique](boutique.md), [Serverlesspresso](serverlesspresso.md), [PetClinic](petclinic.md).

## O que se repete e vale preservar

1. **Fronteira explícita:** faz / não faz / não sabemos impede ampliar o domínio por suposição. Os três casos conseguem explicar o propósito antes da tecnologia.
2. **Leitura por camadas:** resumo, página completa e detalhe do serviço atendem pessoas e agentes com perguntas diferentes. Repetir uma síntese curta aqui tem função.
3. **Conexão entre negócio e falhas:** a parede explica o resultado esperado, a jornada mostra a colaboração e o serviço explica a falha. Boutique se destaca no checkout; PetClinic, na ficha sem histórico quando visitas falha; Serverlesspresso, na cooperação das máquinas e nos timeouts.
4. **Estrutura previsível:** seis páginas e subseções recorrentes permitem trocar de domínio sem reaprender a organização. O conteúdo Markdown incorporado ao HTML é idêntico ao original nos três casos, uma boa propriedade do gerador.

## Repetições que geram custo e inconsistência

| Padrão | Evidência | Consequência | Tratamento sugerido |
|---|---|---|---|
| Regra reaparece integralmente em negócio, jornada, referência e derivados | Regra de validade do cartão na Boutique; limites do pedido no café; memória do chat na PetClinic | Um erro se espalha e precisa de correção em vários lugares | Uma definição canônica com ID e fonte; sínteses contextualizadas nas demais páginas |
| Dois mapas na mesma página | Os três HTML conservam o mapa autoral e inserem o derivado das tabelas Consome | Leitor compara representações de semântica/cobertura diferentes sem explicação | Um mapa principal; segunda visão somente com propósito, legenda e relações claramente distintos |
| Mesmos títulos viram a mesma âncora | “Consome” aparece 12, 10 e 8 vezes, respectivamente | Navegação de outro serviço encontra a primeira ocorrência | IDs compostos por página, serviço e subseção |
| Dúvidas extraídas por posição textual | `llms.txt`, seção “Ainda não se sabe”, nos três casos | Cabeçalhos, localização de variáveis e frases cortadas substituem perguntas úteis | Extrair perguntas completas por categoria, com link e prioridade |
| Mesma afirmação de integração em várias aberturas | Arquitetura, serviços e jornadas | Alongamento sem novo conteúdo | Uma frase local e link para explicação principal |

Não remover toda repetição: o critério é se ela responde uma pergunta diferente ou apenas replica uma afirmação sujeita a mudança.

## Problemas concretos por domínio

- **Boutique:** a regra documentada exige validade posterior ao mês atual, mas a condição executada aceita o próprio mês atual. O erro aparece em quatro páginas e derivados. O grafo da jornada do assistente omite o assistente. Evidências em [boutique.md](boutique.md), itens 1 e 2.
- **Serverlesspresso:** resumo de infraestrutura declara quatro tabelas/duas máquinas, enquanto inventário e template mostram cinco/três. A jornada atribui ao cliente uma chamada restrita ao administrador. As duas jornadas têm zero vínculos com serviços no JSON. Evidências em [serverlesspresso.md](serverlesspresso.md), itens 1–3.
- **PetClinic:** prosa descreve buscas em paralelo, mas o código busca o dono antes das visitas; o diagrama representa essa dependência corretamente. A jornada do chat omite o gateway usado pelo frontend. A afirmação sobre memória de dez mensagens não está comprovada pela configuração citada. Evidências em [petclinic.md](petclinic.md), itens 1, 3 e 5.

Esses exemplos mostram que resumo, comentário de código e texto de README não bastam para confirmar comportamento. Ausência de evidência deve continuar explícita, sem ser confundida com falha da documentação.

## Sinergias entre os três casos

**Um inventário com IDs estáveis pode alimentar todas as saídas.** Atualmente o título do serviço serve também como identidade; qualificadores como “opcional” ou caminhos de diretório prejudicam a associação das jornadas. Separar ID, nome de exibição, caminho e estado ativo/opcional/inativo beneficia cartão, grafo, mapas, links e navegação ao mesmo tempo.

**As relações precisam expressar o que significam.** Uma chamada de API, consumo de evento, acesso a tabela e configuração na inicialização são diferentes. Serverlesspresso evidencia a mistura dessas relações; PetClinic evidencia ligações inferidas por menção textual; Boutique evidencia vínculos perdidos por nomes decorados. Cada jornada deve declarar explicitamente seus participantes e relações, e o gerador deve preservar essa semântica.

**Os três domínios formam uma boa base de testes complementares.** Boutique cobre checkout síncrono e efeitos parciais; café cobre eventos, callbacks, estados e componentes inativos; PetClinic cobre cadastro, agregação com fallback e chamadas de IA. A combinação pode validar o padrão sem exigir que todos sejam descritos como o mesmo tipo de sistema.

**A manutenção do site é compartilhada.** O JavaScript a partir de `let tema` é idêntico nos três HTML. Corrigir IDs e roteamento no gerador resolve uma classe comum de problemas. Os links Markdown no corpo não passam pelo roteador da árvore e apontam para arquivos inexistentes dentro de `site/`.

## Oportunidades priorizadas

Estimativas qualitativas de impacto e esforço; não são compromisso de prazo.

| Ordem | Oportunidade | Impacto | Esforço | Como verificar |
|---|---|---|---|---|
| 1 | Corrigir IDs e roteamento dos links no gerador do site | Alto, nos três domínios | Baixo–médio | Toda subseção abre o serviço certo; links entre páginas permanecem no site; nenhum destino interno ausente |
| 2 | Usar IDs estáveis e relações explícitas/tipadas no grafo | Alto, sobretudo para IA e análise de impacto | Médio | Jornada do assistente inclui assistente; café tem participantes nas duas jornadas; gateway→genai aparece na PetClinic; nenhum destino `—` |
| 3 | Conferir e centralizar regras/fatos com origem específica | Alto, reduz erro propagado | Médio | Validade, inventário e ordem das chamadas correspondem ao código; fonte registra revisão e símbolo/linha; derivados concordam |
| 4 | Corrigir extração de dúvidas e compressão do cartão | Alto para contexto da IA | Baixo–médio | Perguntas completas, qualificadores preservados, links válidos e nenhuma frase interrompida |
| 5 | Evoluir os critérios automáticos para consistência | Alto, evita falsa confiança | Médio | Verificar cada jornada e sua falha, integridade de links, IDs únicos, relações esperadas e concordância entre inventário/resumos |
| 6 | Completar contratos e onboarding críticos | Médio–alto | Médio | Exemplo mínimo de request/response/erro, pré-requisitos, resultado esperado e diagnóstico por jornada crítica |
| 7 | Reduzir cópias integrais e esclarecer portabilidade do HTML | Médio | Baixo–médio | Um mapa principal; regras referenciadas; decisão explícita sobre dependências CDN e busca no corpo |

O site depender de CDNs não contradiz, por si só, “abre sem servidor”. Contudo, impede tratar o arquivo como autossuficiente sem internet. Busca no corpo seria uma melhoria além do requisito atual de filtrar a árvore.

## O que os testes atuais não demonstram

`grade2.py:53–58` estima tokens por caracteres/4; `:65–67` exige somente um diagrama de sequência; `:68–71` exige somente três ligações no grafo. Não demonstra que cada jornada tem caminho de erro, que as relações são verdadeiras ou que os links funcionam. O resultado 11/11 continua válido para esses critérios limitados.

Medições independentes registradas em [medicoes.json](medicoes.json):

| Medida | Boutique | Café | PetClinic |
|---|---:|---:|---:|
| Serviços no JSON | 12 | 13 | 8 |
| Chamadas no JSON | 19 | 22 | 7 |
| Jornadas no JSON | 3 | 2 | 5 |
| Vínculos jornada–serviço | 15 | 0 | 12 |
| Cartão: estimativa caracteres/4 | 1.468 | 1.384 | 1.423 |
| Resumos: estimativa caracteres/4 | 1.916 | 1.927 | 1.461 |
| Palavras aproximadas nas seis páginas | 8.684 | 8.635 | 8.297 |

Contagens de relações não são medidas de completude. Tokens acima são estimativas, não tokenização de um modelo específico. Tempos de leitura, contraste e comportamento visual não foram medidos.

## Recomendação

Preservar as seis páginas e a leitura em camadas. Concentrar a próxima iteração em navegação correta, identidade/semântica das relações e fidelidade dos resumos. Os ganhos devem ser feitos no padrão e nos geradores, seguidos da regeneração dos três casos e verificação de consistência. Os documentos originais e o PRD não foram alterados nesta análise.
