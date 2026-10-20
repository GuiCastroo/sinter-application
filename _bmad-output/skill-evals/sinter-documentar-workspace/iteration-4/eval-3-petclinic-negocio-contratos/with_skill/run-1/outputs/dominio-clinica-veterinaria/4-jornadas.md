# Jornadas: Clínica Veterinária

> **Em resumo:** 5 jornadas, todas síncronas via REST. Sem orquestrador único: cada jornada é uma
> chamada direta a um serviço, ou uma agregação pontual do `api-gateway` (junta dois serviços,
> com circuit breaker). As jornadas centrais são a ficha do dono e o assistente de IA; as demais são
> chamadas simples e aparecem como tabela de entrada e saída.

## Nesta página

| Seção |
|---|
| [Cadastrar dono e pet](#cadastrar-dono-e-pet) |
| [Registrar uma visita](#registrar-uma-visita) |
| [Consultar a ficha do dono](#consultar-a-ficha-do-dono) |
| [Consultar veterinários](#consultar-veterinários) |
| [Conversar com o assistente de IA](#conversar-com-o-assistente-de-ia) |

## Cadastrar dono e pet

**Participantes:** `customers-service`
> **Em resumo:** a recepção (ou o próprio front-end) cria o dono e, na sequência, adiciona um ou
> mais pets a ele. Cada pet pertence a exatamente um dono.

**Em linguagem de negócio:**
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Recepção/dono | Preenche dados do dono (nome, endereço, cidade, telefone) | Dono cadastrado | Nome, endereço, cidade e telefone são obrigatórios; telefone só números, até 12 dígitos |
| 2 | Recepção/dono | Escolhe o tipo do pet e preenche nome e data de nascimento | Pet cadastrado, associado ao dono | Pet precisa de um dono já existente; nome do pet não pode ser vazio |

**Quem orquestra:** ninguém — são duas chamadas independentes e sequenciais ao `customers-service` (`POST /owners`, depois `POST /owners/{ownerId}/pets`), decididas pelo cliente (front-end ou o assistente de IA).

**Passo a passo técnico:**
```mermaid
sequenceDiagram
  participant Cliente
  participant CS as customers-service
  Cliente->>CS: POST /owners {dados do dono}
  CS-->>Cliente: 201 Owner criado
  Cliente->>CS: POST /owners/{ownerId}/pets {nome, tipo, nascimento}
  alt dono existe
    CS-->>Cliente: 201 Pet criado
  else dono não existe
    CS-->>Cliente: 404 Owner not found
  end
```

**Regras que mudam o resultado:** campos obrigatórios e telefone [R01/R02](6-referencia.md#regras-de-negócio); nome do pet [R03](6-referencia.md#regras-de-negócio).

---

## Registrar uma visita

**Participantes:** `visits-service`
> **Em resumo:** a clínica registra que um pet foi atendido, com data e descrição livre; não há
> conceito de agendamento prévio com confirmação — é um registro histórico do atendimento.

**Em linguagem de negócio:**
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Clínica/veterinário | Registra a visita de um pet (data + descrição) | Visita registrada | Descrição até 8192 caracteres; `petId` é só um número, sem checagem de existência |

| Entrada | Saída | Erro |
|---|---|---|
| `POST /owners/*/pets/{petId}/visits` com `date` e `description` | `201` com a visita criada | `400` se a descrição passar de 8192 caracteres ([R04](6-referencia.md#regras-de-negócio)); `petId` inexistente **não** gera erro |
| `GET /owners/*/pets/{petId}/visits` | `200` com as visitas do pet | — |

Chamada direta ao `visits-service`, sem outro serviço envolvido.

---

## Consultar a ficha do dono

**Participantes:** `api-gateway`, `customers-service`, `visits-service`
> **Em resumo:** a jornada mais "orquestrada" do domínio — o `api-gateway` busca o dono e depois, em lote, as visitas de todos os pets dele, juntando tudo numa única resposta para o front-end.
> Se as visitas falharem, a ficha aparece mesmo assim, só que sem histórico.

**Em linguagem de negócio:**
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Dono/recepção | Abre a ficha de um dono | Ficha exibida com dono, pets e visitas de cada pet | Se o histórico de visitas não puder ser buscado a tempo, a ficha mostra os pets sem visitas em vez de falhar |

**Quem orquestra:** `ApiGatewayController.getOwnerDetails` busca o dono e depois, em lote, as visitas dos seus pets. O circuit breaker `getOwnerDetails` devolve visitas vazias se essa segunda consulta falhar. Teste que cobre o fallback: `ApiGatewayControllerTest.getOwnerDetails_withServiceError`.

**Passo a passo técnico:**
```mermaid
sequenceDiagram
  participant Front as Front-end
  participant GW as api-gateway
  participant CS as customers-service
  participant VS as visits-service
  Front->>GW: GET /api/gateway/owners/{ownerId}
  GW->>CS: GET /owners/{ownerId}
  CS-->>GW: 200 Owner + pets
  GW->>VS: GET /pets/visits?petId=...(todos os pets)
  alt visits-service responde a tempo
    VS-->>GW: 200 visitas
    GW-->>Front: 200 Owner + pets + visitas
  else timeout ou erro (circuit breaker aberto)
    GW-->>Front: 200 Owner + pets, visitas vazias
  end
```

**Regras que mudam o resultado:** timeout de 10 s do circuit breaker [R07](6-referencia.md#regras-de-negócio). Histórico vazio e histórico indisponível são indistinguíveis para o usuário.

---

## Consultar veterinários

**Participantes:** `api-gateway`, `vets-service`
> **Em resumo:** lista simples da equipe clínica e suas especialidades; a resposta é cacheada em
> memória no `vets-service`, então uma mudança recente pode não aparecer de imediato.

**Em linguagem de negócio:**
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Dono/recepção | Consulta a lista de veterinários | Lista exibida com nome e especialidades | Resposta pode vir do cache (`@Cacheable("vets")`) |

| Entrada | Saída | Observação |
|---|---|---|
| `GET /api/vet/vets` no `api-gateway` | `200` com veterinários e especialidades | Proxy transparente para `GET /vets` no `vets-service` (`StripPrefix=2`); resposta pode vir do cache `vets` ([R09](6-referencia.md#regras-de-negócio)) |

---

## Conversar com o assistente de IA

**Participantes:** `api-gateway`, `genai-service`, `customers-service`
> **Em resumo:** o usuário manda uma mensagem em linguagem natural; o `genai-service` decide, via
> tool calling do LLM, se precisa listar donos, listar veterinários (busca semântica), ou criar
> dono/pet — chamando `customers-service` diretamente, sem passar pelo `api-gateway`.

**Em linguagem de negócio:**
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Usuário | Envia uma pergunta ou pedido em texto livre | Pergunta recebida | Mantém memória das mensagens anteriores (capacidade a confirmar) da conversa |
| 2 | Assistente de IA | Decide se precisa de dados (lista de donos, veterinários) ou de uma ação (criar dono/pet) | Ferramenta certa é chamada | Só usa as 4 ferramentas expostas em `PetclinicTools` |
| 3 | Assistente de IA | Responde com base no resultado da ferramenta (ou direto, se não precisar de dados) | Resposta enviada ao usuário | Se não souber a resposta, deve dizer que não sabe e perguntar de volta (instrução do prompt de sistema) |

**Quem orquestra:** o próprio LLM decide a sequência de chamadas via tool calling (não há um fluxo fixo programado); `genai-service` é o único componente que fala com `customers-service` nessa jornada, resolvendo o endereço por `DiscoveryClient` (Eureka) em vez de passar pelo `api-gateway`.

**Passo a passo técnico:**
```mermaid
sequenceDiagram
  participant Front as Front-end/Cliente
  participant GW as api-gateway
  participant GEN as genai-service
  participant LLM as OpenAI/Azure OpenAI
  participant CS as customers-service
  Front->>GW: POST /api/genai/chatclient {pergunta}
  GW->>GEN: POST /chatclient {pergunta}
  GEN->>LLM: prompt + histórico + ferramentas disponíveis
  alt LLM decide chamar uma ferramenta
    LLM-->>GEN: pedido de tool call (ex.: addPetToOwner)
    GEN->>CS: POST /owners/{ownerId}/pets
    CS-->>GEN: 201 Pet criado (ou 404)
    GEN->>LLM: resultado da ferramenta
    LLM-->>GEN: resposta final em texto
  else LLM responde direto
    LLM-->>GEN: resposta em texto
  end
  GEN-->>GW: 200 resposta
  GW-->>Front: 200 resposta
  Note over GEN: Se o LLM ou a chamada falhar,<br/>responde "Chat is currently unavailable."
```

**Regras que mudam o resultado:** tipos de pet aceitos pela IA [R05](6-referencia.md#regras-de-negócio); capacidade da memória não confirmada [Q03](6-referencia.md#pendências).

**Fontes:** `ApiGatewayController.java`, `CustomersServiceClient.java`, `VisitsServiceClient.java`, `FallbackController.java`, `ApiGatewayApplication.java` (timeout do circuit breaker), `application.yml` do api-gateway (rotas, retry, circuit breaker do genai); `OwnerResource.java`, `PetResource.java`, `VisitResource.java`, `VetResource.java`; `PetclinicChatClient.java`, `PetclinicTools.java`, `AIDataProvider.java` (fluxo do chatbot e tool calling); `VetsServiceApplication`/`CacheConfig` (cache de vets, mencionado no serviço). Sequências reconstruídas a partir do código (não há diagramas de sequência nem OpenAPI no repositório).
