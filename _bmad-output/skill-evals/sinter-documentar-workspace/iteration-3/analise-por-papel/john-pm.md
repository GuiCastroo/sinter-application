# 📋 John — avaliação como PM recém-chegado

As três documentações permitem entender o produto representado, suas fronteiras e jornadas. O maior ganho viria de **qualificar promessas e trazer consequências ao percurso de negócio**, com menos texto repetido. Não falta um PRD completo.

Leitura independente dos seis MD, `llms.txt` e `llm/resumos.md` de cada domínio v3, sem consultar avaliações anteriores ou executar aplicações. Esta é avaliação documental, não confirmação do código. Referências abaixo usam **B** = `eval-1-microservices-boutique/with_skill/run-1/outputs/dominio-online-boutique`, **C** = `eval-2-serverless-coffee/with_skill/run-1/outputs/dominio-serverlesspresso`, **P** = `eval-3-petclinic-negocio-contratos/with_skill/run-1/outputs/dominio-clinica-veterinaria`, relativos a `iteration-3/`.

## Notas e suficiência

Escala: **0–2** não permite entender; **3–4** exige investigação extensa; **5–6** orienta com lacunas materiais; **7–8** suficiente com consultas pontuais; **9–10** permite decisões usuais com evidência clara. Concisão mede economia de leitura preservando decisão, não apenas tamanho.

| Domínio | Suficiência | Concisão | Julgamento |
|---|---:|---:|---|
| Online Boutique | 8/10 | 7/10 | Propósito pedagógico e fronteira muito claros; risco simulado descrito como perda financeira real em alguns trechos. |
| Serverlesspresso | 7/10 | 7/10 | Atores, valor e limites explícitos; garantias de ordem e atualização são mais fortes no resumo que nas evidências apresentadas. |
| Clínica Veterinária | 8/10 | 7/10 | Excelente distinção entre histórico, agendamento e prontuário; papéis hipotéticos e efeito do histórico indisponível precisam ficar mais visíveis. |

**Boutique:** `1-negocio:28–44` explica por que existe e o que não faz. A parede dá sequência e regras (`49–56`). Entretanto, “cliente já foi cobrado” (`4-jornadas:85`) conflita semanticamente com pagamentos simulados (`1-negocio:42,86–87`). A ausência de estorno é limitação para eventual integração real, não dinheiro perdido na demo. O texto também marca o propósito como “a confirmar” embora cite declaração explícita (`1-negocio:29–35`); separar fato atual de intenção futura evita dúvida artificial.

**Coffee:** valor operacional, cliente/barista/admin e limites estão bem apresentados (`1-negocio:24–50`). “Barista prepara na ordem em que os pedidos chegam” (`1-negocio:4`) não tem regra de FIFO demonstrada nas páginas: qualquer barista pode assumir/devolver (`4-jornadas:29`). “Cliente é avisado na hora” (`1-negocio:50`) precisa qualificação: falha de publicação pode impedir atualização (`2-arquitetura:83–84`). São promessas relevantes para operação, não detalhe técnico.

**Petclinic:** valor de ficha consolidada, capacidades e exclusões aparecem cedo (`1-negocio:27–41`). A parede revela visita sem pet validado e ficha sem histórico quando indisponível (`48–49`), útil para priorizar qualidade. Mas papéis ainda desconhecidos (`38–39`) viram atores assertivos (`46–50`); marcar “atores ilustrativos, permissões não confirmadas” basta. Valor de reduzir papel é hipótese razoável, não resultado medido. “Core” é classificação assumida, explicitamente qualificada.

Ausência de metas, receita, roadmap ou donos de squads é legítima para demos. Não deve gerar exigência de inventar KPIs. Já limite por cliente sem aplicação confirmada, operação do cardápio e distinção entre histórico vazio/indisponível afetam entendimento concreto. Podem permanecer desconhecidos, desde que próximos da decisão afetada.

## Nove perguntas de decisão

