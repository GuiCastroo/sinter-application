# Contrato de API — vets-service

- Base path local: `http://localhost:8083`
- Via api-gateway: `http://<gateway>/api/vet/**` (`StripPrefix=2`)
- Controller-fonte: `VetResource.java`
- Formato: JSON (Spring MVC / `@RestController`)

## `GET /vets` — Listar veterinários

Único endpoint exposto por este serviço.

- **Response:** `200 OK` com array de `Vet`:
```json
[
  {
    "id": "int",
    "firstName": "string",
    "lastName": "string",
    "specialties": [
      { "id": "int", "name": "string" }
    ],
    "nrOfSpecialties": "int"
  }
]
```
- Especialidades vêm ordenadas por nome.
- **Cache:** resposta é cacheada sob a chave de cache `"vets"` (`@Cacheable`), habilitado apenas quando o perfil Spring ativo é `production` (`CacheConfig` com `@Profile("production")`). Em outros perfis (ex.: testes), a consulta sempre vai ao banco.
- Não há paginação, filtro por nome/especialidade, nem endpoints de escrita.

## Consumidores conhecidos deste contrato

- `spring-petclinic-genai-service` (`VectorStoreController`): `GET http://vets-service/vets`, executado uma única vez no evento `ApplicationStartedEvent`, para popular o vector store usado na busca semântica de veterinários (a menos que já exista `vectorstore.json` em classpath, caso em que este endpoint não é chamado).
- UI (via `api-gateway`, rota `/api/vet/**`) para a tela de listagem de veterinários.

## Observação de contrato

Como não há endpoint de escrita, qualquer necessidade de negócio para cadastrar/editar um veterinário ou associar especialidades precisa ser feita fora da API pública (ex.: diretamente no banco via `data.sql`/migração), o que é uma lacuna de contrato caso o negócio precise disso futuramente.
