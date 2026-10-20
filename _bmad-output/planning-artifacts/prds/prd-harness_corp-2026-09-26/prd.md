---
title: "PRD — Sinter"
status: final
created: 2026-09-26
updated: 2026-09-26
inputs:
  - ../../briefs/brief-harness_corp-2026-09-26/brief.md
  - ../../briefs/brief-harness_corp-2026-09-26/addendum.md
  - ../../research/domain-harness-engineering-context-engineering-definicoes-e-concorrencia-research-2026-09-26.md
  - ../../ux-designs/ux-harness_corp-2026-09-26/EXPERIENCE.md
  - ../../ux-designs/ux-harness_corp-2026-09-26/DESIGN.md
---

# PRD: Sinter

## 0. Propósito do Documento

Este PRD define **o que** o MVP do Sinter precisa fazer. Ele é a entrada para arquitetura (`bmad-architecture`) e épicos (`bmad-create-epics-and-stories`). Parte do [product brief](../../briefs/brief-harness_corp-2026-09-26/brief.md) e da [pesquisa de domínio](../../research/domain-harness-engineering-context-engineering-definicoes-e-concorrencia-research-2026-09-26.md), sem repeti-los. A especificação de UX já existe e é a referência para telas e comportamento: [DESIGN.md](../../ux-designs/ux-harness_corp-2026-09-26/DESIGN.md), [EXPERIENCE.md](../../ux-designs/ux-harness_corp-2026-09-26/EXPERIENCE.md) e [mockups](../../ux-designs/ux-harness_corp-2026-09-26/mockups/).

Como ler:
- O vocabulário segue o **Glossário (§3)**; os termos são usados sempre da mesma forma.
- As funcionalidades estão agrupadas em **§4**, com requisitos numerados (FR-1 a FR-N) e jornadas (UJ-N).
- O que foi inferido está marcado com `[SUPOSIÇÃO]` e listado em **§11**.
- Escolhas técnicas (ferramentas, formatos, limites) ficam no [addendum](addendum.md).

## 1. Visão

Software chega ao código pelas mãos de várias pessoas, e **em cada passagem de bastão o contexto se perde**. O Sinter é a camada onde esse contexto é **construído**: o arquiteto organiza cada domínio (repos, documentos, regras, decisões) em um padrão que não vira bola de lama, os papéis desenham a solução em conversas guiadas que já conhecem o domínio, e cada tarefa viaja do PM ao dev acumulando contexto.

O resultado é materializado em uma pasta `.sinter/` dentro de cada repo. Quem abre o repo, humano ou agente, encontra o que precisa: o contexto do domínio, os contratos dos serviços vizinhos, as regras, as decisões, as skills e os fluxos. Os arquivos que cada ferramenta lê (AGENTS.md, CLAUDE.md, regras do Cursor, instruções do Copilot) são gerados a partir dela.

**Promessa: quando você senta para codificar, o contexto já está resolvido.**

## 2. Usuários

### 2.1 Jobs To Be Done

- **Arquiteto de solução (principal):** "Quando alguém precisa entender o domínio, quero que o conhecimento já esteja organizado e confiável, para eu deixar de ser a ponte humana e ver minhas decisões respeitadas no código."
- **Tech lead:** "Quando um repo recebe uma tarefa, quero que o agente já conheça os padrões, os vizinhos e as decisões, para não precisar supervisionar cada passo."
- **PM / arquiteto de negócio:** "Quando defino uma funcionalidade, quero que a intenção e as regras de negócio cheguem intactas ao código, sem eu repetir tudo em cada tarefa."
- **Dev (e o agente dele):** "Quando pego uma tarefa, quero abrir o repo e começar, sem caçar documentação nem abrir outros repos."
- **Comprador (head de engenharia / CTO):** "Quero reduzir retrabalho e aumentar a confiança no código gerado por IA, com segurança e evidência de ROI."

### 2.2 Fora do público do MVP

- Times com um único repo e sem dependências entre serviços (o valor do mapa é baixo)
- Sistemas mainframe (V2+)
- Quem quer um chat de perguntas sobre o código: isso é um *context engine*, e o Sinter não é um (ver §5)

