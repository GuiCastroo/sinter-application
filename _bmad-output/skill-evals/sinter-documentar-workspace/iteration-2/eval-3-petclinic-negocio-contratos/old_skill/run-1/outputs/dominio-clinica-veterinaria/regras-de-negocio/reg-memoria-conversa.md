---
id: reg-memoria-conversa
kind: rule
subject: rule:memoria-conversa
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/PetclinicChatClient.java#L44-L50
    version: aefaf7f
    extraction: extracted
---

# O assistente virtual lembra até 10 mensagens anteriores
O `MessageChatMemoryAdvisor` é configurado com `.order(10)` — o contexto de conversa considerado pelo LLM cobre até as últimas 10 mensagens. Implementação de armazenamento da memória (em memória, banco, etc.) não confirmada nas fontes lidas.

## Onde está implementada
- `spring-petclinic-genai-service` — `PetclinicChatClient`
