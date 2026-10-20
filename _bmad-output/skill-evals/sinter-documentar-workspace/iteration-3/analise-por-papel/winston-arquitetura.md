# 🏗️ Winston — suficiência e concisão para arquitetura

Data: 2026-09-30. Escopo: os três conjuntos `with_skill` da iteration-3. Avaliação do coordenador sob a skill bmad-agent-architect; Amelia e John avaliam seus papéis em paralelo. Leitura documental, sem executar aplicações nem conferir novamente as fixtures. Evidências abaixo são relativas à pasta de cada domínio. O site foi considerado como apresentação do mesmo conteúdo; as conclusões arquiteturais vêm dos Markdown e do grafo.

## Parecer

Há contexto suficiente para explicar a decomposição, os fluxos principais e os riscos mais visíveis. Não há contexto suficiente para assumir que o mapa é um inventário completo de todas as dependências nem para tomar decisões de produção sem consultar fontes e responsáveis. Essa limitação é aceitável em projetos de demonstração, desde que explícita.

Escala: 0 ausente; 5 orientação parcial; 8 entendimento consistente com poucas lacunas; 10 suficiente e conciso para as decisões avaliadas. Notas editoriais, não percentuais de acerto.

| Domínio | Suficiência | Concisão | Motivo |
|---|---:|---:|---|
| Online Boutique | 8 | 6 | Checkout, dados efêmeros, mocks e opcionais bem localizados; explicações repetem ausência de motores/filas e misturam demonstração com risco financeiro real. |
| Serverlesspresso | 7 | 6 | Boa descrição de tokens, eventos e ASL; generalização do sincronismo e mapa parcial tornam perigoso resumir mais antes de qualificar o escopo. |
| PetClinic | 8 | 7 | Propriedade dos dados, gateway, fallback e chat compreensíveis; repetição de perguntas e mistura de decisão observada com motivação inferida prejudicam consulta. |

## Nove decisões testadas só com a documentação

“Respondido” significa que a documentação permite formular a decisão ou localizar seu impacto, não que autoriza uma mudança de produção.

| Domínio / decisão | Resultado | O que a documentação permite concluir |
|---|---|---|
| Boutique: onde atuar ao substituir pagamento simulado por integração real? | Respondido | `paymentservice`, contrato Charge e orquestração no checkout; falha após pagamento precisa de decisão de compensação. `3-servicos.md:308`, `4-jornadas.md:67`, `2-arquitetura.md:83`. |
| Boutique: carrinhos sobrevivem ao ambiente padrão? | Respondido | Redis usa emptyDir e o catálogo é arquivo; variantes gerenciadas são opcionais. `5-infraestrutura.md:3`, `2-arquitetura.md:86`. |
| Boutique: habilitar o assistente afeta quais fronteiras? | Respondido | Frontend, assistente, Gemini, AlloyDB e Secret Manager estão descritos; Kustomize condiciona ativação. `3-servicos.md:464`, `4-jornadas.md:155`. |
| Café: como aumentar capacidade sem editar um campo inoperante? | Respondido | Limite de 20 está no ASL e não usa maxOrdersInQueue; exige alteração e implantação da máquina. `2-arquitetura.md:77`, `6-referencia.md:40`. |
| Café: qual o impacto de um evento novo nos consumidores? | Parcial | Recibo recebe eventos do bus e filtra userId; publishers e métricas têm consumidores. Falta um resumo verificável dos campos/versão de um evento crítico para avaliar compatibilidade. `2-arquitetura.md:63`, `2-arquitetura.md:85`, `3-servicos.md:311`. |
| Café: como o pedido sai da espera e o que acontece sem token? | Respondido | Cooperação por TaskToken/SendTaskSuccess, pausas e timeout descritos; ausência de recuperação confirmada é explicitada. `4-jornadas.md:35`, `4-jornadas.md:88`, `2-arquitetura.md:79`. |
| PetClinic: quais componentes afetam a ficha sem histórico? | Respondido | Gateway busca dono antes das visitas e retorna lista vazia em falha; distinção “sem visitas” versus indisponibilidade fica oculta ao usuário. `4-jornadas.md:78`, `2-arquitetura.md:73`. |
| PetClinic: existe integridade transacional dono/pet/visita? | Respondido | Visit guarda petId sem validação cruzada; não há transação entre os serviços. `4-jornadas.md:50`, `2-arquitetura.md:75`. |
| PetClinic: posso afirmar isolamento de bancos em produção? | Parcial | Perfis e esquema existem; três serviços podem apontar ao mesmo MySQL. Instâncias reais e configuração externa não foram confirmadas. `2-arquitetura.md:66`, `2-arquitetura.md:76`, `5-infraestrutura.md:23`. Não inventar topologia. |

