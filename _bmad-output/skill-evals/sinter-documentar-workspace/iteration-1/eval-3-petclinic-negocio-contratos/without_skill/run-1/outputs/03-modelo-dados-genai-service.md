# Modelo de Dados — genai-service

Este serviço não possui banco relacional próprio. Ele mantém dois tipos de estado:

1. **DTOs de domínio** (réplicas locais dos contratos de `customers-service`/`vets-service`/`visits-service`, usadas apenas para desserializar/serializar chamadas HTTP e respostas das tools de IA — não é armazenamento persistente).
2. **Vector store de veterinários** (`SimpleVectorStore`, persistido em `vectorstore.json`), usado para busca semântica (RAG).

## 1. DTOs de domínio (`org.springframework.samples.petclinic.genai.dto`)

| DTO | Campos | Espelha o modelo de |
|---|---|---|
| `OwnerDetails` | `id, firstName, lastName, address, city, telephone, pets: List<PetDetails>` | `customers-service` (Owner) |
| `PetDetails` | `id, name, birthDate, type: PetType, visits: List<VisitDetails>` | `customers-service` (Pet) + `visits-service` (Visit) |
| `PetRequest` | `id, birthDate, name, typeId` | payload de criação de pet em `customers-service` |
| `PetType` | `name` (sem `id` — diferente do modelo real de `customers-service`, que tem `id` + `name`) | `customers-service` (PetType), de forma simplificada |
| `Vet` | `id, firstName, lastName, specialties: Set<Specialty>` | `vets-service` (Vet) |
| `Specialty` | `id, name` | `vets-service` (Specialty) |
| `VisitDetails` | `id, petId, date, description` | `visits-service` (Visit) |

Estes DTOs são a "visão do assistente de IA" sobre o domínio — mantidos manualmente em código, e não gerados a partir de um contrato compartilhado, o que é um risco de desalinhamento caso os contratos reais mudem (ex.: `PetType` aqui não tem `id`, diferente do `PetType` real).

## 2. Vector store de veterinários (RAG)

- Tecnologia: `org.springframework.ai.vectorstore.SimpleVectorStore`, persistido como JSON em `src/main/resources/vectorstore.json` (formato de exemplo abaixo).
- Estrutura de cada entrada (chave = UUID do documento):
```json
{
  "<uuid>": {
    "text": "{id=2, firstName=Helen, lastName=Leary, specialties=[{id=1, name=radiology}]}",
    "embedding": [0.0127, 0.0346, "... vetor de ponto flutuante ..."]
  }
}
```
- Cada "documento" representa **um veterinário** (serializado como texto livre a partir do objeto `Vet` retornado por `vets-service`), com seu vetor de embedding associado.
- **Origem dos dados:** gerado a partir de `GET /vets` em `vets-service`, uma única vez, no primeiro start sem `vectorstore.json` existente (ver `02-contrato-api-genai-service.md`).
- **Ciclo de vida:** não há atualização incremental — o índice reflete o estado dos veterinários no momento em que foi gerado; alterações posteriores no cadastro de veterinários não aparecem nas buscas de IA até uma reindexação manual (apagar o arquivo e reiniciar o serviço).

## 3. Memória de conversa (Chat Memory)

- `ChatMemory` (Spring AI) mantém o histórico de mensagens por conversa para dar contexto ao modelo (usado via `MessageChatMemoryAdvisor`, ordem 10, no `PetclinicChatClient`).
- Não foi encontrada, no código revisado, configuração explícita de um backend persistente (ex.: banco de dados) para essa memória — não é abordado em detalhe neste levantamento por não haver entidade/schema correspondente no código-fonte principal analisado.
