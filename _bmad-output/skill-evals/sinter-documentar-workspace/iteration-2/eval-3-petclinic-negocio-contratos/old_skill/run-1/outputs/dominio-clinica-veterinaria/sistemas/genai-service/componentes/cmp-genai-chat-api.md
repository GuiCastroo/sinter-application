---
id: cmp-genai-chat-api
kind: component
subject: component:genai-service:petclinic-chat-client
camada: 5
status: proposed
realiza: [sys-genai-service]
realizado-por: [cmp-genai-tools]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/PetclinicChatClient.java
    version: aefaf7f
    extraction: extracted
---

# PetclinicChatClient
Endpoint que recebe a pergunta do usuário em texto livre e a repassa ao LLM configurado, com um prompt de sistema fixo e ferramentas (`PetclinicTools`) que o modelo pode invocar.

| Campo | Valor |
|---|---|
| Tipo | endpoint (controller reativo) |
| Gatilho | HTTP POST `/chatclient` |
| Entrada | corpo `String` (a pergunta do usuário, texto livre) |
| Saída | `String` (resposta do assistente) |
| Timeout / memória / concorrência | não configurado explicitamente; depende do timeout do provedor de LLM (não encontrado nas fontes) |

## Dependências
- `PetclinicTools` (`@Tool`s: `listOwners`, `addOwnerToPetclinic`, `listVets`, `addPetToOwner`)
- `ChatMemory` (contexto de até 10 mensagens anteriores)
- Provedor de LLM externo (Azure OpenAI ou OpenAI, conforme configuração)

## Erros e retentativas
- Qualquer exceção na chamada ao LLM é capturada e vira a resposta fixa "Chat is currently unavailable. Please try again later." (não propaga erro HTTP 5xx ao chamador).