| Domínio / pergunta realista | Resultado | Resposta e evidência |
|---|---|---|
| B — Posso apresentar como loja pronta para vendas? | Respondido | Não: demonstração, sem cobrança/frete reais, estoque ou histórico. `1-negocio:28–44`. |
| B — Falha no email invalida a compra? | Respondido | Não; nem falha ao limpar carrinho bloqueia conclusão. `6-referencia:48`; pagamento continua simulado (`1-negocio:42`). |
| B — Posso prometer “meus pedidos” sem ampliar escopo? | Respondido | Não existe histórico; pedido só é devolvido na resposta. `1-negocio:44`; `6-referencia:34,126`. |
| C — Configurar fila para 10 limita o evento a 10 simultâneos? | Respondido | Não: limite efetivo documentado é 20 fixo; mudar exige implantação. `6-referencia:80–83,91–93`. |
| C — Posso garantir um café por pessoa e atendimento por chegada? | Parcial | Config traz 1, aplicação não confirmada; resumo promete ordem, jornada só descreve assumir/devolver. `6-referencia:44`; `1-negocio:4`; `4-jornadas:29`. |
| C — Quem muda cardápio durante o evento, por qual procedimento? | Parcial | Admin é ator sugerido, API só altera abertura; edição direta precisa procedimento confirmado. `1-negocio:39,46`; `6-referencia:113–115`. |
| P — “Registrar visita” reserva horário ou registra atendimento? | Respondido | Registro histórico; sem confirmação ou conflitos de agenda. `1-negocio:37`; `4-jornadas:50–59`. |
| P — Ficha sem visitas prova que pet nunca foi atendido? | Respondido | Não: falha também devolve histórico vazio, visualmente indistinguível. `1-negocio:49`; `2-arquitetura:73`. |
| P — Dono pode alterar cadastros ou só recepção? | Ausente | Matriz de permissões não estabelecida; o documento reconhece papéis desconhecidos, sem resolver autorização. `1-negocio:38–39,46–47`; `6-referencia:112`. Ausência legítima do material, impeditiva dessa promessa específica. |

## O percurso curto basta?

**`1-negocio` sozinho basta para orientação, não para todas as decisões acima.** Boutique pede consulta ao checkout e Referência; Coffee exige Referência para distinguir configuração de regra efetiva; Petclinic pede a ficha do dono e confirmação de papéis. Nenhum requer ler o inventário de serviços inteiro como PM.

Percurso recomendado: negócio → bloco de negócio da jornada relevante → regras/questões vinculadas. Hoje a navegação quebra esse percurso: “Regras que mandam” e “Linguagem” só remetem genericamente a outra página. Melhor um link direto para regras decisivas/IDs, sem repetir a tabela inteira. Em Petclinic a consequência “indisponível parece sem histórico” está mais clara em arquitetura que em negócio.

`llms.txt` funciona como índice; `resumos.md` funciona para consulta seletiva por agente. Não recomendaria ambos como leitura humana obrigatória: repetem o resumo inicial e acrescentam bastante linguagem de componentes.

## Cortes e acréscimos mínimos

| Ação / trecho | Motivo | Destino | Risco de cortar | Evidência |
|---|---|---|---|---|
| Resumir “Em resumo” + “Em uma frase” nos três | Mesma promessa repetida antes do conteúdo | Uma abertura com valor e finalidade | Baixo, preservando público e limites | B `1:3–7,24–26`; C `1:3–7,24–27`; P `1:3–5,22–25` |
| Manter parede e fronteira | Melhor relação informação/decisão | Negócio | Alto: perde atores, sequência e exclusões | B `1:37–56`; C `1:35–51`; P `1:34–51` |
| Mover detalhes de orquestração e telemetria | gRPC, fan-out, task token e provedores de métricas não decidem o valor | Arquitetura/jornada técnica | Baixo se preservar responsável e consequência | B `1:67–84`; C `1:61–78`; P `1:64–85` |
| Resumir dúvidas duplicadas | “Não sabemos”, dúvidas de contexto e questões por papel repetem temas | Questão canônica com link específico | Médio: manter visível incerteza decisiva | C `1:38–41`, `6:113–127`; P `1:37–41`, `6:106–112` |
| Remover BOAT do glossário PM | Categoria ausente não ajuda entender a loja | Eliminar; arquitetura já registra ausência | Baixo | B `6:31` |
| Mover timeout/retry/cache das regras de negócio | Mistura implementação com política de produto | Referência técnica; manter efeito percebido | Médio se remover consequência | P `6:46–48`; B `6:45` |
| Acrescentar qualificadores pontuais | Evita promessa de dinheiro, FIFO ou papéis verificados | Resumo/parede/jornada correspondente | Alto se mantiver formulação atual | B `4:85`; C `1:4,50`; P `1:38–50` |

## Exemplo e organização reutilizável

**Antes — Coffee, `1-negocio:64`:** “Duas máquinas de Step Functions cooperando. Uma toca o relógio do pedido e pausa esperando ação humana; a outra recebe a ação (via API) e ‘acorda’ a primeira”.

**Depois:** “O sistema acompanha o pedido enquanto espera cliente e barista: cancela após 5 minutos sem escolha ou 15 minutos sem conclusão. Veja a implementação nas duas máquinas em Arquitetura.” Preserva a consequência decisiva (`6-referencia:42–43`) e deixa o mecanismo acessível.

Organização mínima comum, sem nova página: abertura com finalidade/público/valor; fronteira; parede com regras e falhas que mudam o resultado; links das jornadas; até três dúvidas decisivas com evidência. Referência conserva regras completas e perguntas identificadas. Marcar cada afirmação sensível como observada, inferida ou desconhecida no próprio ponto de uso; deixar possíveis evoluções fora do caminho principal.
