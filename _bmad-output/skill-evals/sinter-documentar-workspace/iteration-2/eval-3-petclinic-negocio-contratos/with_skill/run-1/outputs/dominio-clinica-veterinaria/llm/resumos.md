# Clínica Veterinária: resumos

Degrau 1. Cada página e cada seção de serviço e de jornada em poucas linhas. Para o detalhe, abra a seção indicada.

## Negócio (1-negocio.md)
cadastro de uma clínica veterinária — donos, pets, veterinários e o histórico de visitas de cada pet — com um assistente de IA que responde perguntas e cadastra dono/pet por conversa. Não há agendamento com confirmação, cobrança nem prontuário clínico.

Parede do domínio:
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Recepção/dono | Cadastra o dono | Dono cadastrado | Nome, endereço, cidade e telefone obrigatórios; telefone só números, até 12 dígitos |
| 2 | Recepção/dono | Cadastra um pet para o dono | Pet cadastrado | Precisa de um dono já existente; nome do pet obrigatório |
| 3 | Clínica/veterinário | Registra a visita de um pet | Visita registrada | Descrição livre até 8192 caracteres; sem checagem de que o pet existe |
| 4 | Dono/recepção | Abre a ficha do dono | Ficha exibida (dono + pets + visitas) | Se o histórico de visitas não responder a tempo, mostra os pets sem histórico em vez de falhar |
| 5 | Dono/recepção | Consulta a lista de veterinários | Lista exibida (pode vir de cache) | — |
| 6 | Usuário | Pergunta ou pede uma ação ao assistente de IA | Resposta gerada, e opcionalmente dono/pet criado | O assistente só executa as 4 ações que tem disponíveis; se não souber responder, deve dizer isso e perguntar de volta |

## Arquitetura (2-arquitetura.md)
microsserviços Spring Cloud — um serviço por subdomínio (donos/pets, visitas, veterinários, IA), um gateway de borda que agrega e roteia, três serviços de plataforma (config, descoberta, admin). Tudo síncrono via REST; sem fila, evento ou orquestrador.

## Serviços (3-servicos.md)
8 serviços Spring Boot. Quatro carregam o negócio (donos/pets, visitas, veterinários, chatbot de IA), um é a borda (api-gateway), três são plataforma (config, descoberta, admin). Comunicação só síncrona via REST/HTTP — sem fila nem eventos.

- **customers-service** (3-servicos.md#customers-service): dono do sistema de registro de donos (`Owner`) e pets (`Pet`); é a fonte de verdade que os outros serviços (gateway e IA) consultam para saber quem é o dono e quais pets ele tem.
- **visits-service** (3-servicos.md#visits-service): registra o histórico de visitas de um pet (data + descrição). Não sabe quem é o dono nem o tipo do pet — só guarda o `petId`.
- **vets-service** (3-servicos.md#vets-service): cadastro de veterinários e suas especialidades; lista é cacheada em memória (`@Cacheable("vets")`) porque muda pouco e é lida com frequência.
- **genai-service** (3-servicos.md#genai-service): expõe um chatbot (Spring AI) que responde perguntas sobre donos, pets e veterinários e pode criar donos/pets por conta própria, chamando `customers-service` diretamente e usando uma base vetorial pré-carregada dos veterinários para busca semântica.
- **api-gateway** (3-servicos.md#api-gateway): porta de entrada única: serve o front-end AngularJS estático, roteia `/api/**` para os serviços de negócio e é o único ponto que agrega dados de dois serviços (dono + visitas) numa mesma resposta.
- **config-server** (3-servicos.md#config-server): entrega configuração centralizada a todos os outros serviços na subida, lendo de um repositório Git externo (ou de um diretório local no perfil `native`).
- **discovery-server** (3-servicos.md#discovery-server): registro de serviços via Eureka; todo serviço de aplicação se registra aqui e descobre os outros pelo nome lógico (`lb://customers-service`, etc.).
- **admin-server** (3-servicos.md#admin-server): painel de operação (Spring Boot Admin) para visualizar saúde e métricas dos outros serviços registrados no Eureka.

## Jornadas (4-jornadas.md)
5 jornadas, todas síncronas via REST. Sem orquestrador único: cada jornada é uma chamada direta a um serviço, ou uma agregação pontual do `api-gateway` (junta dois serviços, com circuit breaker).

- **Cadastrar dono e pet** (4-jornadas.md#cadastrar-dono-e-pet): a recepção (ou o próprio front-end) cria o dono e, na sequência, adiciona um ou mais pets a ele. Cada pet pertence a exatamente um dono.
- **Registrar uma visita** (4-jornadas.md#registrar-uma-visita): a clínica registra que um pet foi atendido, com data e descrição livre; não há conceito de agendamento prévio com confirmação — é um registro histórico do atendimento.
- **Consultar a ficha do dono** (4-jornadas.md#consultar-a-ficha-do-dono): a jornada mais "orquestrada" do domínio — o `api-gateway` busca o dono e, em paralelo, as visitas de todos os pets dele, juntando tudo numa única resposta para o front-end. Se as visitas falharem, a ficha aparece mesmo assim, só que sem histórico.
- **Consultar veterinários** (4-jornadas.md#consultar-veterinários): lista simples da equipe clínica e suas especialidades; a resposta é cacheada em memória no `vets-service`, então uma mudança recente pode não aparecer de imediato.
- **Conversar com o assistente de IA** (4-jornadas.md#conversar-com-o-assistente-de-ia): o usuário manda uma mensagem em linguagem natural; o `genai-service` decide, via tool calling do LLM, se precisa listar donos, listar veterinários (busca semântica), ou criar dono/pet — chamando `customers-service` diretamente, sem passar pelo `api-gateway`.

## Infraestrutura (5-infraestrutura.md)
aplicações Spring Boot independentes, registradas num Eureka (`discovery-server`) e configuradas por um Config Server que busca valores num repositório Git externo. Sobe local via `docker-compose.yml` ou `mvnw`/`run_all.sh`; sem Terraform, Kubernetes ou CloudFormation.

## Referência (6-referencia.md)
glossário, regras, decisões reconstruídas, padrões de código, como rodar localmente e as dúvidas em aberto por papel — para quem vai mexer no código ou decidir sobre ele sem reler tudo.

