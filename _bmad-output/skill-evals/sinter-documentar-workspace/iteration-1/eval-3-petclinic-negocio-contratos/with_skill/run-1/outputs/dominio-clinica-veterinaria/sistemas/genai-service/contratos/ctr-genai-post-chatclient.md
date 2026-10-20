---
id: ctr-genai-post-chatclient
kind: contract
subject: contract:genai-service:POST-/chatclient
camada: 4
status: proposed
realiza: [cap-atendimento-inteligente]
realizado-por: [cmp-genai-chat-api]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/PetclinicChatClient.java#L58-L68
    version: aefaf7f
    extraction: extracted
---

# POST /chatclient
| Campo | Valor |
|---|---|
| Tipo | API (síncrona do ponto de vista do cliente) |
| Produtor | `genai-service` |
| Consumidores | `api-gateway` (rota `/api/genai/**`), frontend AngularJS (`scripts/genai/chat.js`) |
| Especificação | sem OpenAPI/AsyncAPI; extraído de `PetclinicChatClient.exchange` |

Recebe uma pergunta em texto livre e devolve a resposta do assistente virtual, já com eventuais ações executadas (ex.: cadastro de owner/pet) via *tool calling*.

## Exemplo
```
// POST /chatclient
"Quantos donos de pets estão cadastrados?"
// -> 200
"Atualmente há 10 tutores cadastrados na clínica."
```