### 2.3 Jornadas Principais

`[SUPOSIÇÃO: jornadas ilustrativas, montadas a partir das conversas com o fundador; substituir ou validar com uma sessão real]`

**Personagens:** Rafael (arquiteto de solução, domínio Pagamentos, 34 repos), Carla (PM), Diego (tech lead do `checkout-api`), Bia (dev, usa Claude Code).

- **UJ-1. Rafael vê o domínio Pagamentos inteiro pela primeira vez.**
  Rafael abre o app do Sinter, cria o domínio "Pagamentos", aponta a pasta com os 34 repos e o espaço "PAG" do Confluence, e sobe três PDFs de padrões antigos. O domínio aparece como um **mundo** que gira: cada subdomínio é uma constelação e cada sistema uma estrela, que surgem conforme as fontes são lidas. Ele troca para a visão em **caixas** e vê o **mapa** clássico: sistemas, quem chama quem, filas, donos. Ele clica em `checkout-api` e vê as integrações, cada uma com a origem (arquivo e linha, ou página do Confluence). Duas ligações aparecem como **inferidas**; ele confirma uma e descarta a outra. **Clímax:** pela primeira vez o domínio inteiro cabe em uma tela, e ele confia no que vê porque cada ligação mostra de onde veio. **Caso de borda:** um repo não tem permissão de leitura; o mapa mostra o sistema como "sem acesso", em vez de omiti-lo.

- **UJ-2. Rafael transforma documentação espalhada em padrão.**
  Rafael abre a fila de **curadoria**. O Sinter extraiu 140 itens de conhecimento (regras, padrões, integrações) e agrupou duplicatas. Há 9 **conflitos**: por exemplo, o Confluence diz "timeout de 30 s" e o código usa 10 s. Para cada conflito ele vê as duas fontes lado a lado e escolhe, ou registra uma decisão. Ao aprovar, os itens entram no repo do domínio via PR. **Clímax:** a documentação para de contradizer a si mesma.

- **UJ-3. Carla e Rafael desenham o "parcelamento no checkout".**
  Carla abre uma **conversa guiada** no modo *funcionalidade* e anexa a proposta comercial em PDF e o print da tela nova. O agente facilitador confirma as 3 regras que extraiu dos anexos, já conhece o glossário, as regras de parcelamento e os serviços envolvidos, e pergunta o que falta ("o antifraude precisa saber do número de parcelas?"). Rafael entra no modo *solução*: o agente aponta que a mudança toca `checkout-api`, `payments-gateway` e o evento `PaymentAuthorized`, e alerta que conflita com a ADR-012. O app mostra o **mapa atual e o proposto** lado a lado. Saem um PRD, uma nova ADR e a atualização do contrato do evento, todos aprovados. **Clímax:** a solução nasce já considerando o que o domínio sabe.

- **UJ-4. A tarefa chega pronta para Bia.**
  Da conversa nasce a **tarefa** "Parcelamento no checkout", com um **pacote de contexto**. Rafael adicionou a camada de solução; Diego adiciona a camada do repo ("usar o `InstallmentPolicy` existente, nunca calcular juros no front"). Bia roda `sinter task pull PAG-231` no `checkout-api`, e o pacote entra no `.sinter/`. Ela pede ao Claude Code para implementar; o agente segue as regras, respeita o contrato do evento e não abre outros repos. **Clímax:** o PR sai certo na primeira revisão.

- **UJ-5. Diego cria um serviço novo que já nasce certo.**
  Diego roda `sinter init --domain pagamentos --name refund-service`. O repo nasce com o `.sinter/` pronto (contexto do domínio, vizinhos com que vai falar, padrões da empresa, skills do tech lead e do dev, fluxos "nova feature" e "bugfix") e com os AGENTS.md e demais exports gerados. **Clímax:** o setup que levava dias leva minutos.

## 3. Glossário

