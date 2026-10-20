---
name: Sinter
status: final
created: 2026-09-26
updated: 2026-09-26
sources:
  - ../../prds/prd-harness_corp-2026-09-26/prd.md
  - ../../briefs/brief-harness_corp-2026-09-26/brief.md
---

# Sinter: Experiência

Os mockups de referência estão em [`mockups/`](mockups/). Em caso de conflito entre um mockup e este documento ou o [DESIGN.md](DESIGN.md), **os documentos vencem**. Os nomes de papéis, personagens e funcionalidades seguem o PRD (UJ-1 a UJ-5, FR-1 a FR-33).

## Foundation

- **Duas superfícies:**
  - **App visual** (web, rodando local, desktop) para Arquiteto, PM e Tech lead
  - **CLI** (`sinter`) para o Dev e o agente dele
- **Sem biblioteca de UI definida:** a identidade visual é a do [DESIGN.md](DESIGN.md) (Esmalte), e a escolha de biblioteca de componentes fica para a arquitetura.
- **Só modo escuro no MVP.** O tema claro é pergunta aberta.
- **Desktop primeiro:** a largura mínima suportada do app é 1280 px. Mobile não é objetivo do MVP (ver §Responsive & Platform).

## Information Architecture

**Navegação principal** (trilho à esquerda): Mapa, Curadoria (com contador de conflitos), Conversas, Tarefas e Catálogo.

**Níveis de zoom** (seletor no topo), do macro ao micro:

| Nível | O que mostra | Visões | Mockup |
|---|---|---|---|
| **Empresa** | Todos os domínios, cada um como um mundo | Universo (a desenhar) | — |
| **Domínio** | Os sistemas do domínio agrupados em subdomínios | **Mundo**, **Grafo** e **Caixas** (mesmos dados) | [mundo](mockups/mundo.html), [grafo](mockups/grafo.html), [caixas](mockups/caixas.html) |
| **Sistema** | Um sistema, seus vizinhos e fluxos | Mapa em cartões com fluxo passo a passo | [mapa-sistema](mockups/mapa-sistema.html) |
| **Componente** | O interior de um sistema | A definir na arquitetura | — |

| Superfície | Chega-se por | Propósito | FRs |
|---|---|---|---|
| Mundo do domínio | Abrir um domínio (visão padrão na primeira vez) | Explorar; momento "uau" | FR-10, FR-11 |
| Grafo do domínio | Seletor de visão | Analisar conexões e concentração | FR-10, FR-11 |
| Caixas do domínio | Seletor de visão | Ler a arquitetura como documento; exportar | FR-10, FR-11 |
| Mapa do sistema | Clicar num sistema; "Abrir no nível Sistema" | Vizinhos, contratos, fluxos, inferências | FR-10 a FR-13 |
| Curadoria | Trilho; contador de conflitos | Aprovar propostas e resolver conflitos | FR-14 a FR-16 |
| Conversas | Trilho; "Nova conversa" | Desenhar processo, funcionalidade ou solução | FR-17 a FR-20 |
| Tarefas | Trilho; saída de uma conversa | Pacote de contexto por camadas | FR-21 a FR-24 |
| Catálogo | Trilho | Skills, agentes e fluxos por papel | FR-31 a FR-33 |
| Fontes | "Adicionar fonte" no domínio | Conectar repos e documentos | FR-5 a FR-9 |
| CLI | Terminal do dev | `init`, `task pull`, `sync`, `export`, `status` | FR-24 a FR-30 |

O **seletor de visão** (Mundo, Grafo, Caixas) mantém a seleção atual: o sistema selecionado continua selecionado ao trocar de visão. O app lembra, por usuário, a última visão usada.

## Voice and Tone

| Fazer | Não fazer |
|---|---|
| "Publica PaymentAuthorized?" | "Possível integração detectada!" |
| "Sem acesso de leitura" | "Erro: acesso negado" |
| "Aprovar e próximo" | "Submeter" |
| "Li os dois anexos. Da proposta saíram 3 regras de negócio." | "Processamento concluído com sucesso ✓" |
| "CLAUDE.md foi editado à mão; a próxima exportação sobrescreve. Mova a edição para .sinter/standards/" | "Aviso: arquivo modificado" |
| Usar os termos do Glossário do PRD (domínio, subdomínio, camada, pacote de contexto) | Sinônimos ("projeto", "workspace", "módulo") |

