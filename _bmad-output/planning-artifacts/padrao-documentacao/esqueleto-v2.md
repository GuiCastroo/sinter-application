---
title: "Esqueleto da documentação de domínio: v2"
status: draft
created: 2026-09-26
origem: party mode com John (PM) e Mary (analista), a partir da pesquisa sobre Bounded Context Canvas, Event Storming, NOT list do Inception Deck, Diátaxis e BOAT (Gartner 2026)
substitui: padrao-documentacao-sinter.md (v1, atomizado em um arquivo por item)
---

# Esqueleto da documentação de domínio (v2)

**Princípio:** poucos documentos, cada um respondendo a uma pergunta de quem lê. Explicação primeiro, referência depois (Diátaxis). O detalhe atômico, para curadoria e LLM, é **gerado** a partir destes documentos, e não o contrário.

```
dominio-<nome>/
  1-negocio.md         Como o domínio funciona para o negócio              (todos)
  2-arquitetura.md     Como o domínio é montado, com o mapa dos serviços   (arquiteto, tech lead)
  3-servicos.md        Todos os microsserviços, uma seção por serviço      (tech lead, dev, agente)
  4-jornadas.md        Todas as jornadas, uma seção por jornada            (todos)
  5-infraestrutura.md  Onde roda e do que depende                          (tech lead, infra)
  6-referencia.md      Glossário, regras, ADRs, padrões, como começar, dúvidas (consulta)
  AGENTS.md / llms.txt Cartão do domínio para IA (gerado, ~1.500 tokens)
  llm/                 resumos.md e grafo.json (gerados)
```

**Sempre 6 páginas**, qualquer que seja o tamanho do domínio. Cada página é organizada por dentro, com seções e âncoras estáveis (ex.: `3-servicos.md#checkout-api`), para que o cartão da IA e os links apontem direto para a seção.

**Cada página abre com o seu próprio índice.** A primeira coisa depois do título é o "Em resumo" e, logo abaixo, o **"Nesta página"**: a lista das seções com link e uma linha sobre cada uma. Quem lê (pessoa ou IA) bate o olho no índice e pula direto para o que precisa.

Exemplo do topo de `3-servicos.md`:

```markdown
# Serviços do domínio Pagamentos

> **Em resumo:** 13 serviços em 4 subdomínios. O checkout-api orquestra a compra;
> o payments-gateway fala com o adquirente; o ledger é o mais conectado.

## Nesta página
| Serviço | Subdomínio | Em uma linha |
|---|---|---|
| [checkout-api](#checkout-api) | Checkout | Recebe o pedido e orquestra autorização e antifraude |
| [payments-gateway](#payments-gateway) | Autorização | Fala com o adquirente (ISO 8583) |
| [ledger](#ledger) | Contabilidade | Registra os lançamentos de cada pagamento |
```

**Quando dividir:** só se uma página ficar grande demais para ler (ex.: mais de ~15 serviços). Aí `3-servicos.md` vira a pasta `servicos/`, com um arquivo por subdomínio, e o resto não muda.

Cada página e cada seção de serviço ou jornada **começa** com um bloco **"Em resumo"** (3 a 5 linhas) e **termina** com um bloco curto **"Fontes"** (de onde veio cada informação, e o que é inferido).

## Leitura para IA: em camadas, gastando pouco

A IA não lê a documentação toda, nem uma página inteira quando só precisa de uma seção. Ela lê em três degraus e só desce quando precisa:

| Degrau | Arquivo | Orçamento | O que dá para responder |
|---|---|---|---|
| **0. Cartão do domínio** | `AGENTS.md` / `llms.txt` (gerado) | **até ~1.500 tokens** | O que é o domínio, subdomínios, cada serviço em uma linha, jornadas em uma linha, as 5 regras, **onde procurar cada coisa** |
| **1. Resumos** | `llm/resumos.md` (gerado: o "Em resumo" de cada documento) | **até ~6.000 tokens** | Visão de todos os serviços, jornadas e infra, sem detalhe |
| **2. Seção completa** | a seção do serviço ou da jornada (pela âncora) | sob demanda | O detalhe de uma coisa só |

Mais um atalho: `llm/grafo.json` (quem chama quem, qual jornada usa qual serviço), para responder perguntas de ligação sem abrir documentos.