- **Sinter** — o produto. Composto pelo **app** (visual) e pela **CLI**.
- **Papel** — função de quem usa o Sinter: PM, Arquiteto, Tech lead, Dev. Uma pessoa pode ter mais de um papel.
- **Domínio** — conjunto de sistemas relacionados por negócio (ex.: Pagamentos). Tem um **repo do domínio** e um **mapa**. Contém de 1 a N **repos**.
- **Subdomínio** — agrupamento de sistemas dentro de um domínio (ex.: Checkout, Autorização). Cada sistema pertence a exatamente um subdomínio.
- **Nível** — grau de zoom do mapa: **Empresa** (todos os domínios), **Domínio** (seus subdomínios e sistemas), **Sistema** (um sistema e seus vizinhos) e **Componente** (o interior de um sistema).
- **Visão** — forma de desenhar o nível Domínio: **Mundo** (globo 3D com subdomínios como constelações), **Grafo** (constelação 2D) ou **Caixas** (subdomínios como caixas com os sistemas dentro). As três mostram os mesmos dados.
- **Repo do domínio** — repositório Git que guarda o conhecimento do domínio no **padrão de documentação**. É a fonte da verdade do Sinter.
- **Repo** — repositório de código de um sistema do domínio. Recebe um **`.sinter/`**.
- **Padrão de documentação** — estrutura fixa do repo do domínio: visão, glossário, mapa, sistemas, integrações, regras, decisões, padrões e fontes.
- **Fonte** — origem de conhecimento conectada a um domínio: repo Git, espaço do Confluence, pasta do Google Docs, arquivo PDF ou DOCX.
- **Item de conhecimento** — unidade do padrão: **sistema**, **integração**, **regra**, **decisão** (ADR), **padrão** ou **termo** do glossário. Sempre tem **proveniência**.
- **Proveniência** — referência à fonte de um item (arquivo e linha, página, trecho) e se ele foi **extraído** (explícito na fonte) ou **inferido**.
- **Mapa** — visão gráfica do domínio: sistemas, integrações e donos.
- **Integração** — relação entre dois sistemas (API, evento, fila, arquivo), com **contrato**, produtor e consumidor.
- **Vizinho** — sistema com integração direta com um repo.
- **Curadoria** — revisão humana de itens propostos: aprovar, editar, descartar ou resolver um **conflito**.
- **Conflito** — dois ou mais itens de conhecimento que dizem coisas diferentes sobre o mesmo assunto.
- **Aprovação** — ato registrado (quem, quando, o quê) que torna um item ou uma camada oficial.
- **Conversa guiada** — sessão com um agente facilitador em um dos três **modos**: processo, funcionalidade ou solução. Parte do repo do domínio e produz itens de conhecimento.
- **Anexo** — documento ou referência adicionado a uma conversa guiada (arquivo, página do Confluence/Google Docs, item do domínio, link). É fonte da conversa; o que dele virar item de conhecimento passa pela curadoria.
- **Tarefa** — unidade de trabalho a implementar (feature ou bug). Tem um **pacote de contexto**.
- **Pacote de contexto** — conjunto de **camadas** anexado a uma tarefa: o que o implementador precisa saber.
- **Camada** — contribuição de um papel ao pacote de contexto (negócio, solução, repo), com dono e aprovação.
- **`.sinter/`** — pasta no repo com o contexto materializado (domínio, vizinhos, regras, decisões, padrões, skills, agentes, fluxos). É o modelo canônico do repo.
- **Export** — arquivo gerado a partir do `.sinter/` para uma ferramenta específica (AGENTS.md, CLAUDE.md, regras do Cursor, instruções do Copilot). Nunca editado à mão.
- **Skill** — capacidade empacotada em SKILL.md (padrão aberto).
- **Agente** — definição de subagente em Markdown, associada a um papel.
- **Fluxo** — roteiro de desenvolvimento em Markdown que orienta humano e agente (MVP: "nova feature" e "bugfix").
- **Catálogo** — coleção de skills, agentes e fluxos disponíveis para instalar em um domínio ou repo.

## 4. Funcionalidades

### 4.1 Domínios e Padrão de Documentação

**Descrição:** o arquiteto cria um domínio no app. O Sinter cria (ou conecta) um repo do domínio já com a estrutura do padrão de documentação. Todo item de conhecimento vive em um único lugar do padrão, tem proveniência e só se torna oficial após aprovação. Realiza UJ-1 e UJ-2.

