---
id: flow-atendimento-assistente-virtual
kind: flow
subject: flow:atendimento-assistente-virtual
camada: 1
status: proposed
realiza: [cap-atendimento-inteligente]
realizado-por: [sys-genai-service, sys-api-gateway, sys-customers-service, sys-vets-service]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/PetclinicChatClient.java; PetclinicTools.java
    version: aefaf7f
    extraction: inferred
---

# Atendimento via assistente virtual
Permitir que um usuário converse em linguagem natural com um assistente virtual para consultar tutores, pets e veterinários, ou até cadastrar um novo tutor/pet, sem navegar pelas telas tradicionais.

## Atores
- **Usuário (tutor ou equipe clínica)** — faz perguntas ou pede ações em linguagem natural
- **Assistente virtual (IA)** — interpreta a pergunta, decide se precisa consultar/alterar dados e responde
- **Sistema (clínica veterinária)** — fornece os dados reais de owners/pets/vets sob demanda do assistente

## Etapas
| # | Etapa | Ator | Decisão ou resultado | Técnica |
|---|---|---|---|---|
| 1 | Usuário envia uma pergunta ou pedido em texto livre | Usuário | ex.: "liste os donos" ou "cadastre um novo pet" | [passo 1](./flow-atendimento-assistente-virtual.sequencia.md#passo-1) |
| 2 | Assistente decide se precisa consultar ou alterar dados da clínica | Assistente virtual | invoca uma ou mais ferramentas (tools) | [passo 2](./flow-atendimento-assistente-virtual.sequencia.md#passo-2) |
| 3 | Sistema executa a consulta/ação solicitada | Sistema | dado retornado ou registro criado | [passo 2](./flow-atendimento-assistente-virtual.sequencia.md#passo-2) |
| 4 | Assistente compõe e devolve a resposta em linguagem natural | Assistente virtual | resposta ao usuário, ou mensagem de indisponibilidade em caso de falha | [passo 3](./flow-atendimento-assistente-virtual.sequencia.md#passo-3) |

## Diagrama
```mermaid
flowchart LR
  subgraph Usuário
    A[Faz pergunta em texto livre] --> D[Recebe resposta]
  end
  subgraph Assistente virtual
    A --> B{Precisa de dados da clínica?}
    B -- sim --> C[Invoca ferramenta: listar/cadastrar owner, pet ou vet]
    B -- não --> E[Responde com conhecimento geral]
    C --> F{Clínica respondeu a tempo?}
    F -- sim --> G[Compõe resposta com os dados]
    F -- não --> H[Responde "assistente indisponível"]
    G --> D
    H --> D
    E --> D
  end
```

## Indicadores
- Volume de conversas, taxa de erro/indisponibilidade, custo por interação com o provedor de LLM — não encontrados no código; **a confirmar com o PM**.

## Regras que governam
- [Memória de conversa limitada a 10 mensagens](../regras-de-negocio/reg-memoria-conversa.md)
- [Tipos de pet permitidos](../regras-de-negocio/reg-tipos-de-pet.md)
