---
title: "PRD — Sinter: Catálogo, passo 1 (Domínio)"
status: draft
created: 2026-10-17
updated: 2026-10-17
inputs:
  - ../../prd-yaml.md
  - ../../_bmad-output/planning-artifacts/architecture/architecture-harness_corp-2026-09-26/ARCHITECTURE-SPINE.md
  - ../../_bmad-output/planning-artifacts/prds/prd-harness_corp-2026-09-26/prd.md
  - ../../Exemplo.drawio.xml
references:
  - exemplo-catalogo/
  - addendum.md
---

# PRD: Sinter — Catálogo, passo 1 (Domínio)

## 0. Propósito do documento

Este PRD cobre **só o primeiro passo** do catálogo de contexto do Sinter: a **estrutura do domínio**. Define quais níveis existem, o que cada nível precisa conter para que **uma IA entenda o que acontece no domínio**, e como uma pessoa cria, navega e valida essa estrutura.

Os passos seguintes (importar a saída da `sinter-documentar`, impacto, score, skills, contexto de tarefa, operação multiusuário, site) têm PRDs ou histórias próprios.

O exemplo (um arquivo por item, como no catálogo real) de tudo o que este PRD descreve está em [exemplo-catalogo/](exemplo-catalogo/README.md). Detalhes de implementação (pastas, nomes de campos, ajustes na espinha) ficam no [addendum](addendum.md).

## 1. Problema

Uma IA que recebe um repo, ou mesmo uma pasta de documentos, **não sabe**:

- para que o domínio existe e onde ele termina (o que **não** é dele);
- em que ordem as coisas acontecem e o que acontece quando um passo falha;
- o que é legado, o que é novo e para onde a modernização está indo;
- quais regulações, decisões e documentos de negócio valem para aquela parte;
- o que ainda **ninguém sabe**, e por isso ela não deve inventar.

Sem uma estrutura que responda isso, a IA chuta: inventa integração, ignora regra, trata ata de reunião como lei e não diferencia o batch do mainframe do microserviço que vai substituí-lo.

## 2. Para quem

**Quem cria e mantém:** o arquiteto de solução (ou o tech lead) que já trabalha com um agente de código (Claude Code, Cursor, Copilot).

**Quem consome:** o agente de código, e qualquer pessoa que precise entender o domínio, navegando do geral para o detalhe.

### 2.1 Jornada principal

`[ASSUMPTION: jornada montada a partir desta conversa; validar com uma sessão real]`

**UJ-1. Rafael modela o domínio Pagamentos (Varejo).**
Rafael roda `sinter catalog init` e depois `sinter domain new`, informando o id-domínio `PAGV`, o nome, a área e o propósito em uma frase. Ele cadastra os três subdomínios (Checkout, Autorização, Conciliação), descreve as aplicações de cada subdomínio e os repos que compõem cada uma (incluindo o do mainframe), marca o batch `CONC0100` como `modernizing` e escreve o objetivo "desligar o batch até dez/2027". Liga a LGPD ao domínio e a regulação de arranjos de pagamento só à Conciliação. Descreve a jornada "Pagar um pedido" em etapas, com o que acontece quando o antifraude nega. Roda `sinter validate`: um passo aponta para um subdomínio com o nome errado, ele corrige. Então pede ao agente: "explica o domínio PAGV". O agente roda `sinter get dom-pagv --level 1`, responde certo o que o domínio faz e não faz, que existe um legado sendo substituído e quais regulações valem, e só abre a Conciliação quando Rafael pergunta do batch.
**Clímax:** a IA explica o domínio sem inventar nada, e diz "isso ninguém sabe ainda" onde há pendência.

## 3. Glossário

- **Catálogo:** repo Git onde vive o conhecimento estruturado da organização; cada domínio é uma pasta.
- **Organização:** raiz do catálogo. Guarda as listas que valem para todos (áreas, regulações, padrões).
- **Área:** **agrupador** de domínios (ex.: varejo, atacado, câmbio): é a porta de entrada para achar um grupo de domínios. Tem id, nome e uma frase de descrição, vem de uma lista fechada da organização e **não** é nível da hierarquia (não tem arquivo próprio nem herança), para poder virar nível no futuro sem quebrar nada.
- **Domínio:** conjunto de capacidades de negócio relacionadas (ex.: Pagamentos). Identificado pelo **id-domínio**.
- **id-domínio:** identificador curto do domínio (a antiga "sigla"), informado por quem cria. Desambigua domínios de mesmo nome em áreas diferentes (`PAGV` × `PAGA`).
- **Subdomínio:** capacidade de negócio dentro do domínio (ex.: Checkout, Boletagem). É a "caixinha" de uma jornada.
- **Aplicação:** o que implementa um subdomínio. Agrupa os **N repos** que a compõem (front, BFF, API, batch…), cada um com seu papel e plataforma. Mora **dentro** do arquivo do subdomínio. Tem estado de vida.
- **Estado de vida (lifecycle):** `legacy`, `modernizing`, `modern` ou `retired`. Vive **só** na aplicação.
- **Jornada:** sequência de passos, organizada em etapas, que cumpre um objetivo de negócio. Cada passo aponta para um subdomínio (ou para um externo).
- **Dado (data asset):** conjunto de dados que um subdomínio produz (ex.: posição de câmbio), descrito por **camada** (ex.: raw, trusted, refined — os nomes são os da empresa), com onde fica, formato, atualização, qualidade esperada e quem consome.
- **Doc:** um documento ligado a um nível: um `.md` na pasta `docs/` do domínio **ou** um link (wiki, Confluence, arquivo dentro de um repo). Tipos: negócio, ata, pauta (agenda de reunião), runbook, arquitetura, gerado, link.
- **Conhecimento ligado:** docs, regulações, padrões e decisões associados a um nível. O que é ligado ao domínio vale para todos os seus subdomínios (herança).
- **Pendência ("não sabemos"):** pergunta aberta registrada num nível. Sinal explícito para a IA não inventar.

