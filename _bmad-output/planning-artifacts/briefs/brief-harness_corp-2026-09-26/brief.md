---
title: "Product Brief — Sinter"
status: final
created: 2026-09-26
updated: 2026-09-26
---

# Product Brief: Sinter

## Resumo

Software chega ao código pelas mãos de várias pessoas: negócio ou PM, arquiteto de solução, tech lead e, por fim, o dev, que hoje muitas vezes é um agente de IA. **Em cada passagem de bastão o contexto se perde.** Regras ficam em reuniões, decisões no Confluence, boas práticas em documentos espalhados, e ninguém enxerga como os 20 a 50 repositórios de um domínio se relacionam.

O mercado já concluiu que **o gargalo dos agentes é o contexto, não o modelo**: 90% dos devs usam agentes toda semana, mas só ~3% confiam muito no código gerado. O Sinter remove a atividade que mais destrói valor nessa jornada: **o transporte manual de contexto entre papéis.** O arquiteto organiza cada domínio em um padrão de documentação que não vira bola de lama, e todo projeto recebe uma pasta `.sinter/` com o que humanos e agentes precisam para trabalhar certo.

**Promessa: quando você senta para codificar, o contexto já está resolvido.**

## O Problema

- **Imposto de contexto:** cada tarefa exige explicar de novo ao agente, ou ao dev novo, como o sistema funciona e quais são as regras da casa.
- **Conhecimento fragmentado:** boas práticas espalhadas em Confluence, Google Docs, PDFs e na cabeça das pessoas, muitas vezes contraditórias.
- **Ninguém vê o todo:** nem o arquiteto guarda como 20 a 50 repos se relacionam.
- **Documentação vira lama:** sem padrão, cada documento novo aumenta a confusão.

O resultado é retrabalho, código que viola decisões já tomadas e arquitetos atuando como "ponte humana". Em codebases grandes e desconhecidas, devs experientes ficaram 19% mais lentos com IA (METR).

**Evidência:** o fundador vive a dor, e arquitetos, devs, tech leads e PMs com quem conversou relataram a mesma dor e topariam testar.

## A Solução

Em cada papel, **pensar e decidir** cria valor. **Buscar, repetir e re-explicar contexto** só consome tempo. O produto elimina a segunda parte, sem substituir Confluence, Jira, IDE nem agente (lógica do *Decoupling*).

```
Domínio ──► Conversas guiadas ──► Pacote de contexto ──► .sinter/ no repo ──► Código
```

1. **Domínio como objeto central.** O arquiteto cria um domínio e adiciona repos e documentos (.pdf, .docx, Confluence, Google Docs). A ferramenta gera o **mapa**: sistemas, APIs, eventos e donos.
2. **Padrão de documentação anti-lama.** Tudo é organizado em uma estrutura fixa: visão, glossário, mapa, sistemas, integrações, regras, decisões (ADRs) e padrões. Cada informação tem um lugar, uma única versão verdadeira e uma fonte; conflitos vão para decisão humana. Cada domínio é um repo Git revisado por PR.
3. **Conversas guiadas.** Agentes facilitadores, no estilo do BMAD Method, ajudam a desenhar **processos, funcionalidades ou soluções** já conhecendo o domínio. O resultado volta ao padrão como ADR, regra ou PRD.
4. **Pacote de contexto da tarefa.** A tarefa viaja do PM ao dev, e cada papel só adiciona a sua camada.
5. **`.sinter/` em todo projeto.** Projeto novo já nasce com ela; projeto existente a recebe por PR. Contém contexto do domínio, contratos dos vizinhos, regras, decisões, padrões, skills, agentes e fluxos. AGENTS.md e os arquivos do Claude, Cursor e Copilot são **gerados** a partir dela.
6. **Marketplace de skills e agentes** `.md`, por papel, privados da empresa ou curados da comunidade.

**Princípios:** usar padrões abertos (AGENTS.md, SKILL.md, MCP); deixar o contexto **disponível, não todo carregado**, porque contexto excessivo piora o agente; **incorporar** ferramentas open source para grafo e diagramas (ver addendum) e concentrar o esforço no domínio, no padrão e na cadeia de papéis.

## O Que Diferencia

