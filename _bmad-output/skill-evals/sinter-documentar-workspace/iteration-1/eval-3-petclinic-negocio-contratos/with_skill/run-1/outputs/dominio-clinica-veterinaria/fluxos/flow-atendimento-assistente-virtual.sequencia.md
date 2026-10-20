---
id: flow-atendimento-assistente-virtual-sequencia
kind: flow
subject: flow:atendimento-assistente-virtual:sequencia
camada: 3
status: proposed
realiza: [flow-atendimento-assistente-virtual]
realizado-por: [ctr-genai-post-chatclient, ctr-customers-get-owners, ctr-customers-post-owners, ctr-customers-post-pet]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/PetclinicChatClient.java; PetclinicTools.java; AIDataProvider.java
    version: aefaf7f
    extraction: extracted
---

# Atendimento via assistente virtual: sequência técnica
Realiza as etapas do [fluxo macro](./flow-atendimento-assistente-virtual.md).

## Diagrama
```mermaid
sequenceDiagram
  participant UI as Frontend (chat.js)
  participant GW as api-gateway
  participant CHAT as genai-service (PetclinicChatClient)
  participant LLM as Provedor LLM externo
  participant TOOLS as PetclinicTools/AIDataProvider
  participant CUST as customers-service

  UI->>GW: POST /api/genai/chatclient (pergunta)
  GW->>CHAT: POST /chatclient (StripPrefix=2, circuit breaker "genaiCircuitBreaker")
  CHAT->>LLM: prompt + system message + lista de tools disponíveis
  alt LLM decide chamar uma tool (ex.: listOwners)
    LLM-->>CHAT: pedido de function-call
    CHAT->>TOOLS: listOwners()
    TOOLS->>CUST: GET /owners (via DiscoveryClient + RestClient)
    CUST-->>TOOLS: 200 lista de owners
    TOOLS-->>CHAT: dados formatados
    CHAT->>LLM: resultado da tool
    LLM-->>CHAT: resposta final em linguagem natural
  else LLM responde direto (sem tool)
    LLM-->>CHAT: resposta final
  end
  CHAT-->>GW: 200 texto da resposta
  GW-->>UI: 200 repassado

  alt exceção em qualquer etapa acima
    CHAT-->>GW: 200 "Chat is currently unavailable. Please try again later."
  end
  alt genai-service fora do ar (nível de rede)
    GW-->>UI: fallback (POST /fallback, 503)
  end
```

## Passos
### Passo 1
O frontend envia a pergunta como corpo de texto puro para `POST /chatclient`, roteado pelo `api-gateway` (`/api/genai/**`, com circuit breaker nomeado `genaiCircuitBreaker` além do padrão — sinal de que este caminho é considerado mais instável, por depender de um provedor de LLM externo).

### Passo 2
`PetclinicChatClient` monta o prompt com um system message fixo (persona do assistente da Spring Petclinic) e disponibiliza as 4 tools de `PetclinicTools` ao LLM (`listOwners`, `addOwnerToPetclinic`, `listVets`, `addPetToOwner`). Se o LLM decidir invocar uma tool, `AIDataProvider` executa a chamada real ao `customers-service` (resolvido via `DiscoveryClient`, não via Gateway) ou busca no `VectorStore` local (para `listVets`).

### Passo 3
O resultado da tool volta ao LLM, que compõe a resposta final em linguagem natural, devolvida ao usuário.

### Caminho de erro
- Qualquer exceção dentro de `PetclinicChatClient.exchange` (falha do LLM, falha de rede ao chamar `customers-service`, etc.) é capturada e vira a resposta fixa "Chat is currently unavailable. Please try again later." — **o usuário recebe HTTP 200 com uma mensagem de erro em texto**, não um HTTP 5xx (comportamento notável para quem for tratar erros no frontend).
- Se o próprio `genai-service` estiver fora do ar (não apenas uma exceção interna, mas indisponibilidade de rede), o circuit breaker do `api-gateway` intercepta e devolve o fallback genérico (`POST /fallback`, `503`).
