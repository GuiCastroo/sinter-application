# Negócio: Clínica Veterinária

> **Em resumo:** cadastro de uma clínica veterinária — donos, pets, veterinários e o histórico de
> visitas de cada pet — com um assistente de IA que responde perguntas e cadastra dono/pet por
> conversa. "Visita" é registro histórico, não agendamento; não há cobrança nem prontuário clínico.
> O repositório é uma aplicação de exemplo da Spring; aqui é tratado como domínio real, como pedido.

## Nesta página

| Seção |
|---|
| [Faz / Não faz / Não sabemos](#faz--não-faz--não-sabemos) |
| [A parede do domínio](#a-parede-do-domínio) |
| [Jornadas principais](#jornadas-principais) |
| [Regras que mandam](#regras-que-mandam) |
| [Entra e sai](#entra-e-sai) |
| [Indicadores](#indicadores) |

## Faz / Não faz / Não sabemos
| Faz | Não faz | Não sabemos |
|---|---|---|
| Cadastra donos e seus pets | Agendamento com confirmação/conflito de horário | Se há front-end de agendamento em outro repositório |
| Registra histórico de visitas (data + descrição) | Cobrança, pagamento, convênio pet | Se haverá login e papéis ([Q01](6-referencia.md#pendências)); hoje não há segurança no código |
| Mantém cadastro de veterinários e especialidades | Prontuário clínico (diagnóstico, receita, exames) | Se agendamento e cobrança entram no escopo ([Q01](6-referencia.md#pendências)) |
| Responde perguntas e age via chatbot de IA | Notificação ao dono (e-mail/SMS) | Regra real por trás dos tipos de pet aceitos pela IA ([Q05](6-referencia.md#pendências)) |
| Agrega a "ficha" do dono com pets e visitas | Estoque de insumos/medicamentos | Dono/responsável de cada serviço (sem `CODEOWNERS`) |

## A parede do domínio
Os atores são **ilustrativos**: o repositório não tem login nem papéis, então qualquer usuário faz
qualquer ação ([Q01](6-referencia.md#pendências)).

| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Recepção/dono | Cadastra o dono | Dono cadastrado | Nome, endereço, cidade e telefone obrigatórios; telefone só números, até 12 dígitos |
| 2 | Recepção/dono | Cadastra um pet para o dono | Pet cadastrado | Precisa de um dono já existente; nome do pet obrigatório |
| 3 | Clínica/veterinário | Registra a visita de um pet | Visita registrada | Descrição livre até 8192 caracteres; sem checagem de que o pet existe |
| 4 | Dono/recepção | Abre a ficha do dono | Ficha exibida (dono + pets + visitas) | Se o histórico de visitas falhar, mostra os pets **sem histórico** — igual a "nunca atendido" |
| 5 | Dono/recepção | Consulta a lista de veterinários | Lista exibida (pode vir de cache) | — |
| 6 | Usuário | Pergunta ou pede uma ação ao assistente de IA | Resposta gerada, e opcionalmente dono/pet criado | O assistente só executa as 4 ações que tem disponíveis; se não souber responder, deve dizer isso e perguntar de volta |

## Jornadas principais
| Jornada | Em uma linha | Quem conduz |
|---|---|---|
| [Cadastrar dono e pet](4-jornadas.md#cadastrar-dono-e-pet) | Registrar um novo dono e seus pets | Quem chama (tela ou IA) decide a ordem |
| [Registrar uma visita](4-jornadas.md#registrar-uma-visita) | Registrar o atendimento de um pet | Chamada direta |
| [Consultar a ficha do dono](4-jornadas.md#consultar-a-ficha-do-dono) | Dono com pets e histórico de visitas | `api-gateway` junta dono e visitas |
| [Consultar veterinários](4-jornadas.md#consultar-veterinários) | Equipe clínica e especialidades | Chamada direta (pode vir de cache) |
| [Conversar com o assistente de IA](4-jornadas.md#conversar-com-o-assistente-de-ia) | Perguntar ou pedir ações em linguagem natural | O modelo escolhe qual das 4 ações chamar |

## Regras que mandam
- **Ficha sem visitas não prova que o pet nunca foi atendido** ([R07](6-referencia.md#regras-de-negócio)):
  se o serviço de visitas falhar ou passar de 10 s, a ficha aparece com histórico vazio, sem aviso.
- **Visita não confere se o pet existe:** o registro guarda só o identificador do pet, sem
  validação cruzada ([R04](6-referencia.md#regras-de-negócio) cobre só o tamanho da descrição).
- **Dono exige nome, endereço, cidade e telefone só com dígitos (até 12)**
  ([R01/R02](6-referencia.md#regras-de-negócio)). O assistente de IA aplica a mesma regra de
  telefone, mas aceita qualquer tipo de pet numérico; a lista de tipos válidos é só instrução ao modelo ([R05](6-referencia.md#regras-de-negócio)).

Glossário e demais regras na [Referência](6-referencia.md#glossário).

## Entra e sai
| Direção | O quê | Com quem |
|---|---|---|
| Entra | Cadastro de dono/pet, registro de visita, perguntas em linguagem natural | Front-end (AngularJS no api-gateway), usuário do chat |
| Sai | Ficha do dono, lista de veterinários, respostas do assistente | Front-end, usuário do chat |
| Sai | Perguntas/comandos em linguagem natural | 🩷 OpenAI ou Azure OpenAI (provedor de LLM externo) |
| Entra | Configuração de todos os serviços | 🩷 Repositório Git externo `spring-petclinic-microservices-config` |
| Sai | Traces e métricas técnicas | 🩷 Zipkin, Prometheus, Grafana |

Não há troca com outros domínios de negócio (faturamento, estoque, laboratório) neste repositório.

## Indicadores
Não há indicadores de negócio no código; existem métricas técnicas de volume e latência
(`@Timed petclinic.owner`, `petclinic.pet`, `petclinic.visit`, via Micrometer/Prometheus/Grafana).
Candidatos a validar com o negócio, não metas: cadastros e visitas por período e uso do assistente.

**Fontes:** entidades e controllers de `customers-service`, `visits-service` e `vets-service`;
`PetclinicChatClient.java` e `PetclinicTools.java`; `ApiGatewayController.java`; `README.md`.
