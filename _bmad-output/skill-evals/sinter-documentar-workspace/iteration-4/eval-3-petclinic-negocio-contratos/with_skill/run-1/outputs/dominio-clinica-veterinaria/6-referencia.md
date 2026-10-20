# Referência: Clínica Veterinária

> **Em resumo:** definições únicas do domínio — glossário, regras com ID, padrões, como rodar e
> testar uma mudança, e um só registro de pendências. Decisões de arquitetura ficam em
> [Arquitetura](2-arquitetura.md#decisões-que-moldam).

## Nesta página

| Seção |
|---|
| [Glossário](#glossário) |
| [Regras de negócio](#regras-de-negócio) |
| [Padrões](#padrões) |
| [Como começar](#como-começar) |
| [Pendências](#pendências) |

## Glossário
| Termo | Definição |
|---|---|
| Owner (Dono) | Pessoa responsável por um ou mais pets, com nome, endereço, cidade e telefone; entidade em `customers-service` |
| Pet | Animal de um dono; entidade em `customers-service` |
| PetType | Categoria do pet (cat, dog, ...); entidade em `customers-service` |
| Visit | Registro histórico de atendimento a um pet, com data e descrição livre; entidade em `visits-service` |
| Vet | Veterinário; entidade em `vets-service` |
| Specialty | Especialidade de um veterinário; entidade em `vets-service` |
| Tool calling | Mecanismo do LLM (Spring AI) para chamar funções Java durante a conversa |
| Circuit breaker | Padrão de resiliência (Resilience4j) que corta uma chamada instável e usa um caminho alternativo |
| Eureka | Registro de serviços (Spring Cloud Netflix) usado para descoberta por nome |
| Config Server | Serviço que entrega configuração centralizada, lida de um repositório Git |
| Ficha do dono | Visão agregada do dono com seus pets e o histórico de visitas de cada um |
| Assistente de IA | Chatbot que responde perguntas e executa ações (listar donos/veterinários, cadastrar dono/pet) via linguagem natural |

## Regras de negócio
| ID | Regra | Valor atual | Onde está implementada |
|---|---|---|---|
| R01 | Campos obrigatórios do dono | firstName, lastName, address, city, telephone | `Owner.java`, `OwnerRequest.java` (`@NotBlank`) |
| R02 | Formato do telefone | Só dígitos, até 12 caracteres | `OwnerRequest.java`, `PetclinicTools.java` (`@Digits(fraction=0, integer=12)`) |
| R03 | Nome do pet obrigatório | Mínimo 1 caractere | `PetRequest.java` (`@Size(min=1)`) |
| R04 | Tamanho da descrição da visita | Até 8192 caracteres | `Visit.java` (`@Size(max=8192)`) |
| R05 | Tipos de pet aceitos pelo assistente de IA | 1=cat, 2=dog, 3=lizard, 4=snake, 5=bird, 6=hamster | `PetclinicTools.java` (descrição da tool `addPetToOwner`) |
| R06 | Memória de conversa do chatbot | Capacidade não confirmada ([Q03](#pendências)); `.order(10)` ordena o advisor, não limita a memória | `PetclinicChatClient.java` (`MessageChatMemoryAdvisor.order(10)`) |
| R07 | Timeout do circuit breaker do gateway | 10 segundos | `ApiGatewayApplication.java` (`TimeLimiterConfig`) |
| R08 | Retry do gateway em rotas `/api/**` | 1 tentativa, só para `POST` com resposta `SERVICE_UNAVAILABLE` | `spring-petclinic-api-gateway/src/main/resources/application.yml` |
| R09 | Cache da lista de veterinários | Cache nomeado `vets` (Caffeine) | `vets-service` `application.yml` (`spring.cache.cache-names: vets`), `VetResource.java` (`@Cacheable`) |

R07, R08 e R09 são regras técnicas; entram aqui pelo efeito visível: ficha sem histórico após 10 s, uma nova tentativa em `POST` e lista de veterinários possivelmente desatualizada.

## Padrões
- **Camadas por serviço:** `model` (entidades JPA + repositórios), `web` (controllers REST + DTOs de request), seguindo o pacote `org.springframework.samples.petclinic.<serviço>`.
- **Banco:** HSQLDB em memória por padrão (perfil default), MySQL via perfil `mysql`; scripts em `src/main/resources/db/{hsqldb,mysql}/{schema,data}.sql`.
- **Métricas:** anotação `@Timed` do Micrometer em cada controller principal (`petclinic.owner`, `petclinic.pet`, `petclinic.visit`), expostas via Actuator/Prometheus.
- **Resiliência:** `spring-cloud-starter-circuitbreaker-reactor-resilience4j` no gateway e no genai-service; `chaos-monkey-spring-boot` em customers/vets/visits-service para testes de falha controlada.
- **Rastreamento:** `spring-boot-starter-zipkin` em todos os serviços de aplicação, relatando ao `tracing-server` (Zipkin).
- **Build:** Maven multi-módulo (`pom.xml` raiz + um módulo por serviço), Java 17, imagens Docker via perfil Maven `buildDocker`.

## Como começar
**Rodar localmente:**
1. Subir `config-server` e `discovery-server` primeiro (`../mvnw spring-boot:run` em cada um, ou usar `./scripts/run_all.sh`).
2. Subir os demais serviços (`customers`, `visits`, `vets`, `genai`, `api-gateway`, `admin`).
3. Acessar o front-end em `http://localhost:8080/`; Eureka em `:8761`; Admin em `:9090`; Zipkin em `:9411`.
4. Alternativa: `docker compose up` depois de construir as imagens com `./mvnw clean install -P buildDocker` (ou usar as imagens publicadas em `springcommunity/*`).

**Testar uma mudança (exemplo real):** o fallback da ficha do dono é coberto por
`ApiGatewayControllerTest.getOwnerDetails_withServiceError` (simula erro no `visits-service` e espera
a ficha com visitas vazias). Na raiz: `./mvnw -pl spring-petclinic-api-gateway test -Dtest=ApiGatewayControllerTest`;
resultado esperado: `BUILD SUCCESS` com os dois testes passando. Outros testes por serviço:
`PetResourceTest`, `VisitResourceTest`, `VetResourceTest`. O CI roda o build Maven completo
(`.github/workflows/maven-build.yml`). Plano de carga JMeter em
`spring-petclinic-api-gateway/src/test/jmeter/petclinic_test_plan.jmx`. *Comandos não executados nesta revisão.*

**Onde fica cada coisa:**
- Regras de dono/pet → `spring-petclinic-customers-service/.../web/` e `.../model/`.
- Regras de visita → `spring-petclinic-visits-service/.../web/` e `.../model/`.
- Regras de veterinário → `spring-petclinic-vets-service/.../web/` e `.../model/`.
- Comportamento do chatbot e das ações da IA → `spring-petclinic-genai-service/.../PetclinicChatClient.java`, `PetclinicTools.java`, `AIDataProvider.java`.
- Roteamento e agregação de borda → `spring-petclinic-api-gateway/.../application.yml` e `.../ApiGatewayController.java`.

**As 3 mudanças mais comuns (dedução a partir da estrutura do código):**
1. Adicionar um campo ao dono/pet → no `customers-service`: entidade JPA, `OwnerRequest`, `OwnerEntityMapper` e `schema.sql` (hsqldb e mysql). Para o campo chegar à tela e ao chat: `OwnerDetails` do `api-gateway`, templates `owner-details`/`owner-form` em `static/scripts/`, e `OwnerDetails`/`PetclinicTools` do `genai-service`, se o chat precisar do campo.
2. Adicionar uma nova ferramenta ao assistente de IA → método `@Tool` em `PetclinicTools.java` + método correspondente em `AIDataProvider.java`.
3. Expor um novo agregador na borda → método no `ApiGatewayController` + cliente `WebClient` correspondente + rota em `application.yml` se for proxy simples.

**Como publicar:** `./mvnw clean install -P buildDocker` gera as imagens; `scripts/tagImages.sh` e `scripts/pushImages.sh` publicam num registro Docker configurado via `REPOSITORY_PREFIX` (o CI de build/teste é `.github/workflows/maven-build.yml`; não há pipeline de deploy no repositório).

## Pendências
Registro único de perguntas em aberto. Fatos confirmados não entram aqui. Nenhum conflito entre
fontes foi encontrado.

| ID | Tipo | Assunto | Pergunta | Impacto | Evidência | Quem responde |
|---|---|---|---|---|---|---|
| Q01 | Produto | Escopo e papéis | Agendamento com confirmação, cobrança e papéis de usuário (recepção, veterinário, dono) entram no escopo? | Hoje qualquer usuário faz qualquer ação; não há segurança no código | Ausência de Spring Security e de agendamento | Produto |
| Q02 | Arquitetura | Produção | Em produção, os três bancos MySQL são instâncias separadas? Qual a topologia e a configuração efetiva? | Isolamento de dados e valores reais (portas, timeouts) desconhecidos | `db/mysql/schema.sql`, `spring-petclinic-microservices-config` (externo) | Arquitetura/operação |
| Q03 | Técnica | Memória do chat | Qual a capacidade efetiva do `ChatMemory`? | Não prometer "lembra as últimas N mensagens" | `PetclinicChatClient.java` (`.order(10)`) | Dev |
| Q04 | Técnica | Cache e config | Qual o TTL do cache de veterinários? Como os serviços sobem sem o Config Server (`optional:configserver`)? | Mudanças podem demorar a aparecer; defaults desconhecidos | `VetResource.java`, `application.yml` | Tech lead |
| Q05 | Produto | Tipos de pet na IA | A lista de tipos aceitos pelo assistente deve ser validada no `customers-service`? | Hoje o chat aceita qualquer `typeId` inteiro | `PetclinicTools.java` | Produto + dev |
| Q06 | Arquitetura | Rota do chat | O `genai-service` deve passar a chamar `customers-service` via gateway? | Consistência de observabilidade e segurança | `AIDataProvider.java` | Arquitetura |
| Q07 | Produto | Indicadores | Quais indicadores de negócio importam? | Só há métricas técnicas | `@Timed` nos controllers | Produto |

**Segredos (só localização, valor não copiado):** `OPENAI_API_KEY`, `AZURE_OPENAI_KEY` e
`AZURE_OPENAI_ENDPOINT` em `spring-petclinic-genai-service/src/main/resources/application.yml`
(linhas 9, 17, 18, 25), repassadas pelo `docker-compose.yml` ao container `genai-service`.

**Fontes:** fontes citadas nas páginas anteriores; busca por `CODEOWNERS`, `docs/adr`, `decisions/`
e Spring Security (nenhum encontrado); `pom.xml` raiz e de cada módulo; `scripts/pushImages.sh`,
`scripts/tagImages.sh`; `.github/workflows/maven-build.yml`.