## O que manter, reduzir e acrescentar

| Ação | Trecho / evidência | Destino ou substituição | Risco de cortar |
|---|---|---|---|
| Manter | Responsabilidade de cada componente, dono dos dados, estado opcional/inativo; `3-servicos.md` nos três | Catálogo de serviços consultado por seção | Alto: sem isso não se estima impacto |
| Manter | Sequência de checkout, tokens e fallback; jornadas citadas acima | Uma sequência principal com exceções por fluxo complexo | Alto: mapa de dependências não substitui ordem de execução |
| Resumir | Boutique `2-arquitetura.md:61–70`; PetClinic `2-arquitetura.md:51–60`: listas de tecnologias ausentes | “Chamadas síncronas; sem mensageria. Checkout orquestrado em código”, com as exceções locais | Baixo se sincronismo, timeout e responsável permanecerem |
| Unificar | “Decisões que moldam” da Arquitetura e “Decisões” da Referência nos três | Decisão e consequência ficam em Arquitetura; Referência mantém fonte e link. Evitar duas tabelas completas | Médio: não perder a indicação de motivação inferida |
| Mover | Detalhes de implantação, portas e inventários repetidos em “Infra que usa” | Infraestrutura canônica; serviço mantém apenas nome do recurso e link | Baixo; preservar propriedade dos dados em Serviços |
| Remover | Blocos “Regras e dúvidas” que só repetem o mesmo link ao fim de toda jornada; Boutique `4-jornadas.md:92,147,194`, PetClinic `:46,74,110,139,184` | Uma chamada de Referência no topo; links locais apenas às regras que mudam o resultado daquela jornada | Baixo; links genéricos repetidos não acrescentam contexto |
| Unificar | “Dúvidas e perguntas”, “Dúvidas de contexto” e “Perguntas para decisão” em Referência | Um registro de pendências com categoria, evidência, impacto e responsável; fatos conhecidos ficam fora dele | Médio: preservar conflitos entre fontes, não apagar incerteza |
| Qualificar | Café `2-arquitetura.md:3–7` diz “nada é síncrono”, mas relações declaram acessos compartilhados a dados | Dizer “coordenação entre serviços por eventos e callbacks; há acesso direto a tabelas” | Alto se uma síntese falsa orientar mudança |
| Acrescentar pouco | Escopo do mapa e do grafo | Uma frase: mapa de relações declaradas, não inventário completo de recursos; links para dados/infra. No café, CountingTable é recurso interno do domínio embora não seja serviço | Alto se “externo” for confundido com fora da fronteira organizacional |
| Acrescentar pouco | Contrato de evento crítico do café | Um exemplo com campos essenciais e produtor/consumidor, ou link preciso ao schema/handler existente | Médio: não copiar todos os payloads do código |

O grafo chama de `interno` o destino que coincide com ID de serviço. Isso é classificação de inventário, não de fronteira do domínio: CountingTable aparece como externo, embora seja uma tabela do próprio sistema. Em PetClinic, Config/Discovery são descritos como dependências gerais, mas não aparecem como relações de cada serviço no grafo. Não inferir ausência de acoplamento pela ausência de aresta.

## Exemplo de simplificação preservando o contexto

**Antes:** o resumo de arquitetura do café declara um barramento, nove serviços, dois workflows, ausência de sincronismo e duas exceções; os serviços depois detalham acessos a tabelas compartilhadas.

**Depois proposto:** “O pedido é coordenado por order-processor e order-manager, que cooperam por eventos e TaskToken/SendTaskSuccess. Os demais consumidores reagem aos eventos; configurações e estado também são lidos diretamente no DynamoDB. A entrada é REST e a atualização dos aplicativos usa MQTT. Frontends ficam fora deste repositório; consulte Serviços para componentes ativos e opcionais.”

Preserva coordenação, estado, interfaces e fronteira; remove contagem ambígua e generalização falsa.

## Percurso mínimo do arquiteto

1. Negócio: resumo e fronteira.
2. Arquitetura: contexto, mapa, decisões e riscos.
3. Uma jornada central: checkout / pedido de café / ficha do dono ou chat.
4. Somente os serviços e recursos afetados pela decisão.
5. Referência: questões que bloqueiam essa decisão e fontes.

A centralização não deve transformar “Regras que mandam” em um mero desvio para outra página: conservar duas ou três consequências essenciais no contexto e apontar os IDs das regras completas. Não criar outra “documentação para arquitetos”. Usar links para esse percurso no índice. A forma mais segura de encurtar é retirar repetição e qualificar frases absolutas, preservando efeitos de falha, estados, fronteiras e evidências.