#### FR-1: Criar domínio
O arquiteto pode criar um domínio informando nome, descrição e o local do repo do domínio (novo ou existente).
- O repo do domínio criado contém todas as seções do padrão de documentação, vazias e com instruções.
- Um repo existente que não siga o padrão é recusado com a lista do que falta. `[SUPOSIÇÃO]`

#### FR-2: Um lugar por item
O sistema classifica cada item de conhecimento em exatamente uma seção do padrão (sistemas, integrações, regras de negócio, decisões, padrões ou glossário).
- Nenhum item aprovado fica fora do padrão.
- Itens que o sistema não consegue classificar vão para a curadoria marcados como "sem seção", e não são aprovados até alguém escolher a seção.
- Dois itens aprovados sobre o mesmo assunto não podem coexistir sem uma decisão registrando qual vale.

#### FR-3: Proveniência obrigatória
Todo item de conhecimento registra a sua proveniência.
- Na interface, cada item mostra a fonte e abre o trecho de origem com um clique.
- Um item sem fonte só pode ser aprovado se o aprovador registrar a justificativa (ex.: "decisão tomada nesta conversa").

#### FR-4: Alterações via Git
Toda alteração aprovada no repo do domínio é gravada como commit, em branch e PR, ou direto no branch principal, conforme configuração do domínio.
- O histórico mostra quem aprovou cada alteração.

### 4.2 Fontes e Ingestão

**Descrição:** o arquiteto conecta fontes a um domínio. O Sinter lê e extrai itens de conhecimento, respeitando as permissões de cada fonte e sem vazar segredos. Realiza UJ-1.

#### FR-5: Conectar repos Git
O arquiteto pode adicionar repos de código ao domínio por caminho local ou URL.
- Repos sem permissão de leitura aparecem como "sem acesso", e não são omitidos.

#### FR-6: Conectar documentos
O arquiteto pode adicionar espaços do Confluence, pastas do Google Docs e arquivos PDF e DOCX.
- Cada documento processado aparece na lista de fontes, com status (processado, erro, sem acesso).

#### FR-7: Respeitar permissões
O sistema só usa conteúdo que o usuário que conectou a fonte tem permissão de ler.
- Conteúdo de uma página sem permissão não aparece em nenhum item, mapa ou export.

#### FR-8: Bloquear segredos
O sistema detecta credenciais e segredos (chaves, tokens, senhas) no conteúdo lido e nunca os grava no repo do domínio, no `.sinter/` ou nos exports.
- Cada segredo detectado gera um alerta na curadoria, com a localização na fonte.

#### FR-9: Reprocessar fontes
O arquiteto pode reprocessar uma fonte ou o domínio inteiro.
- Itens já aprovados não são sobrescritos; mudanças viram novas propostas na curadoria.

### 4.3 Mapa do Domínio

**Descrição:** a visão mais importante do produto. Mostra sistemas, integrações e donos do domínio de forma navegável, e é o momento "uau" do arquiteto. Realiza UJ-1 e UJ-3.

#### FR-10: Gerar o mapa
O sistema gera o mapa do domínio a partir das fontes: sistemas, integrações (API, evento, fila, arquivo) e donos.
- Toda integração mostra a proveniência e se é extraída ou inferida.

#### FR-11: Navegar o mapa
Qualquer papel pode navegar o mapa: zoom, busca, filtro por tipo de integração e foco em um sistema com os seus vizinhos.
- Ao selecionar um sistema, o painel mostra responsabilidade, stack, dono, o que expõe e o que consome.

#### FR-12: Confirmar ou descartar inferências
O arquiteto pode confirmar, corrigir ou descartar integrações inferidas.
- Integrações descartadas não reaparecem no reprocessamento, a menos que a fonte mude.

#### FR-34: Níveis de zoom
Qualquer papel pode navegar entre os níveis Empresa, Domínio, Sistema e Componente, descendo por seleção e subindo pelo caminho de navegação.
- A seleção feita num nível é mantida ao descer.
- `[SUPOSIÇÃO: no MVP o nível Empresa lista os domínios; a visão "universo de mundos" e o nível Componente ficam para a V1]`

