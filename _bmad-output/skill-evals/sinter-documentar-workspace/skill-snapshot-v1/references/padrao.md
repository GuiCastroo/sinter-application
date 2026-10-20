# Padrão de documentação do Sinter: as camadas

O mapa é construído de baixo para cima e lido de cima para baixo.

| Camada | Pergunta | Público | Diagramas | Gavetas |
|---|---|---|---|---|
| 1. Negócio | O que a empresa faz e como o valor flui? | PM, diretoria | Mapa de capacidades; fluxo macro com raias | `capacidades/`, `fluxos/` |
| 2. Domínio | Onde começa e termina e com quem fala? | Arquiteto | Contexto (C4 nível 1); relações entre domínios | `README.md`, `mapa/`, `eventos/` |
| 3. Subdomínio | Como os sistemas executam cada fluxo, passo a passo? | Arquiteto, tech lead | Sequência entre sistemas; fluxo de dados | `subdominios/`, `fluxos/*.sequencia.md` |
| 4. Sistema | Como o serviço é por dentro e o que promete aos outros? | Tech lead, dev | Contêiner (C4 nível 2); sequência interna; dados; estados | `sistemas/<s>/` |
| 5. Componente | O que esta lambda, API, worker ou job faz? | Dev | Sequência curta; fluxo de dados | `sistemas/<s>/componentes/` |
| 6. Infraestrutura | Onde roda e do que depende? | Infra, tech lead | Implantação por ambiente | `infraestrutura/recursos/`, `infraestrutura/ambientes/` |
| Transversal | Termos, regras, decisões e padrões | Todos | — | `glossario/`, `regras-de-negocio/`, `decisoes/`, `padroes/` |

## 1. Negócio

- **Canvas do domínio (`negocio/canvas.md`):** a porta de entrada. Uma página com propósito, para quem, proposta de valor, capacidades e fluxos **principais** (até 5 de cada), eventos que importam, regras críticas, indicadores, fronteiras, linguagem, riscos e dúvidas. É um resumo propositivo, não um inventário.
- Detalhe (capacidades e fluxos em arquivos próprios) só para o que está no canvas.
- **Capacidade:** o que a empresa sabe fazer, em linguagem de negócio (*Vender parcelado*, *Conciliar pagamentos*). Liga para os fluxos e sistemas que a realizam.
- **Fluxo macro:** etapas de ponta a ponta, com atores (cliente, loja, banco, times), decisões e indicadores. Sem nome de sistema. Cada etapa aponta para o trecho da sequência técnica que a executa.
- Fonte típica: pessoas, documentos, conversas. Do código dá para **inferir** candidatos; confirme com o usuário.

## 2. Domínio

- Visão, propósito, dono, o que está dentro e fora.
- Subdomínios e responsabilidade de cada um.
- Contexto: o domínio como uma caixa, com atores e sistemas externos.
- Relações com outros domínios (quem depende de quem, quem publica eventos para quem).
- Eventos de domínio principais, cada um com produtor, consumidores e contrato.

## 3. Subdomínio

- Sistemas do subdomínio e o papel de cada um.
- Para cada fluxo relevante: a sequência de chamadas entre sistemas, com contratos, respostas e caminho de erro. É aqui que o fluxo de negócio vira engenharia.
- Fluxo de dados quando houver pipeline, batch ou ETL.

## 4. Sistema

- Ficha: responsabilidade, dono, stack, repositório, subdomínio, criticidade.
- Contêineres internos: componentes, bancos e filas usados.
- Contratos: APIs expostas, eventos publicados e consumidos, arquivos trocados. Aponte para OpenAPI/AsyncAPI quando existirem.
- Sequências internas dos casos de uso principais.
- Modelo de dados: entidades principais e relações.
- Estados das entidades importantes.
- Requisitos de qualidade conhecidos: timeouts, retentativas, limites, SLAs.

## 5. Componente

Para cada lambda, endpoint, worker ou job:
- gatilho (HTTP, evento, fila, agenda)
- entrada e saída
- dependências (componentes, bancos, filas, externos)
- configuração relevante (timeout, memória, concorrência, variáveis), sem valores secretos
- erros e retentativas, fila de mensagens mortas

## 6. Infraestrutura

- Recursos: bancos, filas, tópicos, buckets, funções, clusters, gateways, com quem usa cada um.
- Ambientes: dev, homologação, produção e as diferenças entre eles.
- Contas, regiões e rede apenas no nível necessário para entender dependências.

## Transversal

- **Glossário:** termo, definição única, sinônimos proibidos.
- **Regra de negócio:** o que o negócio exige; valor atual; onde está implementada.
- **Decisão (ADR):** contexto, opções, escolha, consequências, data, status.
- **Padrão:** como a empresa constrói (convenções, bibliotecas, estrutura).

## Rastreabilidade

capacidade → fluxo macro → etapa → sequência → sistema → componente → recurso

Perguntas que o fio tem que responder:
- "O que sustenta a capacidade X?" (de cima para baixo)
- "Se o recurso Y parar, quais fluxos de negócio quebram?" (de baixo para cima)
