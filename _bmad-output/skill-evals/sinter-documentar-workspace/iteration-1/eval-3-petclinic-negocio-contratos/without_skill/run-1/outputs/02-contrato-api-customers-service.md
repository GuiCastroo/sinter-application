# Contrato de API — customers-service

- Base path local: `http://localhost:8081`
- Via api-gateway: `http://<gateway>/api/customer/**` (prefixo `/api/customer` é removido pelo gateway — `StripPrefix=2`)
- Controllers-fonte: `OwnerResource.java`, `PetResource.java`
- Formato: JSON (Spring MVC / `@RestController`)
- Métricas: todos os endpoints de `OwnerResource` têm timer Micrometer `petclinic.owner`; os de `PetResource`, `petclinic.pet`.

## Owners

### `POST /owners` — Cadastrar tutor
Cria um novo tutor.

**Request body** (`OwnerRequest`):
```json
{
  "firstName": "string (obrigatório)",
  "lastName": "string (obrigatório)",
  "address": "string (obrigatório)",
  "city": "string (obrigatório)",
  "telephone": "string numérico, até 12 dígitos (obrigatório)"
}
```

**Response:** `201 Created` — corpo é a entidade `Owner` persistida (inclui `id` e `pets: []`).

### `GET /owners/{ownerId}` — Consultar tutor
- Path param: `ownerId` (inteiro, mínimo 1).
- **Response:** `200 OK` com `Optional<Owner>` serializado (objeto `Owner` ou corpo vazio/`null` se não existir) — inclui a lista `pets` do tutor.
- Não há tratamento explícito de 404 nesta ação (diferente de `updateOwner`/`PetResource`, que lançam `ResourceNotFoundException` → mapeado como erro de negócio).

### `GET /owners` — Listar tutores
- **Response:** `200 OK` com array de `Owner`.

### `PUT /owners/{ownerId}` — Atualizar tutor
- Path param: `ownerId` (mínimo 1).
- **Request body:** `OwnerRequest` (mesmo schema do POST, todos os campos novamente obrigatórios).
- **Response:** `204 No Content`.
- **Erros:** se `ownerId` não existir, lança `ResourceNotFoundException` ("Owner {id} not found").

## Pets

### `GET /petTypes` — Listar tipos de pet
- **Response:** `200 OK` com array de `PetType` (`{ "id": int, "name": string }`).

### `POST /owners/{ownerId}/pets` — Cadastrar pet para um tutor
- Path param: `ownerId` (mínimo 1).
- **Request body** (`PetRequest`):
```json
{
  "id": "int (ignorado na criação)",
  "birthDate": "yyyy-MM-dd",
  "name": "string (mínimo 1 caractere)",
  "typeId": "int (id de PetType existente)"
}
```
- **Response:** `201 Created` — corpo é a entidade `Pet` persistida.
- **Erros:** `ResourceNotFoundException` se `ownerId` não existir. Se `typeId` não existir, o pet é salvo sem tipo (busca é `Optional`, sem lançar erro).

### `PUT /owners/*/pets/{petId}` — Atualizar pet
- Path param: `petId` (o segmento `owners/*` na rota não é validado/usado para autorização — qualquer valor é aceito).
- **Request body:** `PetRequest` (o campo `id` do corpo é o identificador usado para localizar o pet, não o path — atenção: o path `{petId}` está declarado mas a implementação lê `petRequest.id()`).
- **Response:** `204 No Content`.
- **Erros:** `ResourceNotFoundException` se o pet não existir.

### `GET owners/*/pets/{petId}` — Detalhes de um pet
- Path param: `petId`.
- **Response:** `200 OK` com `PetDetails`:
```json
{
  "id": "long",
  "name": "string",
  "owner": "string (\"firstName lastName\")",
  "birthDate": "yyyy-MM-dd",
  "type": { "id": "int", "name": "string" }
}
```
- **Erros:** `ResourceNotFoundException` se o pet não existir.

## Erros

`ResourceNotFoundException` (não mapeado explicitamente para um `@ExceptionHandler` no código revisado) — comportamento de status HTTP depende do tratamento padrão do Spring Boot para exceções não capturadas (tipicamente `500`, a menos que anotada/mapeada em configuração não coberta por este código-fonte).

## Consumidores conhecidos deste contrato

- `spring-petclinic-api-gateway` (`CustomersServiceClient`): `GET http://customers-service/owners/{ownerId}` via WebClient com balanceamento de carga (`lb://`).
- `spring-petclinic-genai-service` (`AIDataProvider`): `GET /owners` (listar), `POST /owners` (cadastrar), `POST /owners/{ownerId}/pets` (cadastrar pet) — via `RestClient` apontando para a instância resolvida por `DiscoveryClient`.