#### FR-35: Três visões do domínio
No nível Domínio, o usuário pode alternar entre as visões Mundo, Grafo e Caixas. Realiza UJ-1.
- As três mostram os mesmos sistemas, integrações e status; a seleção atual se mantém ao trocar de visão.
- Os subdomínios usam a mesma cor nas três visões.
- A visão Mundo pode ser girada e para de girar sozinha quando o sistema operacional pede redução de movimento.

#### FR-36: Exportar a visão
O arquiteto pode exportar a visão Caixas e o mapa de um sistema em C4 (formato Structurizr), SVG e Markdown.
- O export em Markdown é o mesmo conteúdo que alimenta `.sinter/context/domain.md`.

#### FR-13: Comparar mapa atual e proposto
Durante uma conversa guiada no modo solução, o sistema mostra o mapa atual e o proposto, destacando sistemas e integrações adicionados, alterados e removidos. Realiza UJ-3.

### 4.4 Curadoria

**Descrição:** fila onde o arquiteto (ou outro papel com permissão) transforma propostas em conhecimento oficial. É o mecanismo anti-lama. Realiza UJ-2.

#### FR-14: Fila de curadoria
O sistema apresenta os itens propostos agrupados por seção do padrão, com duplicatas já agrupadas.
- O usuário pode aprovar, editar, descartar ou aprovar em lote.

#### FR-15: Resolver conflitos
Para cada conflito, o sistema mostra as versões lado a lado, com as fontes.
- O usuário pode escolher uma versão, escrever uma nova ou registrar uma decisão (ADR).
- Um conflito não resolvido impede a aprovação dos itens envolvidos.

#### FR-16: Registro de aprovação
Toda aprovação registra quem aprovou, quando, o quê e com base em qual fonte.

### 4.5 Conversas Guiadas

**Descrição:** agentes facilitadores ajudam os papéis a desenhar processos, funcionalidades ou soluções, partindo do que o domínio já sabe. O resultado volta ao padrão como item de conhecimento. Metodologia compatível com o BMAD Method ("Works with BMad Method"). Realiza UJ-3.

#### FR-17: Iniciar conversa em um modo
Um usuário pode iniciar uma conversa guiada em um domínio, escolhendo o modo: **processo**, **funcionalidade** ou **solução**.

#### FR-18: Conversa ancorada no domínio
O agente facilitador usa o repo do domínio (glossário, mapa, regras, decisões) durante a conversa.
- Quando uma proposta conflita com uma decisão ou regra aprovada, o agente aponta o conflito e cita o item.
- Os termos usados seguem o glossário do domínio; um termo novo é proposto para o glossário.

#### FR-37: Anexos na conversa
Qualquer participante pode anexar à conversa arquivos (PDF, DOCX, Markdown, imagem), páginas do Confluence ou do Google Docs, links da web e itens do domínio (citados com `@`). Realiza UJ-3.
- Cada anexo mostra o seu estado (lendo, lido, falhou, com o motivo da falha).
- Depois de ler um anexo, o facilitador informa o que extraiu dele.
- Anexos são registrados como fontes da conversa; itens de conhecimento extraídos entram na curadoria com proveniência apontando para o anexo.
- Transcrições de reunião como anexo entram na V1 (ver §8.2).

#### FR-19: Saídas estruturadas
Ao final, a conversa gera propostas de itens de conhecimento (regras, decisões, integrações) e, no modo funcionalidade, um PRD e uma ou mais tarefas.
- As propostas entram na curadoria; nada vira oficial sem aprovação.

#### FR-20: Participação de mais de um papel
Uma conversa pode ter participantes de papéis diferentes, em sequência. `[SUPOSIÇÃO: no MVP, participação em sequência, não simultânea]`

### 4.6 Tarefas e Pacote de Contexto

**Descrição:** a tarefa viaja pelos papéis, e cada um adiciona a sua camada. O dev recebe um pacote com só o que é relevante. Realiza UJ-4.

#### FR-21: Criar tarefa
Um usuário pode criar uma tarefa a partir de uma conversa guiada, de um PRD colado ou de um texto livre, associando-a a um domínio.