**Tabela "onde procurar"** no cartão do domínio: pergunta → arquivo. Ex.: "como funciona o pagamento?" → `4-jornadas.md#compra`; "o que o checkout-api expõe?" → `3-servicos.md#checkout-api`.

**Teste de suficiência:** com **só o degrau 0**, uma IA tem que responder corretamente 10 perguntas-padrão (o que o domínio faz, quais serviços existem, qual serviço cuida de X, qual é a jornada principal, quem orquestra, onde fica o dado Y, qual regra governa Z, com quais domínios fala, o que ele não faz, o que ainda não se sabe). Se não responde, o cartão está incompleto.

## 1-negocio.md

1. **Em uma frase:** o que é, para quem, por quê
2. **Por que existe:** propósito e valor; classificação estratégica (core, suporte ou genérico)
3. **Faz / Não faz / Não sabemos:** três colunas (a NOT list)
4. **A parede do domínio:** Event Storming *Big Picture*. Linha do tempo dos eventos de negócio, com:
   - 🟧 evento (no passado) · 🟦 comando · 🟨 ator · 🟪 política ("sempre que X, faça Y") · 🩷 sistema externo · 🟥 hotspot
   - Na fonte: tabela da linha do tempo. No site: a parede de post-its desenhada.
5. **Jornadas principais:** de 1 a 3, com uma linha cada e link para a seção em `4-jornadas.md`
6. **Quem orquestra:** por jornada, quem manda no processo: motor de processo (BOAT: Camunda, Pega, Appian…), Step Function, serviço orquestrador ou coreografia por eventos
7. **Regras que mandam:** as 5 políticas 🟪 e regras que mais importam
8. **Entra e sai:** eventos, comandos e consultas trocados com outros domínios
9. **Linguagem:** os termos que aparecem na parede (até 10)
10. **Indicadores:** como se sabe que vai bem (a confirmar com o PM)

## 2-arquitetura.md

1. **Contexto:** o domínio como caixa, com atores e sistemas externos (diagrama)
2. **Subdomínios:** tabela com responsabilidade e serviços de cada um
3. **Mapa dos serviços:** quem chama quem, agrupado por subdomínio (diagrama)
4. **Estilo de integração:** síncrono (REST/gRPC) ou assíncrono (eventos, filas); onde há orquestração e onde há coreografia
5. **Decisões que moldam:** as ADRs que explicam o desenho (links para a referência)
6. **Riscos técnicos:** o que quebra junto (ex.: cobrança sem estorno se o frete falhar)

## 3-servicos.md (uma seção por serviço)

1. **O que faz:** uma frase, subdomínio, dono, stack, repositório
2. **Expõe:** contratos de API e eventos publicados (tabela; aponta OpenAPI/AsyncAPI)
3. **Consome:** o que chama e o que escuta (tabela; é daqui que sai o mapa dos serviços)
4. **Por dentro:** componentes (lambdas, workers, jobs), com gatilho e o que fazem (tabela)
5. **Dados:** entidades principais e estados (diagramas curtos)
6. **Quando falha:** timeouts, retentativas, filas de erro, o que o usuário vê
7. **Infra que usa:** bancos, filas e buckets (links para a infraestrutura)

## 4-jornadas.md (uma seção por jornada)

1. **A jornada em linguagem de negócio:** Event Storming *Process Level* (eventos, comandos, atores, políticas)
2. **Quem orquestra**
3. **Passo a passo técnico:** diagrama de sequência entre os serviços, com o caminho de erro
4. **Regras e hotspots desta jornada**

## 5-infraestrutura.md

1. **Ambientes:** dev, homologação, produção e as diferenças
2. **Recursos:** bancos, filas, tópicos, buckets, funções e clusters, e quem usa cada um (tabela)
3. **Implantação:** diagrama por ambiente
4. **De onde veio:** Terraform, CloudFormation, `serverless.yml`, Kubernetes

## 6-referencia.md

1. **Glossário**
2. **Regras de negócio:** valor atual e onde está implementada
3. **Decisões (ADRs)**
4. **Padrões técnicos**
5. **Como começar:** rodar localmente e os testes; onde fica cada coisa no código; as 3 mudanças mais comuns; como publicar
6. **Dúvidas e perguntas:** os 🟥 hotspots, os conflitos entre fontes e as perguntas por papel (PM, arquiteto, tech lead)
