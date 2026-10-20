---
name: sinter-documentar
description: Gera e atualiza a documentação de um domínio de software no Padrão de Documentação do Sinter, em 6 camadas construídas de baixo para cima (infraestrutura, componente, sistema, subdomínio, domínio, negócio) mais as gavetas transversais (glossário, regras, decisões, padrões), com diagramas Mermaid versionados e proveniência em cada item. Use sempre que alguém pedir para documentar um repositório, um conjunto de microsserviços, lambdas ou um sistema legado; mapear arquitetura, infraestrutura, contratos ou integrações; escrever diagramas de sequência, C4, fluxo de negócio, estados ou implantação; montar o "repo do domínio"; ou entender "como o todo funciona" de micro a macro, mesmo que não citem o Sinter.
---

# Sinter: documentar um domínio

Você vai produzir a documentação de um domínio no padrão do Sinter: um repositório de Markdown em que **cada informação tem um lugar só, tem fonte e é ligada às camadas de cima e de baixo**. O objetivo é que um arquiteto, um PM ou um agente de código consiga descer de uma capacidade de negócio até a fila e o banco que a sustentam, e subir de uma lambda até o fluxo de negócio que ela serve.

Leia `references/padrao.md` antes de escrever o primeiro arquivo. Ele define as camadas, as gavetas e o que vai em cada uma.

## Por que o padrão é assim

- **Um lugar por informação:** documentação que se repete em vários lugares diverge e vira "bola de lama". Se algo já existe, atualize; não crie outro arquivo.
- **Proveniência em tudo:** o leitor precisa saber se um fato veio do código, de um documento ou de uma suposição sua. Isso é o que torna a documentação confiável.
- **Extraído vs inferido:** o que você leu literalmente (um endpoint no código, uma fila no Terraform) é `extracted`; o que você deduziu (este serviço provavelmente publica este evento) é `inferred`. Nunca apresente inferência como fato.
- **Diagrama é texto:** Mermaid dentro do Markdown, para passar por PR e por revisão como qualquer outro conteúdo.
- **Você propõe, pessoas aprovam:** tudo o que você escreve nasce com `status: proposed`. Só uma pessoa muda para `approved`.

## Direto ao ponto

Documentação boa é a que se lê. Quem abre quer entender o negócio em 2 minutos e achar um serviço em 20 segundos, não ler um inventário.

- Cada item cabe em uma tela. Se passar disso, você está copiando o código: resuma e aponte o arquivo.
- Profundidade onde importa: fluxos principais, integrações, contratos e o que acontece quando algo falha. O resto pode ser uma linha.
- Prefira tabela e diagrama a parágrafo. Frases curtas, sem introdução, sem repetir o que outro item já diz (use link).
- Nada de seção vazia ou "não se aplica": se não há o que dizer, omita a seção.

## Fluxo de trabalho

### 1. Entender o pedido

Descubra, perguntando só o que não der para inferir:
- **Escopo:** um repo, alguns repos ou o domínio inteiro? Quais caminhos ou URLs?
- **Destino:** onde fica o repo do domínio. Padrão: `./dominio-<nome>/`. Se já existir, você está **atualizando**: leia o que existe antes de escrever.
- **Profundidade:** documentação completa ou só algumas camadas (ex.: "só as sequências do checkout").

### 2. Inventário (sem escrever documentação ainda)

Percorra as fontes e monte uma lista do que existe. Use `references/extracao.md` para saber onde procurar cada coisa: infraestrutura como código, manifestos, contratos OpenAPI/AsyncAPI, migrações de banco, clientes HTTP, produtores e consumidores de mensagens, documentos (README, ADRs, `docs/`).

Não copie valores de segredos, tokens ou senhas que encontrar. Registre só que existe um segredo e onde, para alguém tratar.

### 3. Construir de baixo para cima

Escreva nesta ordem, porque cada camada usa a de baixo como evidência:

1. **Infraestrutura:** recursos (bancos, filas, tópicos, buckets, funções, clusters) e ambientes.
2. **Componentes:** cada lambda, endpoint, worker ou job, com gatilho, entrada e saída, dependências e erros.
3. **Sistemas:** ficha, contêineres internos, contratos, modelo de dados e estados.
4. **Subdomínios:** agrupamento de sistemas e, principalmente, o **passo a passo técnico** dos fluxos, em diagramas de sequência entre sistemas.
5. **Domínio:** visão, fronteiras, contexto, eventos de domínio e relações com outros domínios.
6. **Negócio:** capacidades e fluxos macro, em linguagem de negócio.

A camada de negócio quase nunca está no código. Comece por **`negocio/canvas.md`**: uma página propositiva, só com o principal (até 5 itens por bloco), que qualquer pessoa de negócio entenda em 2 minutos. Depois detalhe em arquivos próprios **apenas** as capacidades e os fluxos que estão no canvas. Marque tudo o que deduziu como `inferred` e "(a confirmar)", e faça perguntas ao usuário em vez de inventar indicadores, prioridades ou atores. Um canvas curto e honesto vale mais que um inventário longo de capacidades.

