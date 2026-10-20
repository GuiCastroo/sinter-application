---
id: cmp-genai-tools
kind: component
subject: component:genai-service:petclinic-tools
camada: 5
status: proposed
realiza: [sys-genai-service]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/PetclinicTools.java; spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/AIDataProvider.java
    version: aefaf7f
    extraction: extracted
---

# PetclinicTools / AIDataProvider
Conjunto de "ferramentas" (`@Tool`) que o LLM pode chamar durante a conversa, e o provedor que de fato executa essas chamadas contra os serviços de negócio.

| Campo | Valor |
|---|---|
| Tipo | worker (function-calling invocado pelo LLM, não pelo usuário diretamente) |
| Gatilho | decisão do LLM durante o processamento de um prompt (`ChatClient.defaultTools`) |
| Entrada | argumentos estruturados que o LLM extrai da pergunta do usuário |
| Saída | dados estruturados (lista de owners, vets, pet criado, owner criado) devolvidos ao LLM para compor a resposta final |
| Timeout / memória / concorrência | não configurado explicitamente |

## Dependências
- `customers-service`, via `DiscoveryClient.getInstances("customers-service")` + `RestClient` (chamadas síncronas bloqueantes: `GET /owners`, `POST /owners`, `POST /owners/{ownerId}/pets`)
- `VectorStore` — busca semântica de veterinários (`listVets`), com `topK=20` (com filtro) ou `topK=50` (sem filtro)

## Erros e retentativas
- `listVets` captura `JacksonException` na serialização do filtro e retorna lista vazia em vez de propagar erro.
- Demais tools não têm tratamento de erro específico identificado — falhas de rede em `AIDataProvider` propagam para `PetclinicChatClient`, que por sua vez cai na resposta fixa de indisponibilidade.
