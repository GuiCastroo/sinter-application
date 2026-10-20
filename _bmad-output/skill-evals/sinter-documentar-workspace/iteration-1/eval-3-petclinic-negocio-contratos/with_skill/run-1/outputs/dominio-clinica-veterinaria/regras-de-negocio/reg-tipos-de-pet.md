---
id: reg-tipos-de-pet
kind: rule
subject: rule:tipos-de-pet
camada: 0
status: proposed
realiza: []
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/PetclinicTools.java#L58-L62; spring-petclinic-customers-service/src/main/resources/db/mysql/data.sql
    version: aefaf7f
    extraction: extracted
---

# Um pet só pode ter um dos tipos cadastrados
Todo pet deve ter um `typeId` que exista na tabela `types`/entidade `PetType`. Os valores observados (via `data.sql` e a descrição da tool `addPetToOwner` do `genai-service`) são: 1=cat, 2=dog, 3=lizard, 4=snake, 5=bird, 6=hamster.

## Onde está implementada
- `spring-petclinic-customers-service` — `PetResource.processCreationForm`/`save` (busca o `PetType` por id; se não encontrar, o pet é salvo sem tipo — `ifPresent`, sem erro explícito)
- `spring-petclinic-genai-service` — `PetclinicTools.addPetToOwner`, documentação da tool cita os 6 ids válidos

## Conflito
Não há validação explícita no `customers-service` que rejeite um `typeId` inexistente — `petRepository.findPetTypeById(...).ifPresent(pet::setType)` simplesmente não define o tipo se o id não existir, deixando `pet.getType()` nulo. Isso pode conflitar com a expectativa de negócio de que "todo pet tem um tipo válido". **A confirmar com o time de desenvolvimento** se isso é um bug ou comportamento aceito.
