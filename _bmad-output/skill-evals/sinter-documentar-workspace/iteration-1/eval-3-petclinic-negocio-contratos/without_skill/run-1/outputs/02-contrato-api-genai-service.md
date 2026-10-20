# Contrato de API — genai-service

- Base path local: `http://localhost:8084` (`web-application-type: reactive`)
- Via api-gateway: `http://<gateway>/api/genai/**` (`StripPrefix=2` + `CircuitBreaker=name=genaiCircuitBreaker,fallbackUri=/fallback`)
- Controller-fonte: `PetclinicChatClient.java`
- Formato: texto simples de entrada/saída (não é um JSON estruturado de request/response)

## `POST /chatclient` — Conversar com o assistente da clínica

Único endpoint HTTP de negócio exposto por este serviço.

- **Request body:** `string` (a pergunta/instrução em linguagem natural do usuário, texto puro, não um objeto JSON).
- **Response:** `200 OK` com `string` (a resposta do assistente em linguagem natural).
  - Em caso de erro no processamento (ex.: falha no provedor de IA), retorna a string fixa: `"Chat is currently unavailable. Please try again later."` em vez de propagar erro HTTP.
- **Comportamento:** o texto do usuário é processado por um `ChatClient` do Spring AI, com:
  - Um *system prompt* fixo definindo o papel do assistente (focado em veterinários, tutores, pets e visitas da "Spring Petclinic").
  - Memória de conversa (`ChatMemory`, via `MessageChatMemoryAdvisor`) — mantém contexto entre chamadas dentro de uma mesma sessão/thread de conversa.
  - Um conjunto de *tools* (function calling) que o modelo pode decidir invocar (ver abaixo).
  - Provedor de modelo configurável: OpenAI (`gpt-4o-mini`, chave via `OPENAI_API_KEY`) ou Azure OpenAI (`gpt-4o`, chave/endpoint via `AZURE_OPENAI_KEY`/`AZURE_OPENAI_ENDPOINT`), `temperature: 0.7`.

### Ferramentas (tools) disponíveis ao modelo — não são endpoints HTTP diretos, mas parte do contrato funcional do assistente

| Tool | Efeito | Serviço de negócio acionado internamente |
|---|---|---|
| `listOwners` | Lista os tutores da clínica | `customers-service` `GET /owners` |
| `addOwnerToPetclinic` | Cadastra um novo tutor (nome, sobrenome, endereço, cidade, telefone — telefone deve ter 10 dígitos conforme instrução da tool) | `customers-service` `POST /owners` |
| `listVets` | Lista veterinários que casam com um critério opcional, via busca semântica (vector store) | Vector store interno (dados originados de `vets-service` `GET /vets` na carga inicial) |
| `addPetToOwner` | Adiciona um pet a um tutor existente, dado `ownerId` e `petTypeId` (1=gato, 2=cachorro, 3=lagarto, 4=cobra, 5=pássaro, 6=hamster) | `customers-service` `POST /owners/{ownerId}/pets` |

## Sem controller separado, mas parte do runtime do serviço

- **Carregamento do vector store (não é um endpoint HTTP):** ao subir a aplicação (`ApplicationStartedEvent`), o serviço tenta carregar `vectorstore.json` do classpath; se ausente, chama `vets-service` (`GET /vets`) uma única vez, gera embeddings e persiste um novo arquivo local temporário. Não há endpoint para forçar reindexação sob demanda.

## Consumidores conhecidos deste contrato

- UI do `api-gateway` (`scripts/genai/chat.js`) consome `POST /api/genai/chatclient` (roteado pelo gateway) para a experiência de chat na tela.

## Observações de contrato

- O corpo de request/response é texto puro, não um envelope JSON com metadados (ex.: sem `conversationId` explícito no contrato HTTP — a continuidade de contexto é gerenciada internamente pelo `ChatMemory`).
- Não há endpoint de health/streaming específico documentado no código revisado além do endpoint padrão do Actuator (não analisado em detalhe neste levantamento).