#### FR-22: Montar o pacote inicial
O sistema monta o pacote de contexto inicial: sistemas afetados, integrações e contratos envolvidos, regras e decisões relevantes.
- Cada elemento do pacote aponta para o item de conhecimento de origem.
- O pacote respeita o limite de tamanho definido na arquitetura (ver §6).

#### FR-23: Adicionar camadas por papel
Cada papel pode adicionar a sua camada ao pacote (negócio, solução, repo) e aprová-la.
- O pacote mostra quais camadas estão presentes, quem é o dono de cada uma e o status.

#### FR-24: Entregar ao repo
O dev pode trazer o pacote de uma tarefa para o repo pela CLI.
- O pacote é gravado no `.sinter/`, e os exports são atualizados.

### 4.7 `.sinter/` e Exports

**Descrição:** o contexto materializado no repo, em arquivos abertos, legíveis por qualquer ferramenta. Funciona mesmo sem o app aberto. Realiza UJ-4 e UJ-5.

#### FR-25: Criar projeto novo com `.sinter/`
O tech lead ou o dev pode criar um repo novo associado a um domínio; o repo nasce com o `.sinter/` completo (contexto do domínio, vizinhos previstos, padrões, skills, agentes e fluxos) e com os exports gerados. Realiza UJ-5.

#### FR-26: Adicionar `.sinter/` a repo existente
O tech lead pode gerar o `.sinter/` para um repo existente do domínio; a entrega é um PR.

#### FR-27: Gerar exports
O sistema gera, a partir do `.sinter/`, os arquivos de cada ferramenta: AGENTS.md (padrão AAIF, com arquivos aninhados quando útil), CLAUDE.md, regras do Cursor e instruções do Copilot.
- A mesma entrada gera sempre a mesma saída.
- Todo export traz no topo o aviso "gerado pelo Sinter, não edite".

#### FR-28: Sincronizar
O dev pode sincronizar o `.sinter/` com o repo do domínio pela CLI.
- Diferenças são mostradas antes de aplicar.
- Edições manuais em exports são detectadas e sinalizadas.

#### FR-29: Contexto disponível, não todo carregado
O `.sinter/` é organizado para que o agente carregue pouco no início e consulte o resto sob demanda: um AGENTS.md curto, skills carregadas quando necessárias e detalhes em arquivos referenciados.
- O AGENTS.md raiz e cada camada do pacote de contexto respeitam os limites do NFR-3; ao ultrapassar, a geração avisa e aponta a camada maior.
- A interface de tarefas mostra o consumo do pacote de contexto contra o orçamento.

### 4.8 CLI do Dev

**Descrição:** a interface do dev e do agente dele. Realiza UJ-4 e UJ-5.

#### FR-30: Comandos essenciais
A CLI oferece, no mínimo: `init` (FR-25), `task pull` (FR-24), `sync` (FR-28), `export` (FR-27) e `status` (o que está desatualizado).
- Todos os comandos funcionam sem o app aberto, desde que o repo do domínio esteja acessível.
- Todos os comandos têm saída legível por máquina (JSON) para uso por agentes.

### 4.9 Catálogo de Skills, Agentes e Fluxos

**Descrição:** versão inicial do marketplace: um catálogo local e privado da empresa, organizado por papel. Realiza UJ-5.

#### FR-31: Navegar e instalar
Um usuário pode navegar o catálogo por papel e tipo e instalar itens em um domínio ou repo.
- Itens instalados em um domínio passam a fazer parte do `.sinter/` dos repos desse domínio.

#### FR-32: Publicar no catálogo da empresa
O arquiteto pode publicar skills, agentes e fluxos no catálogo da empresa.
- Todo item registra autor, versão e licença.

#### FR-33: Fluxos de partida
O catálogo vem com dois fluxos: **nova feature** e **bugfix**. Ambos usam o pacote de contexto da tarefa.

## 5. Não-Objetivos