O facilitador das conversas fala como um colega arquiteto: aponta o conflito, cita a fonte e faz uma pergunta por vez. Ele não elogia e não se desculpa.

## Component Patterns

| Componente | Onde | Regras de comportamento |
|---|---|---|
| Cartão de sistema | Mapa do sistema, Caixas | Clique seleciona e abre o detalhe à direita. Duplo clique desce um nível. |
| Estrela | Mundo, Grafo | Clique seleciona. No Mundo, arrastar gira o globo; clicar numa constelação da lista "voa" até ela, com animação de cerca de 0,6 s. |
| Integração inferida | Todas as visões | Selecionar mostra a pergunta de confirmação no painel ("Confirmar integração" ou "Descartar"). Descartada, ela não volta até a fonte mudar. |
| Player de fluxo | Mapa do sistema | Barra inferior com Voltar e Próximo passo. O passo atual acende no mapa, e os sistemas fora do fluxo ficam esmaecidos. |
| Camadas do mapa | Canvas | Chips que ligam e desligam informação (Tecnologia, Status, Donos, Regras). Não mudam o layout. |
| Fila de curadoria | Curadoria | Agrupada por seção do padrão. "Aprovar e próximo" avança para o próximo item da fila. |
| Comparação de fontes | Curadoria | Duas ou mais versões lado a lado, com autor, idade e trecho de origem. O Sinter sugere uma, e a sugestão fica pré-selecionada, mas nunca é aplicada sozinha. |
| Anexos no chat | Conversas | O botão `+` abre o menu de fontes (arquivo, Confluence/Google Docs, item do domínio com `@`, link da web; transcrição marcada "em breve"). Arrastar e soltar funciona no campo. Chips pendentes mostram "lendo…" até o facilitador confirmar o que extraiu. |
| Respostas rápidas | Conversas | O facilitador oferece 2 a 3 opções como botões. Escrever livremente sempre é possível. |
| Artefatos da conversa | Conversas (direita) | Lista viva do que a conversa produz (ADR, sistema, contrato, PRD) com status. "Enviar para curadoria" envia tudo o que está "pronta". |
| Linha do bastão | Tarefas | Uma camada por papel. Só o dono da camada atual edita. "Aprovar camada e passar para…" avisa o próximo papel. |
| Árvore do `.sinter/` | Tarefas | Pré-visualização do que será gravado: novo, alterado, regerado. |
| Medidor de contexto | Tarefas | Barra por camada contra o orçamento (NFR-3). Acima do limite, fica âmbar e aponta a maior camada. |

## State Patterns

| Estado | Superfície | Tratamento |
|---|---|---|
| Domínio vazio | Mundo | Globo sem estrelas e um único convite: "Adicione o primeiro repositório ou documento", com o botão "Adicionar fonte". |
| Processando fontes | Mundo, Caixas | As estrelas aparecem aos poucos, como partículas que se juntam, com o progresso ("12 de 34 repos lidos"). |
| Sistema sem acesso | Todas as visões | Contorno tracejado, "sem acesso de leitura", e a ação "Pedir acesso" no painel. Nunca omitir. |
| Integração inferida | Todas as visões | Partículas vermelhas; rótulo "inferida, confirmar". |
| Conflito aberto | Curadoria, contador no trilho | Caixa de conflito; o item não pode ser aprovado até alguém resolver. |
| Anexo lendo | Conversas | Chip com "lendo…"; o envio da mensagem não espera o fim da leitura. |
| Anexo com falha | Conversas | Chip em âmbar com o motivo ("PDF protegido por senha") e "Tentar de novo". |
| Camada aguardando | Tarefas | Camada esmaecida com o nome de quem vai recebê-la. |
| Segredo detectado | Curadoria (aba Segredos) | Mostra a localização na fonte; o conteúdo nunca aparece na tela. |
| Export editado à mão | CLI (`status`) | Aviso âmbar com o arquivo e para onde mover a edição. |

## Interaction Primitives

- **Seleção única** em todas as visões, compartilhada entre elas.
- **Descer de nível:** duplo clique ou "Abrir no nível Sistema". **Subir:** o breadcrumb.
- **Atalhos:** `/` busca; `1` `2` `3` alternam Mundo, Grafo e Caixas; `[` e `]` voltam e avançam o passo do fluxo; `a` aprova o item de curadoria em foco.
- **Arrastar** gira o Mundo e move o canvas nas outras visões; a roda do mouse dá zoom.
- **Toda ação que torna algo oficial** (aprovar, confirmar integração, passar camada) é explícita e fica registrada; nada é aprovado por inferência.

