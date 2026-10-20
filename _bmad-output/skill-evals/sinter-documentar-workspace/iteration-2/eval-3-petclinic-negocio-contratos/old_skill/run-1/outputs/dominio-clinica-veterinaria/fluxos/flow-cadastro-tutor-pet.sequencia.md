---
id: flow-cadastro-tutor-pet-sequencia
kind: flow
subject: flow:cadastro-tutor-pet:sequencia
camada: 3
status: proposed
realiza: [flow-cadastro-tutor-pet]
realizado-por: [ctr-customers-post-owners, ctr-customers-post-pet, ctr-customers-get-pettypes]
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/OwnerResource.java; PetResource.java
    version: aefaf7f
    extraction: extracted
---

# Cadastro de tutor e pet: sequência técnica
Realiza as etapas do [fluxo macro](./flow-cadastro-tutor-pet.md).

## Diagrama
```mermaid
sequenceDiagram
  participant UI as Frontend (AngularJS)
  participant GW as api-gateway
  participant CUST as customers-service

  UI->>GW: POST /api/customer/owners (dados do tutor)
  GW->>CUST: POST /owners (StripPrefix=2)
  alt dados válidos
    CUST-->>GW: 201 Created (owner com id)
    GW-->>UI: 201 Created
  else campo obrigatório ausente
    CUST-->>GW: 400 Bad Request (Bean Validation)
    GW-->>UI: 400 repassado
  end

  UI->>GW: GET /api/customer/petTypes
  GW->>CUST: GET /petTypes
  CUST-->>GW: 200 lista de tipos
  GW-->>UI: 200 repassado

  UI->>GW: POST /api/customer/owners/{ownerId}/pets
  GW->>CUST: POST /owners/{ownerId}/pets (StripPrefix=2)
  alt owner existe
    CUST-->>GW: 201 Created (pet)
    GW-->>UI: 201 Created
  else owner não encontrado
    CUST-->>GW: erro (ResourceNotFoundException)
    GW-->>UI: erro repassado
  end
```

## Passos
### Passo 1
`api-gateway` recebe a requisição do frontend na rota `/api/customer/**` e a repassa, via Eureka (`lb://customers-service`) e `StripPrefix=2`, para `POST /owners` no `customers-service`. Ver contrato [ctr-customers-post-owners](../sistemas/customers-service/contratos/ctr-customers-post-owners.md).

### Passo 2
Antes de cadastrar o pet, o frontend consulta `GET /petTypes` para popular a lista de tipos válidos (ver [ctr-customers-get-pettypes](../sistemas/customers-service/contratos/ctr-customers-get-pettypes.md)). Em seguida, envia `POST /owners/{ownerId}/pets` (ver [ctr-customers-post-pet](../sistemas/customers-service/contratos/ctr-customers-post-pet.md)).

### Caminho de erro
- Se o `ownerId` informado não existir, `customers-service` lança `ResourceNotFoundException` — o `api-gateway` não trata esse erro de forma especial nesta rota (ele não passa pelo `ApiGatewayController` de agregação, é uma rota simples do Spring Cloud Gateway), então o erro é repassado como está ao frontend. **Inferido**: o formato exato do corpo de erro não foi confirmado nas fontes lidas.
- Falha de validação (`@NotBlank`, `@Digits`) resulta em `400` do handler padrão do Spring, antes mesmo de chegar à lógica de negócio.