## 4. A estrutura

```text
Organização                  (áreas, camadas de dados, vocabulário, regulações, padrões, repos)
  └── Domínio                (id-domínio, área, propósito, faz/não faz/não sabemos,
       │                      regras do domínio todo, fronteiras, modernização, conhecimento)
       ├── Subdomínio         (os mesmos blocos do domínio, só o que é dele)
       │    ├── Aplicação     (lifecycle, N repos com papel, plataforma e docs)
       │    └── Dado          (camadas raw/trusted/refined…, qualidade, consumidores)
       ├── Jornada            (etapas → passos → subdomínio, falhas, regras, regulação)
       ├── (regras e decisões ficam DENTRO do domínio/subdomínio, como listas)
       └── docs/              (os .md citados pelos campos docs: de cada nível; o resto é link)
```

O formato exato de cada arquivo está no **[Apêndice A](#apêndice-a--esqueleto-dos-arquivos)**.

**Princípio 1 — cada fato num lugar só.** O subdomínio guarda as suas aplicações; cada aplicação diz se é legado e quais repos a compõem. Toda visão que junta isso (ex.: "quantos legados há no domínio", "quais repos o domínio tem") é **calculada**, nunca escrita. **Exceção consciente:** uma lista que serve de **sumário** para quem lê o arquivo (os subdomínios no domínio) pode repetir uma ligação, desde que o `validate` garanta que os dois lados batem.

**Princípio 2 — do geral para o detalhe.** Cada nível responde às perguntas que a IA faz ao chegar nele, de forma curta. O detalhe fica um nível abaixo ou num documento, e só é aberto quando necessário.

**Princípio 3 — estrutura em YAML, narrativa em Markdown.** O YAML é curto e validável; o Markdown explica o porquê. Markdown nunca declara estrutura.

## 5. Funcionalidades

### 5.1 Catálogo e organização

#### FR-1: Iniciar o catálogo
A pessoa cria um catálogo vazio com a estrutura de pastas e a configuração da organização.
- O catálogo nasce com a lista de áreas vazia, a lista de repos vazia e um `schemaVersion`.
- Rodar de novo num catálogo existente não altera nada e avisa.

#### FR-2: Manter as listas da organização
A pessoa mantém as listas que valem para todos os domínios: **áreas**, **repos** (id + endereço), **regulações** e **padrões**.
- Uma regulação tem nome, jurisdição e vigência (início e fim opcional) e pode substituir outra.
- Um repo pode ser citado por mais de um domínio.

### 5.2 Domínio

#### FR-3: Criar domínio
A pessoa cria um domínio informando **id-domínio**, nome, área e propósito (uma frase).
- O id-domínio é obrigatório, único no catálogo e segue um formato curto (letras maiúsculas e números, 2 a 8 caracteres) `[ASSUMPTION: formato]`.
- A área tem que existir na lista da organização.
- O mesmo nome de domínio pode existir em áreas diferentes; o id-domínio não pode se repetir.

#### FR-4: Descrever o domínio para a IA
O domínio guarda, além da identidade:
- **Faz** (3 a 5 itens), **Não faz** (o que se acha que ele faz, mas não faz, com quem faz) e **Não sabemos** (pendências).
- **Regras:** frases curtas, **dentro do próprio arquivo** (cada uma com id, para jornadas citarem). No domínio, só as que valem para todos os subdomínios (herdadas por eles); as de uma parte ficam no subdomínio. A explicação longa de uma regra vai para a página `.md` do nível.
- **Jornadas principais.**
- **Fronteiras:** o que entra e o que sai, e de/para qual domínio ou externo. No domínio elas são **calculadas** a partir das fronteiras dos subdomínios que apontam para fora dele (nenhum vizinho fica esquecido); quem escreve fronteira é o subdomínio.
- **Donos.**
- **Repos compartilhados:** só repos que não pertencem a nenhuma aplicação (bibliotecas, infraestrutura) `[ASSUMPTION]`. Os demais repos do domínio são calculados a partir das aplicações (FR-8).

Critérios:
- Um domínio sem propósito não é aceito.
- Faz, Não faz e Não sabemos podem estar vazios, mas a resposta da CLI mostra quando estão vazios (a IA sabe que não foi preenchido, em vez de supor que "não há nada").

#### FR-5: Intenção de modernização
Domínio e subdomínio podem registrar o **objetivo de modernização** (uma frase) e a decisão que o sustenta.
- O panorama (quantas aplicações legadas, modernizando, modernas e desligadas) **não é escrito**: é calculado a partir das aplicações.

#### FR-6: Conhecimento ligado ao nível
Domínio, subdomínio, jornada, aplicação, **cada repo de uma aplicação** e regulação podem ter conhecimento ligado:
- **Regulações, padrões e decisões** (só em domínio, subdomínio e jornada): citados pelo id (são itens com vida própria, que valem para vários lugares).
- **Docs** (em todos esses níveis): lista no próprio nível. Os **tipos** de doc vêm de uma lista da organização (7 padrão — negócio, ata, pauta, runbook, arquitetura, gerado, link — e a empresa acrescenta os seus). Cada doc tem título, tipo e **ou** um caminho para um arquivo em `docs/` (normalmente `.md`; pode ser um desenho, um PDF) **ou** um link; opcionalmente id, data e data da última verificação.
- Um doc já citado em outro nível é reaproveitado pelo id, sem repetir.
- No repo, os docs são links que apontam para dentro dele (README, contrato, pasta de JCL).
- **Herança:** o que está ligado ao domínio vale para todos os seus subdomínios, sem precisar repetir `[ASSUMPTION: sem exceções nesta história]`.
- Na consulta, o conhecimento herdado aparece marcado como herdado.

#### FR-20: Glossário
Organização, domínio e subdomínio podem ter **glossário**: termo, definição curta, sinônimos e "não confundir com".
- **Organização:** jargão da empresa inteira (ex.: D0, PF/PJ, "sigla"). **Domínio:** termos do negócio do domínio (ex.: boleta, spread). **Subdomínio:** termos que só fazem sentido naquela parte (ex.: natureza da operação).
- O termo é definido **uma vez**, no nível mais alto em que tem um significado só; na consulta, o glossário de um nível soma os termos herdados, marcados.
- Na mesma linha de herança (organização → domínio → subdomínio), **redefinir** um termo é erro.
- Em domínios diferentes, o mesmo termo pode ter significados diferentes (ex.: "conta" em Contas e em Contabilidade).

#### FR-21: Operação (opcional)
Domínio e subdomínio podem dizer **quando e quanto** funcionam, para a IA saber o que é urgente: horário de funcionamento, janelas de batch, criticidade e volume.
- Tudo é opcional e descritivo; o subdomínio herda do domínio o que não declarar.

### 5.3 Subdomínio

#### FR-7: Criar subdomínio
A pessoa cria um subdomínio dentro de um domínio, com nome e propósito (uma frase). O subdomínio tem **os mesmos blocos do domínio**, exceto id-domínio, área e a configuração do Sinter: faz, não faz e não sabemos, donos, aplicações, dados, regras, fronteiras, modernização, regulações, padrões, decisões e docs.
- O subdomínio diz a que domínio pertence, e o domínio traz a **lista de subdomínios como sumário**, na ordem em que faz sentido ler. Os dois lados têm que bater (o `validate` confere) e, ao criar um subdomínio pela CLI, o rascunho já inclui o domínio com a lista atualizada.
- As jornadas que passam por um subdomínio são **calculadas** a partir dos passos.
- Tudo o que o domínio declara vale para o subdomínio (herança); o subdomínio declara só o que é **dele** e, na consulta, os dois aparecem somados, com o herdado marcado.

#### FR-8: Aplicações do subdomínio
O subdomínio descreve, **dentro do próprio arquivo**, as aplicações que o implementam. Cada aplicação tem id, nome, **lifecycle**, apelidos (ex.: `CONC0100`) e a lista dos **repos** que a compõem, cada um com papel (frontend, BFF, API, batch, lib) e plataforma (ex.: react, java, mainframe), e opcionalmente o caminho dentro do repo.
- O id da aplicação é único no catálogo, para que jornadas e relações possam citá-la.
- O lifecycle é obrigatório e é o único lugar onde se diz se a aplicação é legado.
- Um repo pode compor mais de uma aplicação (ex.: o repo do mainframe).
- Uma aplicação usada por outro subdomínio é citada pelo id, sem ser repetida (sem regra especial nesta história).

#### FR-19: Dados do subdomínio
O subdomínio (e, se fizer sentido, o domínio) descreve os **dados** que produz: nome, descrição, aplicação que produz, se tem dado pessoal, e cada **camada** pela qual o dado passa.
- As camadas e seus nomes vêm de uma lista da organização (ex.: raw → trusted → refined, ou bronze → silver → gold), na ordem do fluxo.
- Em cada camada: onde fica (caminho ou tabela), formato, frequência de atualização, regras de qualidade esperadas e quem consome.
- Dado com dado pessoal aparece marcado na consulta (para a IA tratar com cuidado).
- Um dado pode ter docs (dicionário de dados, contrato).

### 5.4 Aplicação

#### FR-9: (incorporado ao FR-8)
As aplicações são cadastradas dentro do subdomínio (FR-8).

#### FR-10: Substituição de legado
A pessoa registra que uma aplicação é **substituída por** outra, com fase (`planned`, `in-progress`, `done`) e a evidência (de onde veio essa informação).

### 5.5 Jornada

#### FR-11: Descrever jornada
A pessoa descreve uma jornada com propósito, gatilho (o que a inicia), resultado esperado e pendências.
- A jornada pode ser **variante** de outra (ex.: PF e PJ).

#### FR-12: Etapas e passos
A jornada é organizada em **etapas** (ex.: Cotar, Contratar); cada etapa pode ter um canal de entrada (micro-front, BFF) e uma lista de **passos**.
- Cada passo aponta para um **subdomínio** (a parte do domínio que faz o passo) e, se for o caso, para o **externo ou outro domínio** que ele chama (ex.: SWIFT, Bacen, Risco). Um passo que é só do externo não tem subdomínio.
- Cada passo pode ter: ação, resultado, regras, regulação, evento publicado, job (para batch) e **o que acontece se falhar**.
- Passos formam um pequeno grafo: um passo indica os próximos (`next`) e pode correr em paralelo com outros.
- Jornada de legado batch usa o mesmo formato, com a agenda como quem dispara cada passo.

Critérios:
- Todo `next` aponta para um passo da mesma jornada; todo subdomínio citado existe.
- A consulta da jornada devolve a sequência de etapas e passos, em ordem, com os desvios de falha; ninguém mantém um diagrama à mão. O desenho visual fica para o site (fora desta história).

#### FR-13: Do passo ao detalhe
A partir de um passo, a pessoa (ou a IA) chega ao subdomínio, dele às aplicações, e delas aos repos e aos documentos, um nível por vez.

### 5.6 Documentos

#### FR-14: Documentos do domínio
Os `.md` citados pelos níveis ficam na pasta `docs/` do domínio, organizados como a pessoa preferir (por tipo ou por subdomínio).
- **Pautas** (agendas de reunião) e **atas** são tipos próprios: a pauta diz o que vai ser discutido; a ata, o que foi decidido.
- Uma ata pode ser **promovida** a decisão: cria-se uma Decisão cuja evidência aponta para o doc da ata.
- Classificação de acesso fica para quando houver controle de acesso (fora desta história).

### 5.7 Navegar e validar

#### FR-15: Consultar por nível
A pessoa e o agente consultam qualquer item em níveis de detalhe crescentes:
- **Nível 0:** id, nome, tipo, propósito, contagens.
- **Nível 1:** + faz/não faz/não sabemos, filhos (subdomínios, aplicações, repos calculados), panorama de modernização, conhecimento (próprio e herdado, marcado), jornadas.
- **Nível 2:** + vizinhança (jornadas e passos que passam pelo item, aplicações substituídas/substitutas).
- Toda resposta tem versão legível por máquina (JSON) e diz o que foi omitido e como pedir.

#### FR-16: Ler documento por seção
A pessoa e o agente leem só uma seção de um documento (por âncora), sem carregar o documento inteiro.

#### FR-17: Validar o catálogo
`sinter validate` confere todo o catálogo e lista cada erro com arquivo e motivo:
- formato e campos obrigatórios de cada item;
- unicidade de ids e do id-domínio;
- hierarquia sem ciclo (organização → domínio → subdomínio);
- a lista de subdomínios do domínio bate com os subdomínios que dizem pertencer a ele (nenhum faltando, nenhum sobrando);
- nenhum termo do glossário é redefinido na mesma linha de herança;
- **aviso** quando um subdomínio repete algo que já herda do domínio (regulação, padrão, decisão, regra), porque a repetição não acrescenta nada;
- toda referência **interna** existe (subdomínio, aplicação, dado, repo, regra, regulação, padrão, decisão, jornada, doc reaproveitado por id, passo `next`);
- referência a **outro domínio** (`dom-`) que não está no catálogo gera **aviso**, não erro (o catálogo cresce aos poucos);
- referências a coisas que não têm arquivo (`ext-` externos, `evt-` eventos, `agenda-` agendadores) só têm o formato conferido;
- todo doc tem caminho **ou** link, e todo caminho aponta para um arquivo que existe;
- área existe na lista da organização.

### 5.8 Como a estrutura é escrita

#### FR-18: Um único caminho para criar e alterar
Toda criação ou alteração no catálogo passa por **um** caminho: um **rascunho** (um ou mais arquivos no formato do Apêndice A) é **conferido** e, se a pessoa confirmar, **gravado**.
- O rascunho pode vir de três lugares: gerado pela CLI a partir do esqueleto (com os campos obrigatórios marcados), escrito ou editado à mão, ou montado pela IA numa conversa (skill, em história própria).
- Antes de gravar, a pessoa vê **um resumo em linguagem natural** do que vai mudar ("cria o subdomínio Boletagem, legado, com a aplicação BOL0100…") e a lista de erros, se houver; conferir não grava nada.
- O rascunho traz o **item inteiro** (não um pedaço): gravar substitui o arquivo daquele item. Para acrescentar uma aplicação ou um doc, o rascunho é o subdomínio completo já com o acréscimo.
- Ao gravar, cada item vai para o seu lugar no catálogo (tabela abaixo) e a mudança vira um registro identificado (quem, quando, o quê) `[ASSUMPTION: nesta história, quem grava aprova no mesmo passo]`.
- Um rascunho com erro não é gravado, nem em parte.
- Por convenção, quem edita um arquivo do catálogo à mão passa a edição pelo mesmo caminho; nesta história nada impede tecnicamente o contrário (a checagem automática no remote é do passo 8).

| Tipo | Onde é gravado |
|---|---|
| Organization | `organization.yaml` |
| RepositoryList | `repositories.yaml` |
| Regulation · Standard | `regulations/<id>.yaml` · `standards/<id>.yaml` |
| Domain | `domains/<id-domínio>/domain.yaml` |
| Subdomain · Journey · Relation | `domains/<id-domínio>/{subdomains,journeys,relations}/<id>.yaml` |

### 5.9 Buscar e estruturar com a IA

#### FR-22: Buscar no catálogo
A pessoa e o agente acham um item sem saber o id.
- `find <texto>` procura em nome, id-domínio, apelidos de aplicação, termos e sinônimos do glossário, propósito e repo, e devolve os ids encontrados em ordem de relevância, cada um no nível 0 e com o campo onde casou.
- `list domains` lista os domínios (id-domínio, nome, área, propósito), com filtro por área.
- A busca ignora maiúsculas e acentos ("cambio" acha "Câmbio").

#### FR-25: Navegar por área
A área direciona para um grupo de domínios: é o primeiro passo de quem chega ao catálogo sem saber o domínio.
- `list areas` lista as áreas com nome, descrição e quantos domínios cada uma tem.
- `get area-<slug>` devolve a área e os seus domínios no nível 0 (lista **calculada** a partir do `metadata.area` dos domínios, nunca escrita).
- `find` também casa no nome da área (ex.: `find cambio` traz a área Câmbio e os domínios dela).
- A consulta da organização (`get org-<slug> --level 1`) mostra os domínios agrupados por área.

#### FR-23: Editar a partir do atual
A pessoa e o agente pegam o YAML atual de um item como rascunho (`get <id> --raw`), alteram e devolvem pelo caminho único (FR-18). Criar e editar usam o mesmo fluxo.

#### FR-24: Skills de buscar e de estruturar
Duas skills no agente de código, por cima da CLI (só chamam a CLI com `--json`):
- **`/sinter-find`** (só lê): acha o item com `find` e explica com `get`, abrindo mais níveis só quando perguntado.
- **`/sinter-domain`** (escreve): **sempre busca antes de criar**. Se o domínio existe, oferece estruturá-lo (acrescentar subdomínio, aplicação, jornada…); se não existe, pede só o obrigatório e monta o rascunho. Toda gravação passa por `apply --dry-run`, mostra o resumo, pede confirmação e só então grava.
- **O preenchimento é uma conversa guiada:** a skill pergunta nível a nível, do geral para o detalhe, uma pergunta por vez, em linguagem de negócio, com exemplo da resposta esperada e com opções quando o catálogo tem a lista (área, lifecycle, regulações, subdomínios…). Resposta vaga gera pergunta de seguimento; "não sei" vira pendência (não sabemos), nunca valor inventado; sugestões só entram se aceitas; cada bloco termina com um resumo para confirmar. Dá para parar e retomar pelas lacunas.
- Nesta história as skills montam o rascunho perguntando; ler fontes (repos, desenhos) para rascunhar fica para o passo 3.

## 6. Fora do escopo desta história

- Importar a saída da `sinter-documentar` ou de outra skill (passo 3).
- Relações técnicas gerais entre aplicações (chama, consome, publica) além de "substituído por" (passo 2).
- Análise de impacto (passo 4) e cálculo de score de confiabilidade e relevância (passo 5). Os campos que alimentam o score já são guardados (tipo, data de verificação).
- Outras skills `sinter-*` além de `/sinter-find` e `/sinter-domain` (passo 6), e skills que leem fontes para rascunhar (passo 3).
- Contexto de tarefa e `.sinter/` nos repos (passo 7).
- Várias pessoas aprovando ao mesmo tempo, push e checagem no remote (passo 8).
- Site estático e app visual.
- Exceções de herança, área como nível, integração do id-domínio com cadastro oficial.

## 7. Requisitos não funcionais

- **NFR-1 Compacto para a IA:** o nível 0 de um domínio cabe em até ~300 tokens e o nível 1 em até ~2.000 tokens para um domínio com 10 subdomínios e 40 aplicações `[ASSUMPTION]`.
- **NFR-2 Determinístico:** a mesma versão do catálogo gera sempre a mesma resposta, byte a byte, na mesma ordem.
- **NFR-3 Rápido:** `validate` de um catálogo com 500 itens termina em até 3 segundos numa máquina comum `[ASSUMPTION]`.
- **NFR-4 Legível por humano:** todo arquivo pode ser lido e revisado num PR sem ferramenta especial.
- **NFR-5 Local:** funciona sem rede e sem chamar nenhum modelo de IA.
- **NFR-6 Versionado:** o formato tem versão; uma CLI mais velha recusa um catálogo de formato mais novo.

## 8. Métricas de sucesso

`[ASSUMPTION: medir com o próprio Gui e o exemplo PAGV + Câmbio antes de qualquer piloto]`

- **SM-1 Cobertura do modelo:** os dois domínios do exemplo (PAGV e CAMB) passam no `validate` com **zero erros e zero campos desconhecidos**, e cada tipo do Apêndice A tem ao menos um exemplo. Meta: 100%.
- **SM-2 A IA entende:** um agente que recebe só a saída de `sinter get --level 1` (e pode pedir mais níveis) acerta o questionário de [avaliacao-ia.md](avaliacao-ia.md) (10 perguntas com gabarito sobre o PAGV). Cada rodada é feita 3 vezes com o agente e o modelo do dia a dia do Gui, registrando o modelo usado. Meta: ≥ 9/10 na média, e **zero** respostas inventadas onde há pendência. Base de comparação: o mesmo agente recebendo o mesmo conhecimento em texto corrido (os `.md` sem a estrutura).
- **SM-3 Tempo de modelagem:** tempo para modelar um domínio de tamanho médio (3 subdomínios, 7 aplicações, 2 jornadas). Meta: < 2 horas.

**Contra-métricas (não otimizar):**
- **SM-C1 Quantidade de campos preenchidos:** encher campo não é entender; um domínio com tudo preenchido e propósito vago falha no SM-2.
- **SM-C2 Tamanho do nível 1:** crescer o nível 1 para "ajudar" a IA quebra a divulgação progressiva (NFR-1).

## 9. Questões em aberto

Resolvidas nesta história (registradas no memlog):
- ~~Chaves em inglês ou português~~ → chaves em inglês, valores no idioma da empresa.
- ~~Herança com exceção~~ → **sem exceção**: o que não vale para todos desce para os subdomínios onde vale.
- ~~Modernização por aplicação~~ → o `modernized_by` na aplicação basta; o objetivo fica no domínio/subdomínio.
- ~~Quem aprova~~ → quem grava aprova (passo 1); revisão por outra pessoa no passo 8 (PR).
- ~~Tipos de doc~~ → lista **aberta**, definida pela empresa (`organization.docTypes`), com 7 padrão.
- ~~Bloco de operação~~ → entra como opcional (FR-21).

Em aberto (não bloqueiam a implementação):
1. **O que trafega em cada passo da jornada** (`carries`): fica para o passo de relações técnicas.

## 10. Índice de suposições

- §2.1 — UJ-1 ilustrativa.
- FR-3 — formato do id-domínio.
- FR-4 — repos compartilhados só para o que não pertence a aplicação.
- FR-6 — herança sem exceções.
- FR-19 — dados também podem ser declarados no domínio.
- FR-18 — quem grava aprova no mesmo passo.
- NFR-1, NFR-3 — limites de tamanho e tempo.
- §8 — metas e forma de medir.

## Apêndice A — Esqueleto dos arquivos

O contrato de cada arquivo do catálogo. Legenda nos comentários: **`(obr)`** obrigatório, **`(opc)`** opcional, **`(calc)`** nunca escrito, a CLI calcula. Todo arquivo segue o mesmo envelope:

```yaml
apiVersion: sinter.dev/v1     # (obr) versão do formato
kind: <Tipo>                  # (obr) Organization | RepositoryList | Regulation | Standard | Domain | Subdomain | Journey | Relation
metadata:
  id: <prefixo>-<slug>        # (obr) único no catálogo, nunca muda
  name: <texto>               # (obr)
  status: approved            # (obr) candidate | approved | rejected | deprecated | superseded
  owners: [<pessoa|time>]     # (opc)
spec: { ... }                 # (obr) varia por tipo, abaixo
```

Blocos que se repetem (definidos uma vez, usados em vários tipos):

```yaml
# DOC — item de qualquer lista docs:
- id: doc-<slug>              # (opc) só se for reaproveitado em outro nível
  title: <texto>              # (obr)
  type: negocio               # (obr) um dos tipos de organization.docTypes
  path: docs/<...>            # (obr: path OU url) arquivo na pasta docs/ do domínio (em geral .md)
  url: <https://...>          #                    ou link externo / dentro de um repo
  date: AAAA-MM-DD            # (opc) data da reunião, da versão…
  verifiedAt: AAAA-MM-DD      # (opc) última vez que alguém conferiu
- ref: doc-<slug>             # alternativa: reaproveita um doc citado em outro nível

# EVIDÊNCIA — item de qualquer lista evidence:
- source: <doc-|repo-|sub-|app-|…>  # (obr) de onde veio
  locator: <arquivo#âncora ou #L10-L20>   # (obr)
  version: <commit ou data>       # (opc)
  contentHash: sha256:<…>         # (opc) hash do trecho citado
  extraction: human               # (obr) human | extracted | inferred

# GLOSSÁRIO — presente em organização, domínio, subdomínio
glossary:
  - term: <texto>             # (obr) único na linha de herança
    definition: <1 frase>     # (obr)
    synonyms: [<texto>]       # (opc)
    notToConfuseWith: <texto> # (opc) o termo parecido que a IA costuma confundir

# OPERAÇÃO — presente em domínio, subdomínio
operation:
  hours: <texto>              # (opc) ex.: "dias úteis, 9h–17h (horário de Brasília)"
  batchWindows: [<texto>]     # (opc) ex.: ["02:00–07:00 conciliação"]
  criticality: alta           # (opc) baixa | media | alta | critica
  volume: <texto>             # (opc) ex.: "~40 mil operações/dia"

# CONHECIMENTO — presente em domínio, subdomínio, jornada
regulations: [reg-<slug>]     # (opc)
standards:   [std-<slug>]     # (opc)
decisions:   [<DECISÃO>]      # (opc) ver A.6
docs:        [<DOC>]          # (opc)
```

### A.1 Raiz do catálogo

```text
catalogo/
├── organization.yaml
├── repositories.yaml
├── regulations/reg-*.yaml
├── standards/std-*.yaml
└── domains/<id-domínio em minúsculas>/
    ├── domain.yaml
    ├── subdomains/sub-*.yaml
    ├── journeys/jor-*.yaml
    ├── relations/rel-*.yaml
    └── docs/…                 # .md livres, citados pelos campos docs:
```

#### `organization.yaml` — `kind: Organization`

```yaml
spec:
  schemaVersion: 1                        # (obr)
  areas:                                  # (obr, pode ser vazia) rótulos de domínio
    - { id: area-<slug>, name: <texto>, description: <1 frase> }   # description (opc)
  dataLayers:                             # (opc) camadas de dados, na ordem do fluxo
    - { id: raw, name: Raw, meaning: <texto> }
  glossary: [<GLOSSÁRIO>]                 # (opc) jargão corporativo
  docTypes: [negocio, ata, pauta, runbook, arquitetura, gerado, link]   # (opc) tipos de doc aceitos;
                                          #   esses 7 são o padrão, a empresa acrescenta os seus
  vocabulary:                             # (opc) como a empresa chama as coisas
    domainId: "sigla"
  domains: [dom-<slug>]                   # (calc)
```

#### `repositories.yaml` — `kind: RepositoryList`

```yaml
spec:
  repositories:                           # (obr)
    - { id: repo-<slug>, url: <git url> } # (obr) id + endereço; nada mais aqui
```

#### `regulations/reg-*.yaml` — `kind: Regulation`

```yaml
spec:
  jurisdiction: BR                        # (obr)
  effective: { from: AAAA-MM-DD, to: null }   # (obr) vigência
  supersedes: reg-<slug>                  # (opc)
  summary: <1 frase>                      # (opc)
  docs: [<DOC>]                           # (opc) texto oficial, interpretação interna
```

#### `standards/std-*.yaml` — `kind: Standard`

```yaml
spec:
  summary: <1 frase>                      # (obr) o que o padrão exige
  appliesTo: [api | evento | batch | dados | front]   # (opc)
  docs: [<DOC>]                           # (opc)
```

### A.2 Domínio — `domains/<d>/domain.yaml` — `kind: Domain`

```yaml
metadata:
  domainId: PAGV                          # (obr) o "id-domínio" (ex-sigla), único
  area: area-<slug>                       # (obr) da lista organization.areas
spec:
  parent: org-<slug>                      # (obr)
  purpose: <1 frase>                      # (obr)
  does:     [<texto>]                     # (opc) 3–5 itens
  doesNot:  [<texto>]                     # (opc) o que acham que faz e não faz (com quem faz)
  unknowns: [<texto>]                     # (opc) pendências — a IA não deve inventar aqui
  subdomains: [sub-<slug>]                # (obr) SUMÁRIO na ordem de leitura; tem que bater com
                                          #       os Subdomain cujo metadata.domain é este domínio
  sharedRepositories: [repo-<slug>]       # (opc) só repos fora de qualquer aplicação (libs, infra)
  rules: [<REGRA>]                        # (opc) só as que valem para o domínio inteiro
  mainJourneys: [jor-<slug>]              # (opc)
  boundaries: …                           # (calc) a partir das fronteiras dos subdomínios
  glossary: [<GLOSSÁRIO>]                 # (opc) termos do domínio, herdados pelos subdomínios
  operation: <OPERAÇÃO>                   # (opc) herdado pelos subdomínios
  modernization:                          # (opc) só a intenção
    goal: <1 frase>
    decision: ADR-<ID>-NNN
  data: [<DADO>]                          # (opc) dados do domínio inteiro (ver A.3)
  <CONHECIMENTO>                          # (opc) herdado por todos os subdomínios
  nextTaskNumber: 1                       # (opc) operação do Sinter (passos seguintes)
  nextAdrNumber: 1                        # (opc) próximo número de ADR do domínio
  delivery: pr                            # (opc) direct | pr (passo 8)
  # (calc) repos do domínio, panorama de modernização, contagens
```

### A.3 Subdomínio — `domains/<d>/subdomains/sub-*.yaml` — `kind: Subdomain`

Os mesmos blocos do domínio, **menos** `domainId`, `area`, `subdomains` e a operação do Sinter. Tudo do domínio vale aqui por herança.

```yaml
metadata:
  domain: dom-<slug>                      # (obr) o pai; não existe spec.parent no subdomínio
spec:
  purpose: <1 frase>                      # (obr)
  does / doesNot / unknowns               # (opc) como no domínio
  applications:                           # (opc) quem implementa esta parte
    - id: app-<id-domínio>-<slug>         # (obr) único no catálogo
      name: <texto>                       # (obr)
      lifecycle: modern                   # (obr) legacy | modernizing | modern | retired
      aliases: [<texto>]                  # (opc) ex.: CONC0100, nome antigo
      repositories:                       # (obr) os N repos que compõem a aplicação
        - repo: repo-<slug>               # (obr) da lista repositories.yaml
          role: api                       # (obr) frontend | bff | api | batch | lib | infra
          platform: java                  # (obr) java | node | react | mainframe | …
          path: <caminho no repo>         # (opc) quando a aplicação é só parte do repo
          docs: [<DOC>]                   # (opc) links para dentro do repo
      docs: [<DOC>]                       # (opc)
  data:                                   # (opc) DADO — o que esta parte produz
    - id: dat-<slug>                      # (obr)
      name: <texto>                       # (obr)
      description: <1 frase>              # (opc)
      producedBy: app-<slug>              # (opc)
      personalData: false                 # (obr) true → proteção de dados se aplica
      layers:                             # (obr) chaves = organization.dataLayers
        <camada>:
          location: <caminho ou tabela>   # (obr)
          format: <texto>                 # (opc)
          refresh: <texto>                # (opc) ex.: "D+1 06:00"
          quality: [<texto>]              # (opc) regras de qualidade esperadas
          consumers: [<dom-|sub-|ext->]   # (opc)
      docs: [<DOC>]                       # (opc) dicionário de dados, contrato
  rules: [<REGRA>]                        # (opc) as regras desta parte
  journeys: [jor-<slug>]                  # (calc) jornadas com passo neste subdomínio
  boundaries:                             # (opc) quem esta parte recebe e para quem entrega
    in:  [{ from: <dom-|sub-|ext->, what: <texto> }]
    out: [{ to:   <dom-|sub-|ext->, what: <texto> }]
  glossary: [<GLOSSÁRIO>]                 # (opc) só termos desta parte
  operation: <OPERAÇÃO>                   # (opc) só o que difere do domínio
  modernization                           # (opc) como no domínio
  <CONHECIMENTO>                          # (opc) soma com o herdado
  # (calc) repos, panorama, jornadas, conhecimento herdado (marcado)
```

### A.4 Jornada — `domains/<d>/journeys/jor-*.yaml` — `kind: Journey`

```yaml
metadata:
  domain: dom-<slug>                      # (obr)
spec:
  variantOf: jor-<slug>                   # (opc) ex.: PF é variante de "Enviar moeda"
  purpose: <1 frase>                      # (obr)
  trigger: <texto>                        # (obr) o que inicia
  outcome: <texto>                        # (obr) o resultado esperado
  orchestrator: <app-|agenda-|none>       # (opc) quem conduz; none = coreografia por eventos
  stages:                                 # (obr) ao menos uma etapa
    - id: <slug>                          # (obr)
      name: <texto>                       # (opc)
      entry: repo-<slug>                  # (opc) canal de entrada (ex.: micro-front)
      via: [repo-<slug>]                  # (opc) ex.: BFF
      steps:                              # (obr)
        - id: <slug>                      # (obr) único na jornada
          capability: sub-<slug>          # (obr, exceto passo só com externo) qual parte do domínio faz
          calls: <ext-|dom->              # (opc) externo ou outro domínio chamado (SWIFT, Bacen, Risco)
          action: <texto>                 # (obr)
          actor: <texto>                  # (opc) Cliente | Sistema | Agenda | …
          application: app-<slug>         # (opc) quando importa dizer qual aplicação
          result: <texto>                 # (opc)
          next: [<id de passo>]           # (opc) próximos passos (grafo)
          parallelWith: [<id de passo>]   # (opc)
          rules: [rule-<slug>]            # (opc)
          governedBy: [reg-<slug>]        # (opc)
          event: evt-<slug>               # (opc) evento publicado
          job: <texto>                    # (opc) job batch (ex.: CONC0100)
          onFailure: <texto>              # (opc) o que acontece se falhar
  unknowns: [<texto>]                     # (opc)
  <CONHECIMENTO>                          # (opc)
  # (calc) sequência ordenada para consulta, participantes, subdomínios tocados
```

### A.5 Regra — lista `rules:` dentro do domínio ou do subdomínio

Regra **não é arquivo próprio**: é uma frase dentro do nível onde vale. A explicação longa vai para a página `.md` do nível.

```yaml
rules:
  - id: rule-<id-domínio>-<slug>          # (obr) único no catálogo (jornadas citam pelo id)
    statement: <1 frase>                  # (obr) a regra, em linguagem de negócio
    exceptions: [<texto>]                 # (opc)
    example: <texto>                      # (opc)
    regulations: [reg-<slug>]             # (opc) de onde vem, se regulatória
    evidence: [<EVIDÊNCIA>]               # (opc) onde está no código ou no doc
```

### A.6 Decisão (ADR) — lista `decisions:` dentro do domínio ou do subdomínio

Como a regra, a decisão **não é arquivo próprio**: o resumo fica no nível onde vale (o subdomínio herda as do domínio) e o texto completo vai para a página `.md` do nível.

```yaml
decisions:
  - id: ADR-<ID-DOMÍNIO>-NNN              # (obr) número de nextAdrNumber; único no catálogo
    title: <texto>                        # (obr)
    date: AAAA-MM-DD                      # (obr)
    context: <1–2 frases>                 # (obr) o problema
    decision: <1–2 frases>                # (obr) o que foi decidido
    consequences: [<texto>]               # (opc)
    supersedes: ADR-<ID>-NNN              # (opc)
    evidence: [<EVIDÊNCIA>]               # (opc) ex.: a ata de onde saiu
```

### A.7 Relação — `domains/<d>/relations/rel-*.yaml` — `kind: Relation`

Nesta história só existe o tipo `modernized_by`.

```yaml
metadata:
  id: rel-<origem>--<tipo>--<alvo>        # (obr)
  domain: dom-<slug>                      # (obr) domínio da ORIGEM (o dono)
spec:
  source: app-<slug>                      # (obr)
  type: modernized_by                     # (obr)
  target: app-<slug>                      # (obr)
  phase: planned                          # (obr) planned | in-progress | done
  evidence: [<EVIDÊNCIA>]                 # (obr) ao menos uma
```

### A.8 Prefixos de id

| Prefixo | Tipo | Prefixo | Tipo |
|---|---|---|---|
| `org-` | organização | `jor-` | jornada |
| `area-` | área | `rule-` | regra |
| `dom-` | domínio | `ADR-` | decisão |
| `sub-` | subdomínio | `reg-` | regulação |
| `app-` | aplicação (`app-<id-domínio>-<slug>`) | `std-` | padrão |
| `repo-` | repositório | `rel-` | relação |
| `dat-` | dado | `doc-` | doc reaproveitável |
| `ext-` | sistema externo (sem arquivo) | `evt-` | evento (sem arquivo) |
| `agenda-` | agendador batch (sem arquivo) | | |
