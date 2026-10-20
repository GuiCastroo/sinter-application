# 💻 Amelia — avaliação para desenvolvimento

As três documentações permitem entender o domínio e localizar o início de uma mudança. Ainda não fecham igualmente bem a passagem de “entendi” para “reproduzi e verifiquei”. A melhoria prioritária é um caminho concreto de execução/teste por domínio, não mais inventário nem transcrição do código.

Método: leitura das seis páginas, `llms.txt`, resumos e grafo de cada domínio, antes de qualquer fixture. **Não consultei fixtures nem executei aplicações**: as respostas abaixo são o que um dev consegue extrair da documentação. Avalio documentação, não maturidade de produção das demos. Abrir o código indicado para implementar é esperado.

Referências abreviadas: **B** = `eval-1-microservices-boutique/with_skill/run-1/outputs/dominio-online-boutique`; **S** = `eval-2-serverless-coffee/with_skill/run-1/outputs/dominio-serverlesspresso`; **P** = `eval-3-petclinic-negocio-contratos/with_skill/run-1/outputs/dominio-clinica-veterinaria`. Todos relativos a `iteration-3/`. `B/3:269` significa `B/3-servicos.md:269`; demais números correspondem às seis páginas.

## Notas

Suficiência: 0 = sem orientação; 5 = panorama, procura de código ainda ampla; 8 = fluxo, contratos, dados e pontos de alteração localizados, com pequenas lacunas operacionais; 10 = percurso até verificação reproduzível, sem duplicar código. Concisão: 0 = informação útil enterrada; 5 = repetição relevante; 8 = leitura seletiva eficiente; 10 = cada bloco tem função própria.

| Domínio | Suficiência /10 | Concisão /10 | Razão |
|---|---:|---:|---|
| Online Boutique | 8 | 7 | Excelente sequência e falhas; testes genéricos, assistente com carga vetorial desconhecida. Muito texto repetindo sincronismo e natureza de demo. |
| Serverlesspresso | 8 | 7 | Estados, tokens, tabelas e código inativo evitam mudanças no lugar errado. Falta fechar reprodução do pedido e localizar um teste efetivamente utilizável. |
| Clínica Veterinária | 8,5 | 7 | Rotas, DTOs, entidades, classes e comandos mais acionáveis; impacto transversal de novo campo precisa de uma frase adicional. CRUD simples recebe descrição excessiva. |

## Nove tarefas de onboarding

**Respondido** = sei explicar o comportamento e abrir os arquivos certos; **parcial** = há direção, mas falta um elo documental específico; **ausente** = nenhuma orientação. Nenhuma tarefa ficou totalmente ausente; há subperguntas ausentes.

| Domínio / tarefa | Resultado antes do código | Evidência e limite |
|---|---|---|
| B: investigar checkout que retorna 500 após pagamento | **Respondido.** `PlaceOrder` cobra antes de `ShipOrder`; falha de envio retorna `Unavailable`, sem compensação; falhas de carrinho/email posteriores são ignoradas. | B/3:269,284,292; B/4:54. A “cobrança” é simulada, conforme B/3:312. Receita de injeção/reprodução da falha está **ausente**, sem impedir localizar o problema. |
| B: acrescentar campo ao produto e exibi-lo | **Parcial.** Localizo `Product`, `products.json`, loader, contrato proto, handlers/templates e regeneração. | B/3:59,151,156; B/6:58,91. Falta um encadeamento curto produtor → proto → representação/template consumidor; testes são só exemplos genéricos em B/6:79. |
| B: diagnosticar assistente que responde 500 | **Parcial.** Entrada `/bot` → HTTP `/` → Gemini/AlloyDB; conheço payload, flag, credencial e handler. | B/3:480,492,498; B/4:165,182. Processo de carga dos embeddings explicitamente desconhecido em B/3:496; isso limita reprodução completa. |
| S: entender pedido que expira após envio da bebida | **Respondido.** Examinar primeiro token, `ConditionExpression`, sanitização e `SendTaskSuccess`; comparar pausa de 300s com 900s. | S/3:172,174,236,265; S/4:66. Distingue erro de infraestrutura com retry de bebida inválida encerrada silenciosamente. Falta exemplo de execução correlacionada por `orderId`. |
| S: ajustar capacidade do evento | **Respondido.** Alterar ASL ativo; `maxOrdersInQueue` não governa o limite real. Reimplantar stack apropriada. | S/6:72,80,92; S/3:170. Evita editar Lambda órfã (S/5:79). Validar comportamento nas fronteiras requer abrir ASL; não é necessário copiá-lo na doc. |
| S: adicionar consumidor de eventos de pedido | **Parcial.** Modelo de extensão, barramento, nomes, filtros, dados e deploy opcional localizados. | S/6:67,84; S/3:289,338,443. Falta referência pontual a um envelope de evento válido e ao teste que o usa; `node localTest.js` genérico (S/6:75) não fecha a reprodução. |
| P: acrescentar campo do dono à ficha exibida | **Parcial.** Entidade, DTO, schemas, mapper e DTO agregado estão identificados. | P/6:86; P/3:53,287. A receita não lembra conferir `OwnerEntityMapper`, representação do gateway, formulário e tool de cadastro, quando fizerem parte da mudança. Não se pede copiar esses arquivos. |
| P: investigar ficha sem visitas | **Respondido.** Gateway busca dono antes das visitas em lote; fallback retorna visitas vazias; encontro clientes, controller e timeout. | P/4:98; P/3:281,284,290. Teste modular e carga têm caminho em P/6:76; falta apontar qual teste cobre o fallback. |
| P: ajustar comportamento do chat indisponível | **Respondido.** Rota pública/interna, prompt, tools, provedor, descoberta e dois caminhos de falha estão documentados. | P/3:213,225,238,267; P/4:167; P/5:39. Memória desconhecida é corretamente delimitada (P/6:45), não razão para inventar configuração. |