- **Não é um context engine de perguntas e respostas.** O Sinter prepara o contexto antes da tarefa; não compete com Unblocked, Augment ou Tabnine em busca ao vivo.
- **Não substitui** Confluence, Jira, IDE nem agente de código. Lê deles e entrega para eles.
- **Não gera o código da tarefa.** Quem codifica é o dev ou o agente dele.
- **Não mede desempenho individual de pessoas.** Evita risco ético e regulatório (EU AI Act).
- **Não cria um formato proprietário** para o que o agente lê: usa AGENTS.md, SKILL.md e Markdown.

## 6. Requisitos Não Funcionais

- **NFR-1 Local-first:** no MVP, nenhum dado sai da máquina ou da rede do cliente, exceto chamadas ao provedor de LLM escolhido pelo cliente.
- **NFR-2 Modelo escolhido pelo cliente:** o cliente configura o provedor e o modelo de LLM, incluindo modelos locais.
- **NFR-3 Tamanho do contexto:** o AGENTS.md raiz gerado respeita um limite de tamanho, e cada camada do pacote de contexto tem orçamento próprio. `[SUPOSIÇÃO: limites definidos na arquitetura; referência inicial no addendum]`
- **NFR-4 Portabilidade:** o `.sinter/` e os exports funcionam sem o Sinter instalado; qualquer agente compatível com os padrões abertos os lê.
- **NFR-5 Determinismo:** a geração de exports é reprodutível (mesma entrada, mesma saída).
- **NFR-6 Escala do MVP:** um domínio com até 50 repos e 500 documentos é processado e tem o mapa inicial em menos de 30 minutos numa máquina de desenvolvedor comum. `[SUPOSIÇÃO]`
- **NFR-7 Rastreabilidade:** 100% dos itens aprovados têm proveniência ou justificativa registrada.
- **NFR-8 Segurança:** nenhum segredo detectado aparece em repo do domínio, `.sinter/` ou export.
- **NFR-9 Idioma:** interface em português e inglês; o conteúdo segue o idioma das fontes.
- **NFR-10 Usabilidade visual:** o mapa permanece legível e navegável com 50 sistemas; um arquiteto novo cria um domínio e vê o mapa sem ajuda.

## 7. Restrições e Salvaguardas

- **Propriedade intelectual:** o Sinter não pode ser desenvolvido nem testado com código, documentos ou reuniões da empregadora do fundador. Pilotos só com repos open source, sintéticos ou de *design partners* sob acordo formal.
- **Privacidade:** o MVP não processa transcrições de reunião, que são a fonte de maior risco de LGPD. Quando entrarem (V1), exigirão aviso aos participantes e minimização (guardar a decisão, não quem disse o quê).
- **Marca:** usar "Sinter"; nunca usar "BMad" no nome ou no marketing, apenas "Works with BMad Method".
- **Licenças:** componentes de terceiros devem ter licença compatível com uso comercial, registrada no catálogo e no repositório.

## 8. Escopo do MVP

### 8.1 Dentro
- App visual rodando local + CLI (duas superfícies)
- Domínios, repo do domínio e padrão de documentação opinativo (FR-1 a FR-4)
- Fontes: repos Git, Confluence, Google Docs, PDF e DOCX (FR-5 a FR-9)
- Mapa, com comparação entre atual e proposto, níveis de zoom, três visões (Mundo, Grafo, Caixas) e exportação (FR-10 a FR-13, FR-34 a FR-36)
- Curadoria com conflitos e aprovação (FR-14 a FR-16)
- Conversas guiadas nos três modos, com anexos (FR-17 a FR-20, FR-37)
- Tarefas e pacote de contexto por camadas (FR-21 a FR-24)
- `.sinter/`, exports e CLI (FR-25 a FR-30)
- Catálogo local com fluxos de partida (FR-31 a FR-33)

### 8.2 Fora do MVP
- **Transcrição de reunião → decisões** (V1): maior risco de LGPD; entra com consentimento e minimização.
- **Atualização automática do `.sinter/` quando as fontes mudam** (V1): no MVP, `status` e `sync` são manuais.
- **Revisão de PR contra decisões e contratos, e boas práticas como checagens automáticas** (V2).
- **Mainframe** (V2+).
- **SaaS multi-empresa, SSO, cobrança e marketplace público.**
- **Jira, Slack e Notion como fontes.** No MVP, a tarefa vive só no Sinter.
- **Visão "universo de mundos" no nível Empresa e o nível Componente** (V1).
- **Tema claro e uso em telas menores que 1280 px.**