Use os modelos de `references/modelos.md` para cada tipo de item e os padrões de diagrama de `references/diagramas.md`.

### 4. Ligar as camadas

Cada item tem `realiza` (aponta para cima) e `realizado-por` (aponta para baixo), com os ids dos outros itens. O fio completo é:

capacidade → fluxo macro → etapa → sequência → sistema → componente → recurso de infra

Um fluxo de negócio (camada 1) e a sua sequência técnica (camada 3) são **o mesmo fluxo em dois níveis**: cada etapa do fluxo macro aponta para o trecho da sequência que a executa.

### 5. Transversal

Quando encontrar um termo de negócio, uma regra (ex.: timeout de 10 s, até 12x sem juros), uma decisão com justificativa ou uma convenção técnica, crie o item na gaveta transversal e ligue-o aos itens a que se aplica. Se duas fontes dizem coisas diferentes, **não escolha sozinho**: registre as duas versões num item com `conflito: true` e cite as fontes.

### 6. Gerar as duas versões de leitura

Os Markdown são a fonte única. A partir deles, gere duas projeções com os scripts da skill (não escreva essas saídas à mão, para que sejam sempre iguais aos Markdown):

```bash
python3 <skill>/scripts/gerar_site.py <repo-do-dominio> --nome "<Domínio>"   # humanos: site/index.html
python3 <skill>/scripts/gerar_llm.py  <repo-do-dominio> --nome "<Domínio>"   # agentes: llms.txt, llm/contexto.md, llm/grafo.json
```

- **Para pessoas (`site/index.html`):** um site num arquivo só, em abas. **Visão geral** (canvas de negócio, arquitetura do domínio e mapa dos serviços montado a partir da seção "Consome" das fichas), **Microsserviços**, **Fluxos**, **Infraestrutura** e **Referência**. Para o mapa sair certo, preencha a tabela "Consome" de cada ficha de sistema com o nome exato do sistema consumido.
- **Para LLM (`llms.txt` + `llm/`):** índice no padrão llms.txt, um contexto compacto de uma linha por item com as sequências preservadas, e o grafo de ligações em JSON. É o que um agente deve ler primeiro.

Se um script acusar item sem cabeçalho ou ligação para id inexistente, corrija os Markdown e rode de novo.

### 7. Relatório final

Termine escrevendo `RELATORIO.md` na raiz do repo do domínio e mostrando um resumo ao usuário:
- quantos itens por camada, e quantos `extracted` vs `inferred`
- conflitos encontrados
- segredos encontrados (só a localização)
- **perguntas para as pessoas**, agrupadas por papel (PM, arquiteto, tech lead), que destravam o que você não conseguiu confirmar

## Formato de cada item

Um arquivo Markdown por item, com este cabeçalho:

```yaml
---
id: sys-checkout-api            # prefixo do tipo + slug em kebab-case
kind: system                    # capability | flow | domain | subdomain | system | component | resource | environment | contract | entity | integration | rule | decision | standard | term
subject: system:checkout-api    # chave única do assunto, para achar duplicatas
camada: 4                       # 1 negócio ... 6 infraestrutura; 0 para transversal
status: proposed
realiza: [sub-checkout]
realizado-por: [cmp-checkout-api-lambda-authorize, res-payments-db]
provenance:
  - source: repo:checkout-api
    locator: src/main/kotlin/GatewayClient.kt#L20-L41
    version: 8f3c21a            # commit, versão da página ou data do documento
    extraction: extracted       # extracted | inferred | human
---
```

Depois do cabeçalho, o corpo segue o modelo do tipo em `references/modelos.md`.

## Estrutura do repo do domínio

```
dominio-<nome>/
  README.md                 # camada 2: visão, fronteiras, dono
  negocio/canvas.md         # camada 1: resumo em canvas (porta de entrada)
  capacidades/  fluxos/     # camada 1: detalhe só do que está no canvas
  mapa/  eventos/           # camada 2
  subdominios/              # camada 3 (sequências ficam em fluxos/<fluxo>.sequencia.md)
  sistemas/<sistema>/       # camadas 4 e 5 (componentes/ dentro de cada sistema)
  infraestrutura/           # camada 6: recursos/ e ambientes/
  glossario/  regras-de-negocio/  decisoes/  padroes/   # transversal
  RELATORIO.md
```

## Cuidados

- Em repos grandes, priorize amplitude antes de profundidade: primeiro todos os sistemas e integrações, depois o detalhe. Um mapa completo e raso vale mais que um sistema perfeito e o resto vazio.
- Prefira contratos formais (OpenAPI, AsyncAPI, schemas) quando existirem; cite o arquivo em vez de copiar o contrato inteiro.
- Não documente o que o código já diz melhor linha a linha. Documente o que conecta: quem fala com quem, por quê, com qual contrato, e o que acontece quando falha.
- Escreva no idioma do usuário; nomes de sistemas, endpoints e eventos ficam como estão no código.
