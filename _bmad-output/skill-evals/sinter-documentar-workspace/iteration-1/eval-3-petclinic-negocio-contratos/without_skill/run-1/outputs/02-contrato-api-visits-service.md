# Contrato de API — visits-service

- Base path local: `http://localhost:8082`
- Via api-gateway: `http://<gateway>/api/visit/**` (`StripPrefix=2`)
- Controller-fonte: `VisitResource.java`
- Formato: JSON (Spring MVC / `@RestController`)
- Métricas: timer Micrometer `petclinic.visit` em todos os endpoints.

## `POST owners/*/pets/{petId}/visits` — Registrar visita

- Path param: `petId` (inteiro, mínimo 1). O segmento `owners/*` não é validado.
- **Request body** (`Visit`, validado com `@Valid`):
```json
{
  "date": "yyyy-MM-dd (opcional; padrão = data/hora atual do servidor)",
  "description": "string, até 8192 caracteres",
  "petId": "int (sobrescrito pelo path param no servidor)"
}
```
- **Response:** `201 Created` — corpo é a entidade `Visit` persistida (com `id` gerado).
- Observação: o `petId` do corpo é sobrescrito pelo `petId` da URL antes de salvar (`visit.setPetId(petId)`), então o valor enviado no corpo é ignorado para esse fim.

## `GET owners/*/pets/{petId}/visits` — Consultar visitas de um pet

- Path param: `petId` (mínimo 1).
- **Response:** `200 OK` com array de `Visit`.

## `GET pets/visits?petId=1,2,3` — Consultar visitas de múltiplos pets

- Query param: `petId` — lista de inteiros, repetível ou separada por vírgula (`@RequestParam List<Integer>`).
- **Response:** `200 OK`:
```json
{
  "items": [
    { "id": "int", "date": "yyyy-MM-dd", "description": "string", "petId": "int" }
  ]
}
```
- Usado para busca em lote, evitando N chamadas para montar o histórico de vários pets de uma vez.

## Consumidores conhecidos deste contrato

- `spring-petclinic-api-gateway` (`VisitsServiceClient`): `GET http://visits-service/pets/visits?petId=...` (WebClient, hostname fixo `http://visits-service/` resolvido via service discovery/load balancer), usado por `ApiGatewayController.getOwnerDetails` para montar a ficha do tutor. Esta chamada é protegida por Circuit Breaker (`getOwnerDetails`) — em caso de falha, o gateway trata como "sem visitas" em vez de propagar o erro.
- Nenhuma chamada observada partindo de `genai-service` para este serviço no código analisado.

## Observação de contrato

Não existe endpoint de atualização (`PUT`) nem exclusão (`DELETE`) de visita — o histórico de visitas é apenas append-only pela API pública atual.
