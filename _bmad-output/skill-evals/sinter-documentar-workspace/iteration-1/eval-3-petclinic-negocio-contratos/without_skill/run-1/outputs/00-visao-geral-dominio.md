# Domínio: Clínica Veterinária (Spring PetClinic Microservices)

> Fonte analisada: `spring-petclinic-microservices` (repositório local, somente leitura).
> Este documento é o índice do "repo do domínio" — reúne capacidades de negócio, contratos de API e modelo de dados de cada serviço que compõe o domínio "Clínica Veterinária".

## 1. O que é o domínio

O sistema implementa a operação de uma clínica veterinária: cadastro de tutores (owners) e seus animais (pets), agenda de visitas/consultas, cadastro de veterinários com especialidades, e um assistente conversacional (GenAI) que apoia a equipe da clínica a consultar e alimentar esses dados em linguagem natural.

É uma decomposição em microsserviços do clássico Spring PetClinic, usando Spring Cloud (Config Server, Eureka Discovery, Gateway, Circuit Breaker) e Spring AI.

## 2. Mapa de serviços

| Serviço | Papel no domínio | Porta padrão | Tipo |
|---|---|---|---|
| `spring-petclinic-customers-service` | Sistema de registro de Tutores (Owners), Pets e Tipos de Pet | 8081 | Negócio (core) |
| `spring-petclinic-vets-service` | Sistema de registro de Veterinários e Especialidades | 8083 | Negócio (core) |
| `spring-petclinic-visits-service` | Sistema de registro de Visitas/Consultas de um Pet | 8082 | Negócio (core) |
| `spring-petclinic-genai-service` | Assistente conversacional (chat) sobre o domínio, com ferramentas (tools) que chamam customers-service e um vector store de veterinários | 8084 | Negócio (suporte / IA) |
| `spring-petclinic-api-gateway` | Front-end (UI AngularJS) + BFF/API Gateway que agrega Owner + Pets + Visits para a tela do tutor, e roteia `/api/**` para os serviços | 8080 | Infraestrutura / Experiência |
| `spring-petclinic-discovery-server` | Service Registry (Eureka) | 8761 | Infraestrutura |
| `spring-petclinic-config-server` | Configuração centralizada (Spring Cloud Config) | 8888 | Infraestrutura |
| `spring-petclinic-admin-server` | Observabilidade/administração (Spring Boot Admin) | 9090 | Infraestrutura |

Serviços auxiliares fora do código Java: Zipkin (tracing, porta 9411), Prometheus (9091) e Grafana (3030) — definidos em `docker-compose.yml` e `docker/`.

## 3. Como o domínio se conecta (visão de integração)

```mermaid
flowchart LR
    subgraph Cliente
        UI[AngularJS UI]
    end

    UI -->|HTTP /api/*| GW[api-gateway]

    GW -->|Path=/api/customer/** StripPrefix=2| CUST[customers-service]
    GW -->|Path=/api/vet/** StripPrefix=2| VET[vets-service]
    GW -->|Path=/api/visit/** StripPrefix=2| VIS[visits-service]
    GW -->|Path=/api/genai/** StripPrefix=2 + CircuitBreaker| GENAI[genai-service]

    GW -->|GET /api/gateway/owners/{id}\n(WebClient lb://customers-service)| CUST
    GW -->|GET /api/gateway/owners/{id}\n(WebClient lb://visits-service, com Circuit Breaker)| VIS

    GENAI -->|RestClient via Eureka DiscoveryClient\nGET/POST /owners...| CUST
    GENAI -->|WebClient no startup\nGET /vets| VET
    GENAI -.->|vector store (RAG)\nSimpleVectorStore / vectorstore.json| GENAI

    CUST -.->|referencia lógica pet_id, sem FK física| VIS

    CUST --- DISC[discovery-server / Eureka]
    VET --- DISC
    VIS --- DISC
    GENAI --- DISC
    GW --- DISC

    CUST --- CFG[config-server]
    VET --- CFG
    VIS --- CFG
    GENAI --- CFG
    GW --- CFG
    DISC --- CFG

    ADM[admin-server] -.->|monitora via Eureka| DISC
```

Pontos-chave da integração:
- Toda comunicação síncrona de negócio entre serviços é feita via HTTP REST, resolvendo o host lógico pelo nome registrado no Eureka (`lb://customers-service`, `http://vets-service/`, `discoveryClient.getInstances("customers-service")`).
- Não há mensageria/eventos assíncronos no código analisado — toda integração é request/response síncrona (WebClient reativo no gateway, RestClient bloqueante no genai-service).
- `visits-service` guarda apenas `pet_id` (inteiro), sem chave estrangeira física para a tabela `pets` de `customers-service` — o vínculo Pet↔Visita é uma referência lógica entre bancos de dados distintos (consistência eventual/acoplamento fraco de dados, e não de schema).
- O `api-gateway` é o único serviço que agrega dados de dois serviços de negócio (customers + visits) numa única resposta (`GET /api/gateway/owners/{ownerId}`), com Circuit Breaker para tolerar falha do visits-service (retorna lista de visitas vazia).
- O `genai-service` só integra com `customers-service` (leitura/escrita de Owners e Pets) e com `vets-service` (somente leitura, e apenas uma vez no startup para popular o vector store). Ele não conversa diretamente com `visits-service`.

## 4. Documentos deste repositório de domínio

- Capacidades de negócio: `01-capacidades-negocio.md`
- Contratos de API por serviço:
  - `02-contrato-api-customers-service.md`
  - `02-contrato-api-vets-service.md`
  - `02-contrato-api-visits-service.md`
  - `02-contrato-api-genai-service.md`
  - `02-contrato-api-gateway.md`
- Modelo de dados por serviço:
  - `03-modelo-dados-customers-service.md`
  - `03-modelo-dados-vets-service.md`
  - `03-modelo-dados-visits-service.md`
  - `03-modelo-dados-genai-service.md`
- Serviços de infraestrutura de suporte: `04-servicos-infraestrutura.md`
- Glossário do domínio: `05-glossario.md`

## 5. Stack técnica observada

- Java 17, Spring Boot `4.0.1` (spring-boot-starter-parent), Spring Cloud `2025.1.0`.
- Persistência: Spring Data JPA + HSQLDB (perfil de desenvolvimento/testes, `db/hsqldb`) ou MySQL (perfil `mysql`, `db/mysql`), scripts `schema.sql`/`data.sql` por serviço.
- Comunicação: Spring Cloud Gateway (WebFlux reativo) no api-gateway; Spring Web MVC (bloqueante) em customers/vets/visits-service.
- Resiliência: Spring Cloud Circuit Breaker (Resilience4j) no api-gateway e nas rotas do gateway para `genai-service`.
- Observabilidade: Micrometer + `@Timed`, Spring Boot Admin, Prometheus, Grafana, Zipkin.
- IA: Spring AI (`ChatClient`, tools/function-calling, `SimpleVectorStore` para RAG sobre dados de veterinários), com suporte a OpenAI e Azure OpenAI como provedores de modelo.
