---
id: reg-telefone-formato
kind: rule
subject: rule:telefone-formato
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/model/Owner.java#L58-L60; OwnerRequest.java
    version: aefaf7f
    extraction: extracted
---

# Telefone do tutor deve ter até 12 dígitos, sem formatação
O telefone do tutor é validado com `@Digits(fraction = 0, integer = 12)` — só dígitos, sem parte fracionária, no máximo 12 caracteres numéricos. O campo também é obrigatório (`@NotBlank`).

## Onde está implementada
- `spring-petclinic-customers-service` — entidade `Owner` e DTO `OwnerRequest`
- `spring-petclinic-genai-service` — o `record OwnerRequest` da tool `addOwnerToPetclinic` replica a mesma regra (`@Digits(fraction = 0, integer = 12)`)
