# Contrato de API — api-gateway

- Base path local: `http://localhost:8080`
- Controllers-fonte: `ApiGatewayController.java`, `FallbackController.java`
- Tecnologia: Spring Cloud Gateway (WebFlux, reativo)

O api-gateway tem dois papéis contratuais distintos: (1) roteador transparente para os serviços de negócio, e (2) um endpoint próprio de agregação (BFF) para a tela de detalhe do tutor.

## 1. Rotas de proxy (Spring Cloud Gateway)

Configuradas em `application.yml`, sem código Java de roteamento (declarativas):

| Rota (id) | Predicado | Destino | Filtros |
|---|---|---|---|
| `vets-service` | `Path=/api/vet/**` | `lb://vets-service` | `StripPrefix=2` |
| `visits-service` | `Path=/api/visit/**` | `lb://visits-service` | `StripPrefix=2` |
| `customers-service` | `Path=/api/customer/**` | `lb://customers-service` | `StripPrefix=2` |
| `genai-service` | `Path=/api/genai/**` | `lb://genai-service` | `StripPrefix=2`, `CircuitBreaker=name=genaiCircuitBreaker,fallbackUri=/fallback` |

Filtros globais (`default-filters`, aplicados a todas as rotas acima):
- `CircuitBreaker` nomeado `defaultCircuitBreaker`, com fallback em `forward:/fallback`.
- `Retry`: 1 tentativa adicional, apenas para respostas `SERVICE_UNAVAILABLE` e apenas em métodos `POST`.

Efeito de negócio: qualquer chamada `POST` do front-end que resulte em `503` do serviço de destino é automaticamente reexecutada uma vez antes de acionar o fallback.

## 2. `GET /api/gateway/owners/{ownerId}` — Ficha agregada do tutor (BFF)

Endpoint próprio do gateway (não é um proxy simples).

- Path param: `ownerId` (inteiro).
- **Orquestração:**
  1. Busca o tutor e seus pets em `customers-service`: `GET http://customers-service/owners/{ownerId}` (via `CustomersServiceClient`, `WebClient` com resolução por load balancer).
  2. Com os IDs dos pets do tutor, busca as visitas de todos eles em lote em `visits-service`: `GET http://visits-service/pets/visits?petId=<id1>,<id2>,...` (via `VisitsServiceClient`).
  3. Combina o resultado: cada pet do tutor recebe sua lista de `visits` preenchida a partir do resultado do passo 2.
- **Resiliência:** a chamada ao `visits-service` é envolvida por um Circuit Breaker nomeado `getOwnerDetails`. Se abrir (falha/timeout), o gateway substitui o resultado por uma lista de visitas vazia (`emptyVisitsForPets`), e a resposta é retornada normalmente sem visitas, em vez de falhar.
- **Response:** `200 OK` com `OwnerDetails`:
```json
{
  "id": "int",
  "firstName": "string",
  "lastName": "string",
  "address": "string",
  "city": "string",
  "telephone": "string",
  "pets": [
    {
      "id": "int",
      "name": "string",
      "birthDate": "string (yyyy-MM-dd)",
      "type": { "id": "int", "name": "string" },
      "visits": [
        { "id": "int", "petId": "int", "date": "string", "description": "string" }
      ]
    }
  ]
}
```

## 3. `POST /fallback` — Fallback padrão de circuito

- Acionado internamente pelo Gateway quando um circuito (`defaultCircuitBreaker` ou `genaiCircuitBreaker`) abre.
- **Response:** `503 Service Unavailable`, corpo: `"Chat is currently unavailable. Please try again later."`
- Observação: a mensagem de fallback é genérica para "chat", mesmo sendo o fallback padrão de qualquer rota — pode gerar mensagem enganosa se o circuito que abrir for o de `customers-service`, `vets-service` ou `visits-service` (não apenas o de `genai-service`).

## 4. UI estática

O mesmo serviço também serve a aplicação AngularJS (`src/main/resources/static/`) que consome as rotas acima como seu backend — não detalhado aqui por não ser um contrato de API de domínio, apenas front-end estático.

## Consumidores conhecidos

- UI AngularJS embutida (`owner-details.component.js`, `vet-list.component.js`, etc.) é a única consumidora conhecida deste contrato no código analisado.