## Accessibility Floor

- Todas as ações do canvas também são acessíveis pela lista à esquerda e pelo painel (navegação por teclado sem depender do mapa).
- O Mundo tem alternativa textual: as visões Grafo e Caixas e a lista de constelações.
- A rotação automática respeita `prefers-reduced-motion` e tem o botão "Pausar rotação".
- Nenhuma informação só por cor: inferido tem pontilhado e texto; sem acesso tem tracejado e texto; aprovado tem ponto e texto no painel.
- O foco do teclado é sempre visível (anel neon).
- A CLI tem `--json` em todos os comandos e não depende de cor (os prefixos `+`, `~` e `!` carregam o significado).

## Key Flows

**UJ-1: Rafael vê o domínio Pagamentos inteiro pela primeira vez.**
1. Cria o domínio e adiciona as fontes (34 repos, espaço PAG do Confluence, 3 PDFs).
2. O Mundo aparece vazio e as estrelas surgem conforme as fontes são lidas.
3. Ele gira o globo, clica em "Checkout" na lista e o globo voa até a constelação.
4. Seleciona o `checkout-api`: as integrações acendem em neon, e o painel mostra a integração inferida.
5. **Clímax:** o domínio inteiro cabe numa tela, e cada ligação diz de onde veio.
6. Confirma uma inferência, descarta outra e troca para Caixas para mandar o desenho ao time.

**UJ-2: Rafael resolve conflitos.**
1. O trilho mostra "Curadoria 9"; ele abre o primeiro conflito, "Timeout da autorização".
2. Vê 30 s no Confluence (26 meses, a autora saiu) contra 10 s no código (3 semanas, em produção).
3. Confere "Quem depende desta regra", aceita a sugestão e escreve a justificativa.
4. **Clímax:** "Aprovar e próximo". A regra vira fonte única, e faltam 8.

**UJ-3: Carla e Rafael desenham o parcelamento.**
1. Carla abre uma conversa no modo Funcionalidade e anexa a proposta em PDF e o print da tela.
2. O facilitador confirma as 3 regras extraídas e aponta o conflito com a ADR-012.
3. Rafael muda para o modo Solução e propõe o `installment-policy`; o mapa atual vs proposto se atualiza à direita.
4. **Clímax:** a lista "O que esta conversa está produzindo" mostra ADR-013, o sistema novo, o contrato e o PRD; "Enviar para curadoria".

**UJ-4: a tarefa chega pronta para a Bia.**
1. PAG-231 nasce da conversa com as camadas de Negócio e Solução aprovadas.
2. Diego adiciona a camada do repo (padrões e uma nota) e vê a árvore do `.sinter/` e o medidor de contexto (3,7 mil de 5 mil).
3. "Aprovar camada e passar para o dev"; a Bia recebe o aviso.
4. A Bia roda `sinter task pull PAG-231`, e a CLI lista as camadas, os arquivos gravados e os exports regerados.
5. **Clímax:** "Pronto. Peça ao seu agente…"; o agente implementa seguindo `.sinter/flows/nova-feature.md`.

**UJ-5: Diego cria um serviço que já nasce certo.**
1. Roda `sinter init --domain pagamentos --name installment-policy`.
2. A CLI mostra o subdomínio, a ADR de origem e os vizinhos previstos (um contrato ainda em rascunho, em âmbar).
3. **Clímax:** "Pronto em 4 s." O repo nasce com `.sinter/`, skills, agentes, fluxos e exports, e já aparece no mapa como "aguardando primeiro commit".

## Responsive & Platform

- **App:** desktop de 1280 px ou mais. Entre 1280 e 1440 px, o painel de detalhe vira gaveta sobreposta. Abaixo de 1280 px, uma mensagem sugere abrir no desktop; o Mundo e as Caixas continuam navegáveis só para leitura.
- **CLI:** macOS, Linux e Windows (WSL); saída adaptada à largura do terminal; `--json` para agentes e CI.

## Open Questions

1. Tema claro no MVP ou depois?
2. Visão **Empresa** (universo de mundos): desenhar agora ou na V1?
3. Nível **Componente**: o que mostrar dentro de um sistema?
4. Tela de **Fontes** e de **Catálogo**: ainda sem mockup; construir a partir deste documento ou desenhar antes?
5. Biblioteca de componentes do app: fica para a arquitetura.
