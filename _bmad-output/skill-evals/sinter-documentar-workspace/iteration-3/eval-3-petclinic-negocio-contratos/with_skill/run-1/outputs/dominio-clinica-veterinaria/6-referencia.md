# Referência: Clínica Veterinária

> **Em resumo:** glossário, regras, decisões reconstruídas, padrões de código, como rodar
> localmente e as dúvidas em aberto por papel — para quem vai mexer no código ou decidir sobre
> ele sem reler tudo.

## Nesta página

| Seção |
|---|
| [Glossário](#glossário) |
| [Regras de negócio](#regras-de-negócio) |
| [Decisões](#decisões) |
| [Padrões](#padrões) |
| [Como começar](#como-começar) |
| [Dúvidas e perguntas](#dúvidas-e-perguntas) |
| [Dúvidas de contexto](#dúvidas-de-contexto) |
| [Perguntas para decisão](#perguntas-para-decisão) |
| [Evidências da revisão v3](#evidências-da-revisão-v3) |

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
| R06 | Memória de conversa do chatbot | Capacidade a confirmar; `.order(10)` ordena o advisor, não demonstra o limite da memória | `PetclinicChatClient.java` (`MessageChatMemoryAdvisor.order(10)`) |
| R07 | Timeout do circuit breaker do gateway | 10 segundos | `ApiGatewayApplication.java` (`TimeLimiterConfig`) |
| R08 | Retry do gateway em rotas `/api/**` | 1 tentativa, só para `POST` com resposta `SERVICE_UNAVAILABLE` | `spring-petclinic-api-gateway/src/main/resources/application.yml` |
| R09 | Cache da lista de veterinários | Cache nomeado `vets` (Caffeine) | `vets-service` `application.yml` (`spring.cache.cache-names: vets`), `VetResource.java` (`@Cacheable`) |

## Decisões
*(reconstruídas a partir do código; não há pasta `docs/adr` nem `decisions/` no repositório)*

| Contexto | Escolha | Consequência |
|---|---|---|
| Cada subdomínio de negócio precisava evoluir e escalar de forma independente | Um serviço Spring Boot por subdomínio (customers, visits, vets, genai), descobertos via Eureka | Chamadas entre serviços viram rede (latência, falha parcial); precisa de circuit breaker (ver `api-gateway`) |
| Front-end precisa de uma única origem de dados (dono + visitas) numa tela | `api-gateway` agrega no lado do servidor em vez de o front-end chamar dois serviços | Um ponto a mais de falha, mitigado com circuit breaker + fallback de dados vazios |
| Assistente de IA precisa de dados atualizados de donos/pets | `genai-service` chama `customers-service` direto via Eureka, sem passar pelo `api-gateway` | Caminho de escrita adicional fora do proxy central; exige que `genai-service` conheça o contrato de `customers-service` diretamente |
| Configuração não deveria ficar hardcoded em cada serviço | Config Server buscando de um repositório Git externo | Config real de produção não está neste repositório — quem consultar precisa acessar `spring-petclinic-microservices-config` |
| Consultar veterinários é uma leitura frequente e de baixa mudança | Cache em memória (`@Cacheable("vets")`) | Atraso possível entre mudança no banco e reflexo na API |

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

**Testes:** cada módulo tem seus próprios testes (`spring-boot-starter-test`, `spring-boot-starter-webmvc-test`/`webflux-test`); rodar via `../mvnw test` no módulo desejado. Há um plano de carga JMeter em `spring-petclinic-api-gateway/src/test/jmeter/petclinic_test_plan.jmx`.

**Onde fica cada coisa:**
- Regras de dono/pet → `spring-petclinic-customers-service/.../web/` e `.../model/`.
- Regras de visita → `spring-petclinic-visits-service/.../web/` e `.../model/`.
- Regras de veterinário → `spring-petclinic-vets-service/.../web/` e `.../model/`.
- Comportamento do chatbot e das ações da IA → `spring-petclinic-genai-service/.../PetclinicChatClient.java`, `PetclinicTools.java`, `AIDataProvider.java`.
- Roteamento e agregação de borda → `spring-petclinic-api-gateway/.../application.yml` e `.../ApiGatewayController.java`.

**As 3 mudanças mais comuns (dedução a partir da estrutura do código):**
1. Adicionar um campo ao dono/pet → entidade JPA + DTO de request/response + migração do `schema.sql` (hsqldb e mysql) no `customers-service`.
2. Adicionar uma nova ferramenta ao assistente de IA → método `@Tool` em `PetclinicTools.java` + método correspondente em `AIDataProvider.java`.
3. Expor um novo agregador na borda → método no `ApiGatewayController` + cliente `WebClient` correspondente + rota em `application.yml` se for proxy simples.

**Como publicar:** `./mvnw clean install -P buildDocker` gera as imagens; `scripts/tagImages.sh` e `scripts/pushImages.sh` publicam num registro Docker configurado via `REPOSITORY_PREFIX` *(a confirmar pipeline de CI/CD real de produção — só há o workflow `maven-build.yml` do GitHub Actions citado no badge do README para build/teste)*.

## Dúvidas e perguntas

**Segredos encontrados (só localização, valor não copiado):**
- `spring-petclinic-genai-service/src/main/resources/application.yml` (linhas 9, 17, 18, 25): variáveis `OPENAI_API_KEY`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT`.
- `docker-compose.yml` (serviço `genai-service`): repassa as mesmas variáveis ao container.

**Conflitos entre fontes:** nenhum encontrado — a lacuna principal é que a config real (portas, timeouts, credenciais) fica no repositório externo `spring-petclinic-microservices-config`.

As questões por papel estão reunidas em [Perguntas para decisão](#perguntas-para-decisão).

**Fontes:** consolidação das fontes citadas em `1-negocio.md`, `2-arquitetura.md`, `3-servicos.md`, `4-jornadas.md` e `5-infraestrutura.md`; busca adicional por `CODEOWNERS`, `docs/adr`, `decisions/` (nenhum encontrado); `pom.xml` raiz e de cada módulo (dependências e plugins de build/publicação); `scripts/pushImages.sh`, `scripts/tagImages.sh`, `README.md` (processo de publicação de imagens).

## Dúvidas de contexto

Topologia de produção, réplicas e valores efetivos de configuração permanecem desconhecidos: o repositório mostra o empacotamento Docker, e a configuração externa não foi fornecida. Fontes: `docker-compose.yml` e referências a `spring-petclinic-microservices-config`. Papéis dos usuários, exclusão e cancelamento aguardam decisão de produto (Q01).

## Perguntas para decisão

| ID | Papel | Pergunta |
|---|---|---|
| Q01 | Responsável pelo domínio | **PM/negócio:** este domínio deve ganhar agendamento com confirmação de horário e cobrança, ou isso fica fora de escopo permanentemente? Quais indicadores de negócio importam (retenção de donos, volume de visitas, uso do assistente de IA)? Existe distinção de papéis de usuário (recepção vs. veterinário vs. dono) a modelar? |
| Q02 | Responsável pelo domínio | **Arquiteto:** o `genai-service` deveria continuar chamando `customers-service` direto, ou passar a sempre passar pelo `api-gateway` por consistência de observabilidade/segurança? Em produção, os bancos MySQL de `customers-service`, `vets-service` e `visits-service` são instâncias separadas ou compartilham a mesma instância (mesmo nome de banco `petclinic`)? |
| Q03 | Responsável pelo domínio | **Tech lead:** qual é o TTL real do cache de veterinários? Qual o comportamento real do `config: import: optional:configserver:...` quando o Config Server está fora do ar (a app sobe com quais defaults)? Existe CI/CD de deploy automatizado além do workflow de build/teste do GitHub Actions? |
| Q04 | Tech lead | Qual é a capacidade efetiva do ChatMemory injetado? `.order(10)` define a ordem do advisor e não comprova uma janela de dez mensagens. |

## Evidências da revisão v3

`spring-petclinic-api-gateway/.../ApiGatewayController.java:56–60` busca dono antes das visitas; `spring-petclinic-api-gateway/src/main/resources/static/scripts/genai/chat.js:42` usa `/api/genai/chatclient`; `spring-petclinic-customers-service/.../PetResource.java:71` lê `petRequest.id()`; `spring-petclinic-genai-service/.../PetclinicChatClient.java:49` usa `.order(10)` sem comprovar capacidade da memória.

Caminhos relativos à fixture local do domínio; snapshots e hashes em `verificacao.json` da iteração. As aplicações não foram executadas.