## O que preservar e enxugar

| Ação / trecho | Motivo | Destino | Risco de cortar | Evidência |
|---|---|---|---|---|
| **Manter** contratos + “Por dentro” + falhas | Principal ponte entre incidente e código | Serviços | Alto: perde localização e efeitos parciais | B/3:269–299; S/3:233–268; P/3:278–292 |
| **Manter** sequência complexa, estados e dados | Explicam ordem, persistência e fronteiras | Jornadas/Serviços | Alto: mapa de dependências não substitui cronologia | B/4:42; S/3:178,245; P/4:92 |
| **Resumir** CRUD/listagem simples | Tabela, resumo, frase de orquestração e sequência repetem uma chamada | Mesmas jornadas, uma tabela de entrada/saída | Baixo, mantendo rota, validação e erro | P/4:50–74,114–139 |
| **Mover/consolidar** código inativo | Informação importante aparece duas vezes quase integralmente | S/5:75 como registro; link em Referência | Médio se sumir o aviso junto do caminho ativo | S/6:98; S/5:75 |
| **Remover** explicação de BOAT e enumeração de motores ausentes | Não ajuda uma mudança nesta demo | Nenhum; conservar “sem motor de processo” quando relevante | Baixo | B/6:31; B/2:65; P/2:58 |
| **Resumir** perguntas completas no cartão LLM | Cartão de entrada carrega agenda de evolução além da localização | IDs + assunto + link para Referência | Baixo se preservar lacunas que alteram execução | B/llms.txt:35; S/llms.txt:35; P/llms.txt:33 |
| **Acrescentar mínimo** teste/exemplo existente com comando, pasta e resultado esperado | Fecha onboarding operacional sem criar suíte nova | “Como começar”, 3–5 linhas por domínio após confirmar fontes | Alto se mantida falsa impressão de reprodução completa | B/6:79; S/6:75; P/6:76 |
| **Acrescentar mínimo** consumidores de novo campo | Evita alteração só na persistência | Uma frase em P/6:86 e B/6:91 | Médio: respostas podem perder o campo | P/3:53,287; B/3:62,156 |

Os mapas MD têm apenas `<!-- MAPA-PRINCIPAL -->` (B/2:53; S/2:52; P/2:44): para leitura isolada, acrescentar link direto ao mapa do site/grafo, sem duplicar desenho. O grafo tipado é útil à navegação automatizada; não deve virar leitura obrigatória humana. Resumos funcionam como alternativa inicial às páginas, não como etapa adicional obrigatória.

## Exemplo de simplificação

Antes, P/4:89: “busca síncrona em `customers-service`, depois busca em sequência (dono antes das visitas) (reativo) em `visits-service`, protegida por um circuit breaker”.

Depois: “`ApiGatewayController.getOwnerDetails` busca o dono e depois as visitas dos seus pets. O circuit breaker `getOwnerDetails` devolve visitas vazias se essa segunda consulta falhar.” Mantém ordem, ponto de código e efeito observável; diagrama preserva contratos.

## Percurso mínimo, sem nova documentação

- **Dev:** resumo do Negócio → jornada da tarefa → serviços participantes → Referência: regras e Como começar → Infra apenas do ambiente usado → código/teste indicado.
- **PM:** Negócio → parte de negócio da jornada → regras e perguntas de produto na Referência.
- **Arquiteto:** Arquitetura → sequência crítica → contratos/dados/falhas dos participantes → Infra → decisões e incertezas na Referência.

Esse roteamento pode caber em três linhas no índice existente. Não ler seis páginas em série, resumos e grafo para toda tarefa.