Os concorrentes **recuperam** contexto na hora da pergunta (Unblocked, Augment, Tabnine, com US$ 20 mi a 250 mi captados), e os agentes controlam onde ele é consumido. **Ninguém é dono de onde o contexto é construído.**

1. **Autoria em cadeia:** cada papel constrói, aprova e é dono da sua camada.
2. **Domínio organizado e rastreável**, versionado em Git, em vez de um índice opaco.
3. **Contexto materializado no repo:** portável, revisável e independente de ferramenta.
4. **Desenho de solução que parte do que a empresa já sabe**, e não do zero.

Em uma frase, contra o concorrente mais próximo: *"o Unblocked responde perguntas na hora; nós preparamos o repo antes da tarefa, curado e versionado."*

## Para Quem

- **Arquiteto de solução (principal):** dono do domínio e curador do contexto. Quer deixar de ser a ponte humana e ver as decisões respeitadas no código.
- **Tech lead:** quer que o agente siga os padrões sem supervisão constante.
- **PM / arquiteto de negócio:** quer que a intenção chegue intacta ao código.
- **Dev (humano ou agente):** quer abrir o repo e começar.

**Quem compra** é a empresa (head de engenharia ou CTO), que exige ROI mensurável, segurança e compliance.

## Critérios de Sucesso `[A VALIDAR NO PRD]`

| Métrica | O que mostra |
|---|---|
| **Acerto na 1ª tentativa:** % de tarefas em que o agente respeita padrões, regras e contratos sem correção de contexto | O harness orienta de verdade |
| **Tempo de setup de contexto** por tarefa e por projeto novo | O imposto de contexto sumiu |
| **Cobertura do harness:** % de repos com `.sinter/` aprovado e de vizinhos com contrato documentado | Adoção e completude |

## Escopo do MVP

**Dentro:** execução local-first, com o cliente escolhendo o modelo de LLM; só código moderno; criação de domínio com padrão opinativo; fontes Git, Confluence, Google Docs, PDF e DOCX; mapa do domínio; consolidação de boas práticas com curadoria; conversas guiadas; pacote de contexto; `.sinter/` para projeto novo e existente, com exports; fluxos "nova feature" e "bugfix"; catálogo inicial de skills; salvaguardas (permissões da fonte, scanner de segredos, registro de aprovações).

**Depois:** transcrição de reunião → decisões e harness que se atualiza (V1); revisão de PR guiada por decisões e checagens automáticas (V2); mainframe (V2+); SaaS multi-empresa e marketplace público.

## Riscos

- 🔴 **Propriedade intelectual:** pela Lei 9.609/98, software ligado ao cargo e feito durante o vínculo pode pertencer ao empregador. Construir com equipamento e dados próprios (repos open source ou sintéticos), revisar o contrato e fazer pilotos com *design partners* sob acordo formal.
- 🟡 **Nome:** escolhido "Sinter" (sinterizar: fundir partículas soltas em uma peça sólida), evitando "Harness" (marca da Harness Inc.) e "Kiln" (colisão com dev tools). Falta a checagem formal no INPI, USPTO e EUIPO e do domínio. "BMad" é marca: o código (MIT) pode ser usado, o nome não.
- 🟡 **Absorção pelos agentes:** memória, skills e regras estão virando nativas. A defesa é o domínio, as fontes corporativas e a autoria em cadeia.
- 🟡 **Contexto grande ou velho** piora o agente: exige limite de tamanho por camada e, na V1, detecção de desatualização.
- 🟡 **Venda corporativa:** SOC 2 e ISO 27001/42001 aparecerão nas compras; LGPD pesa quando entrarem as transcrições.

## Visão

Em 2 a 3 anos, o produto é **a camada de autoria de contexto entre a intenção e o código**: cada domínio é um repositório vivo de conhecimento, cada conversa de design o enriquece e cada repo recebe automaticamente o que precisa. Os erros recorrentes dos agentes viram novas regras e checagens; o mainframe abre bancos, seguradoras e governo; e o marketplace vira o lugar onde empresas compartilham skills, agentes e fluxos por papel.

---
_Detalhes em [addendum.md](addendum.md): glossário, Decoupling, padrão de documentação, `.sinter/`, funcionalidades, stack candidata e pendências. Pesquisa: [domain research](../../research/domain-harness-engineering-context-engineering-definicoes-e-concorrencia-research-2026-09-26.md)._