## 9. Métricas de Sucesso

`[SUPOSIÇÃO: linhas de base estimadas; medir no primeiro piloto antes de usar o Sinter]`

**Primárias**
- **SM-1 Acerto na 1ª tentativa:** % de tarefas implementadas por agente cujo PR é aprovado sem correção por falta de contexto (regra, padrão, contrato ou decisão ignorados). Medição: no review, o tech lead marca se houve correção por falta de contexto; comparar 20 tarefas antes e 20 depois do Sinter no piloto. Linha de base estimada: 60%. Meta: ≥ 80%. Valida FR-22 a FR-29.
- **SM-2 Tempo de preparo de contexto por tarefa:** tempo entre a tarefa estar definida e o dev começar a implementar. Medição: registro do dev nas mesmas 20 + 20 tarefas; no Sinter, tempo entre a aprovação da última camada e o `task pull`. Linha de base estimada: 30 a 60 min. Meta: ≤ 10 min. Valida FR-21 a FR-24.

**Secundárias**
- **SM-3 Setup de projeto novo:** tempo até um repo novo estar pronto para o agente trabalhar. Linha de base estimada: 1 a 2 dias. Meta: < 1 hora. Valida FR-25 e FR-27.
- **SM-4 Cobertura do domínio:** % dos repos do domínio piloto com `.sinter/` aprovado e % de vizinhos com contrato documentado. Meta: ≥ 80% em 4 semanas de piloto. Valida FR-10, FR-26.
- **SM-5 Tempo até o primeiro mapa:** de criar o domínio até o mapa navegável. Meta: < 1 dia de trabalho do arquiteto. Valida FR-1 a FR-11.
- **SM-6 Conflitos resolvidos:** % de conflitos detectados que foram resolvidos na curadoria. Valida FR-15.

**Contra-métricas (não otimizar)**
- **SM-C1 Volume do contexto:** mais contexto não é melhor; um `.sinter/` crescendo sem limite piora o agente. Contrabalança SM-4.
- **SM-C2 Quantidade de itens de conhecimento:** não medir sucesso pelo número de itens. Contrabalança SM-6.
- **SM-C3 Velocidade de aprovação:** aprovar rápido demais indica curadoria de fachada. Contrabalança SM-5.

## 10. Questões em Aberto

1. **Sessão real:** qual foi uma feature recente em que o contexto se perdeu, e onde? Substitui ou valida UJ-1 a UJ-5.
2. **Linhas de base reais** de SM-1 a SM-3: medir no piloto.
3. **Design partners:** quais empresas, com que acordo de PI e dados?
4. **Motor do grafo:** o Graphify (ou alternativa) identifica bem integrações entre serviços (HTTP, eventos, filas)? Testar na arquitetura.
5. **Permissões no app:** `[SUPOSIÇÃO adotada para o MVP]` o arquiteto aprova itens de conhecimento e a camada de solução; cada papel aprova só a própria camada. Revisar com os design partners.
6. **Onde a tarefa vive:** decidido para o MVP: só no Sinter (ver §8.2). Espelhar no Jira volta à pauta na V1.
7. **Checagem de marca:** "Sinter" no INPI, USPTO e EUIPO, e disponibilidade de domínio.
8. **Modelo de preço** para a compra corporativa (por usuário, por domínio, por repo).

## 11. Índice de Suposições

- §2.3 — UJ-1 a UJ-5 são ilustrativas; validar com uma sessão real.
- FR-1 — repo do domínio existente fora do padrão é recusado (alternativa: migração assistida).
- FR-20 — conversas com vários papéis em sequência, não simultâneas.
- FR-34 — nível Empresa só lista domínios no MVP; universo de mundos e nível Componente na V1.
- §10.5 — regras de permissão de aprovação no MVP.
- NFR-3 — limites de tamanho do contexto definidos na arquitetura.
- NFR-6 — escala e tempo de processamento do MVP.
- §9 — linhas de base e metas das métricas são estimativas.
