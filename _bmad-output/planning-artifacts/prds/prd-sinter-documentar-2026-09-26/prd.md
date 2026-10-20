---
title: "PRD — Sinter · Documentação de domínio (sinter-documentar)"
status: draft
created: 2026-09-26
updated: 2026-09-26
tipo: retrospectivo (registra o que já foi construído e decidido)
relacionado: ../prd-harness_corp-2026-09-26/prd.md
---

# PRD — Sinter · Documentação de domínio

> **Em resumo.** O Sinter promete que, quando alguém senta para codar, o contexto já está resolvido. A primeira peça concreta dessa promessa é a **documentação de domínio**: a partir do código e dos documentos de um domínio, gerar em poucos minutos **6 páginas** que uma pessoa lê em meia hora e que uma IA entende gastando **~1.500 tokens**. Essa capacidade já existe como a skill `sinter-documentar` e foi testada em 3 repositórios públicos, cumprindo 11 de 11 critérios nos três. Este PRD registra o que foi feito, o que foi decidido e o que falta.

## Nesta página

| Seção | O que tem |
|---|---|
| [1. Contexto](#1-contexto) | Onde isso entra no Sinter e por quê |
| [2. O que já fizemos](#2-o-que-já-fizemos) | Linha do tempo: v1, v2, site, testes |
| [3. Quem usa](#3-quem-usa) | Pessoas e o que cada uma quer da doc |
| [4. Requisitos](#4-requisitos) | O que a capacidade faz, com IDs estáveis |
| [5. Qualidade](#5-qualidade-nfr) | Requisitos que valem para tudo |
| [6. Evidência](#6-evidência-testes) | Resultados dos testes |
| [7. Métricas](#7-métricas) | Como saber se funciona, e o que vigiar |
| [8. Fora do escopo](#8-fora-do-escopo) | O que não faz agora |
| [9. Dúvidas e próximos passos](#9-dúvidas-e-próximos-passos) | O que falta decidir e fazer |

---

## 1. Contexto

**Sinter** é uma plataforma B2B, local-first, que ajuda arquitetos (principalmente), tech leads, PMs e devs a montar o **harness** de cada projeto: regras de negócio, mapas do domínio, skills e agentes, prontos no repositório antes da primeira linha de código. O contexto passa de mão em mão (negócio → arquiteto de solução → PM → tech lead → dev ou agente) e fica materializado em `.sinter/`.

**Problema que esta capacidade resolve.** Hoje, entender um domínio com, digamos, 5 microsserviços, bancos, filas e lambdas exige garimpar código, Confluence e reuniões. O resultado costuma ser:

- **para pessoas:** documentação exaustiva que ninguém lê, ou nenhuma documentação;
- **para IA:** o agente lê tudo e queima tokens (context rot), ou lê pouco e inventa.

**Promessa.** Uma documentação **direta ao ponto**, de baixo para cima (infraestrutura → serviços → jornadas → arquitetura → negócio), com o negócio primeiro na leitura e uma versão enxuta para IA.

## 2. O que já fizemos

| Etapa | O que aconteceu | Resultado |
|---|---|---|
| Planejamento BMAD | Brief, pesquisa de domínio, PRD geral (FR-1..37), UX (Esmalte; visões Mundo, Grafo e Caixas), arquitetura (AD-1..16), épicos 1-6 com as histórias do épico 1 | Base do Sinter definida |
| Pesquisa do padrão | Party mode com PM, analista e UX. Referências: Bounded Context Canvas, Event Storming, Domain Storytelling vs BPMN, lista "faz / não faz / não sabemos" (Inception Deck), Diátaxis, C4, arc42, ADRs, llms.txt, Gartner BOAT | Esqueleto v2 |
| Padrão v1 | 6 camadas atômicas, um arquivo por item | 52 a 88 arquivos por domínio; **difícil de ler** (feedback do Gui) |
| Padrão v2 | **6 páginas fixas**, cada uma com "Em resumo", índice "Nesta página", seções e "Fontes" | `esqueleto-v2.md` e exemplo real (Serverlesspresso) |
| Skill v1 → v2 | `sinter-documentar` reescrita com o skill-creator: SKILL.md, 3 referências e 3 scripts | Skill v2 em `.agents/skills/sinter-documentar/` |
| Versão para IA | Cartão `llms.txt` (~1.500 tokens), `llm/resumos.md` (~6k), `llm/grafo.json` | Leitura em degraus |
| Site | Redesenho com a Sally: árvore aninhada só à esquerda, tema claro (escuro opcional), post-its do Event Storming, mapa de serviços automático | `site/index.html`, um arquivo só |
| Testes | 2 iterações × 3 repos públicos, com baseline | v2: 11/11 nos três |

### As 6 páginas (padrão v2)

| Página | Pergunta que responde | Destaques |
|---|---|---|
| `1-negocio` | O que esse domínio faz e para quem? | Quase um canvas: propósito, faz / não faz / não sabemos, **parede de Event Storming** (🟨 ator, 🟦 comando, 🟧 evento, 🟪 política), **quem orquestra**, regras que mandam, entra e sai. Sem jargão técnico. |
| `2-arquitetura` | Como as peças se encaixam? | Contexto do domínio e **mapa dos serviços** gerado automaticamente |
| `3-servicos` | O que cada serviço faz? | Uma seção por serviço: Expõe, Consome, Por dentro, Dados, Quando falha, Infra que usa |
| `4-jornadas` | Como um pedido atravessa o sistema? | Passo a passo e diagrama de sequência com caminho de erro |
| `5-infraestrutura` | Onde roda? | Implantação, recursos, onde ficam os segredos (nunca o valor) |
| `6-referencia` | O resto que se consulta | Glossário, regras, ADRs, padrões, como começar, **dúvidas** |

Acima de ~15 serviços, uma página pode virar pasta, dividida por subdomínio.

## 3. Quem usa

| Pessoa | O que quer da doc |
|---|---|
| **Arquiteto de solução** (usuário principal) | Entender um domínio legado rápido, de baixo para cima, e ter um mapa confiável para desenhar a solução |
| **PM / negócio** | Ler só `1-negocio` e entender propósito, fronteira e regras sem jargão |
| **Tech lead** | Serviços, contratos e jornadas para quebrar o trabalho |
| **Dev** | Chegar na tarefa com a seção certa do serviço e as regras já escritas |
| **Agente de IA** | Entender o todo com o cartão, abrir só a seção necessária e consultar o grafo |

## 4. Requisitos

IDs `FR-D*` para não colidir com FR-1..37 do PRD geral. Substituem o formato atômico descrito hoje em FR-1/FR-2 e em AD-4 (ver §9).

### 4.1 Gerar as 6 páginas

- **FR-D1.** A partir de um ou mais repositórios de um domínio, gerar as 6 páginas fixas (`1-negocio` … `6-referencia`).
- **FR-D2.** Toda página abre com "Em resumo" (um parágrafo em blockquote) e um índice "Nesta página" em tabela, e fecha com "Fontes" (arquivos de onde veio cada afirmação).
- **FR-D3.** A coleta vai de baixo para cima (infra → serviços → jornadas → arquitetura → negócio → referência), mas a leitura começa pelo negócio.
- **FR-D4.** O que não pode ser confirmado no código ou nos documentos vira "(a confirmar)" e entra em "Dúvidas e perguntas". Nada é inventado.
- **FR-D5.** Segredos nunca são copiados; a doc indica só onde ficam.
- **FR-D6.** Acima de ~15 serviços, a página pode ser dividida em pasta por subdomínio, e os geradores leem os dois formatos.

### 4.2 Página de negócio

- **FR-D7.** Mostrar a fronteira do domínio em três colunas: faz / não faz / não sabemos.
- **FR-D8.** Montar a parede de Event Storming (ator → comando → evento → política) a partir dos eventos reais do código.
- **FR-D9.** Ter a seção "Quem orquestra", identificando o orquestrador pelos sinais do repositório: `*.asl.json` → Step Functions; `*.bpmn`, Camunda ou Zeebe → BOAT; Temporal; saga; coreografia por eventos.
- **FR-D10.** Usar no máximo 3 termos técnicos na página de negócio.

### 4.3 Serviços, jornadas e mapa

- **FR-D11.** Cada serviço tem as subseções Expõe, Consome, Por dentro, Dados, Quando falha e Infra que usa.
- **FR-D12.** Na tabela "Consome", a primeira coluna traz o nome exato de **um** serviço por linha; é dela que sai o mapa.
- **FR-D13.** Cada jornada tem um diagrama de sequência com ao menos um caminho de erro.
- **FR-D14.** O mapa de serviços (quem chama quem) é derivado automaticamente das tabelas "Consome" e inserido na página de arquitetura.

### 4.4 Versão para IA, em degraus

- **FR-D15.** Gerar o cartão `llms.txt` (degrau 0, ~1.500 tokens) com: fronteira, serviços com link para a seção, jornadas, quem orquestra, regras, entra e sai, "ainda não se sabe", onde procurar, e uma seção "Optional".
- **FR-D16.** Gerar `llm/resumos.md` (degrau 1, ~6.000 tokens) com o resumo de cada página, seção de serviço e jornada, mais a parede.
- **FR-D17.** Gerar `llm/grafo.json` com serviços, jornadas, chamadas (origem, destino, contrato, interno/externo) e quais serviços cada jornada usa.
- **FR-D18.** Avisar quando o cartão ou os resumos passam do orçamento e dizer o que encurtar.

### 4.5 Site para pessoas

- **FR-D19.** Gerar um site num único arquivo HTML, que abre sem servidor.
- **FR-D20.** A navegação é uma árvore aninhada só à esquerda (página › seção › subseção), com destaque da seção atual durante a rolagem e trilha no topo (ex.: "Serviços › checkout › Consome").
- **FR-D21.** A busca filtra a árvore.
- **FR-D22.** O tema claro é o padrão; o escuro (Esmalte) é opcional e a escolha é lembrada.
- **FR-D23.** A parede de Event Storming aparece como post-its coloridos.
- **FR-D24.** Um nó "Para IA" mostra o `llms.txt` e o total de tokens.

### 4.6 Teste de suficiência

- **FR-D25.** Ao terminar, a skill roda um teste de 10 perguntas (ex.: "o que o domínio não faz?", "quem orquestra a compra?", "o que acontece se o pagamento falhar?") e aponta as que a doc não responde.

## 5. Qualidade (NFR)

- **NFR-D1. Leitura humana.** A página de negócio é lida em ≤ 10 minutos e a doc inteira em ~30 minutos.
- **NFR-D2. Custo para IA.** O cartão fica em ≤ 1.500 tokens e os resumos em ≤ 6.000 tokens.
- **NFR-D3. Poucos arquivos.** No máximo 15 arquivos Markdown escritos, fora `llm/` e `site/`.
- **NFR-D4. Determinismo.** Com as mesmas páginas, os geradores produzem o mesmo resultado. São Python puro, sem dependências nem rede.
- **NFR-D5. Rastreabilidade.** Toda seção cita suas fontes.
- **NFR-D6. Segurança e IP.** Nunca copia segredos. O desenvolvimento e os testes usam só repositórios públicos ou sintéticos, nunca código do empregador (Lei 9.609/98, art. 4).
- **NFR-D7. Acessibilidade do site.** O contraste é legível nos dois temas, funciona em telas estreitas e o `localStorage` é opcional.

## 6. Evidência (testes)

Os testes rodaram em três repositórios públicos, com o mesmo prompt com e sem a skill.

| Eval | Repositório | Foco |
|---|---|---|
| 1 | Online Boutique (microservices-demo, Google) | 12 serviços, gRPC, jornada de compra |
| 2 | Serverlesspresso (serverless-coffee, AWS) | Serverless, Step Functions, eventos |
| 3 | Spring PetClinic Microservices | Negócio e contratos, modelo de dados |

| Iteração | Comparação | Taxa de acerto | Tempo médio | Tokens médios |
|---|---|---|---|---|
| 1 | skill v1 × sem skill | **100%** × 14% | 1.053 s × 367 s | 212 mil × 132 mil |
| 2 | skill v2 × skill v1 | **100% (11/11 nos 3)** × 0% | **610 s** × 1.053 s | **168 mil** × 212 mil |

Mapas gerados na iteração 2:

| Repositório | Serviços | Chamadas |
|---|---|---|
| Online Boutique | 12 | 19 |
| Serverlesspresso | 13 | 22 |
| PetClinic | 8 | 7 |

**Como ler.** Os critérios da iteração 2 foram escritos para o formato v2, então o 0% da v1 mostra a mudança de formato, não uma queda de qualidade. O ganho real da v2 está em sair mais rápida (−42% de tempo) e mais barata (−21% de tokens), com a doc mais curta.

**Aprendizado dos testes.** Uma célula de "Consome" com vários serviços quebrava as ligações do mapa. Daí veio a regra de um serviço por linha (FR-D12).

## 7. Métricas

| Métrica | Meta |
|---|---|
| Critérios automáticos (`grade2.py`) por repo | 11/11 |
| Tempo para documentar um domínio médio | ≤ 15 min |
| Cartão `llms.txt` | ≤ 1.500 tokens |
| Teste de suficiência | ≥ 8 de 10 perguntas respondidas |
| Ligações do mapa reconhecidas como internas | ≥ 90% |

**Contra-métricas (vigiar):**

- Doc curta demais que esconde regra importante: medir pelo teste de suficiência e pela revisão humana.
- Critérios que passam mas a leitura é ruim: exige avaliação qualitativa do Gui e de arquitetos.
- Mais "(a confirmar)" do que conteúdo: sinal de que faltam fontes, não de sucesso.
- Tokens do cartão baixos à custa de links quebrados para seções.

## 8. Fora do escopo

Nesta versão a capacidade não faz:

- Conectores de fontes (Confluence, Google Docs, PDF, transcrições): a skill lê o que está no repositório ou na pasta.
- Edição e curadoria da doc no app Sinter (proposta → aprovação → commit). Está no PRD geral.
- Visões Mundo / Grafo / Caixas: o site é estático, e o app virá depois.
- Código legado não moderno (mainframe).
- Atualização incremental da doc quando o código muda.

## 9. Dúvidas e próximos passos

**Dúvidas:**

- O site novo (árvore, tema claro) ficou bom de usar? Falta o feedback do Gui.
- O teste de suficiência deve bloquear a entrega ou só avisar?
- A página de negócio deve aceitar insumos de reuniões (transcrições) já na próxima versão?
- Quais eventos da parede vêm do código e quais precisam de confirmação humana?

**Próximos passos:**

1. Recolher o feedback do Gui sobre o site e o conteúdo e fazer a iteração 3.
2. Atualizar o PRD geral (FR-1/FR-2), a arquitetura (AD-4) e o brief para o padrão v2: 6 páginas, cartão llms.txt, Event Storming, BOAT.
3. Escrever as histórias dos épicos 2 a 6 (fluxo pausado em `epics.md`, passo 2).
4. Otimizar a descrição da skill para que ela seja acionada nas situações certas.
5. Testar num quarto repositório com orquestração BPMN/Camunda.
