# Negócio: Clínica Veterinária

> **Em resumo:** cadastro de uma clínica veterinária — donos, pets, veterinários e o histórico de
> visitas de cada pet — com um assistente de IA que responde perguntas e cadastra dono/pet por
> conversa. Não há agendamento com confirmação, cobrança nem prontuário clínico.

## Nesta página

| Seção |
|---|
| [Em uma frase](#em-uma-frase) |
| [Por que existe](#por-que-existe) |
| [Faz / Não faz / Não sabemos](#faz--não-faz--não-sabemos) |
| [A parede do domínio](#a-parede-do-domínio) |
| [Jornadas principais](#jornadas-principais) |
| [Quem orquestra](#quem-orquestra) |
| [Regras que mandam](#regras-que-mandam) |
| [Entra e sai](#entra-e-sai) |
| [Linguagem](#linguagem) |
| [Indicadores](#indicadores) |

## Em uma frase
Manter o cadastro de donos, pets e veterinários de uma clínica veterinária, registrar o
histórico de visitas de cada pet, e oferecer um assistente de IA que consulta e atualiza esses
dados por meio de conversa em linguagem natural.

## Por que existe
Classificação: **core** *(a confirmar — o repositório é publicamente descrito como aplicação de
exemplo/demonstração da Spring, não uma clínica real; tratamos aqui como se fosse o domínio de
negócio real, como pedido)*. O valor é dar a uma clínica uma visão única de "quem é esse dono",
"quais pets ele tem" e "o que já aconteceu com cada pet", reduzindo a necessidade de planilhas ou
papel — e permitir que essa consulta seja feita por conversa (assistente de IA) além de telas.

## Faz / Não faz / Não sabemos
| Faz | Não faz | Não sabemos |
|---|---|---|
| Cadastra donos e seus pets | Agendamento com confirmação/conflito de horário | Se há front-end de agendamento em outro repositório |
| Registra histórico de visitas (data + descrição) | Cobrança, pagamento, convênio pet | Se há autenticação/login de usuário |
| Mantém cadastro de veterinários e especialidades | Prontuário clínico (diagnóstico, receita, exames) | Se há papel de "recepção" distinto de "veterinário" |
| Responde perguntas e age via chatbot de IA | Notificação ao dono (e-mail/SMS) | Regra real por trás dos tipos de pet aceitos pela IA |
| Agrega a "ficha" do dono com pets e visitas | Estoque de insumos/medicamentos | Dono/responsável de cada serviço (sem `CODEOWNERS`) |

## A parede do domínio
| # | 🟨 Quem | 🟦 Faz | 🟧 Acontece | 🟪 Regra ou reação |
|---|---|---|---|---|
| 1 | Recepção/dono | Cadastra o dono | Dono cadastrado | Nome, endereço, cidade e telefone obrigatórios; telefone só números, até 12 dígitos |
| 2 | Recepção/dono | Cadastra um pet para o dono | Pet cadastrado | Precisa de um dono já existente; nome do pet obrigatório |
| 3 | Clínica/veterinário | Registra a visita de um pet | Visita registrada | Descrição livre até 8192 caracteres; sem checagem de que o pet existe |
| 4 | Dono/recepção | Abre a ficha do dono | Ficha exibida (dono + pets + visitas) | Se o histórico de visitas não responder a tempo, mostra os pets sem histórico em vez de falhar |
| 5 | Dono/recepção | Consulta a lista de veterinários | Lista exibida (pode vir de cache) | — |
| 6 | Usuário | Pergunta ou pede uma ação ao assistente de IA | Resposta gerada, e opcionalmente dono/pet criado | O assistente só executa as 4 ações que tem disponíveis; se não souber responder, deve dizer isso e perguntar de volta |

🟥 Consulte as [dúvidas de contexto na Referência](6-referencia.md#dúvidas-de-contexto).

## Jornadas principais
| Jornada | Em uma linha | Link |
|---|---|---|
| Cadastrar dono e pet | Recepção registra um novo dono e seus pets | [4-jornadas.md](4-jornadas.md#cadastrar-dono-e-pet) |
| Registrar uma visita | Clínica registra o atendimento de um pet | [4-jornadas.md](4-jornadas.md#registrar-uma-visita) |
| Consultar a ficha do dono | Ver o dono com pets e histórico de visitas | [4-jornadas.md](4-jornadas.md#consultar-a-ficha-do-dono) |
| Consultar veterinários | Ver a equipe clínica e especialidades | [4-jornadas.md](4-jornadas.md#consultar-veterinários) |
| Conversar com o assistente de IA | Perguntar ou pedir ações em linguagem natural | [4-jornadas.md](4-jornadas.md#conversar-com-o-assistente-de-ia) |

## Quem orquestra
| Jornada | Quem manda | Como |
|---|---|---|
| Cadastrar dono e pet | Ninguém — chamadas diretas e sequenciais | Cliente (front-end ou IA) decide a ordem |
| Registrar uma visita | Ninguém — chamada direta | — |
| Consultar a ficha do dono | `api-gateway` | Agregação pontual (fan-out): busca dono, depois visitas, com circuit breaker |
| Consultar veterinários | Ninguém — chamada direta (proxy) | — |
| Conversar com o assistente de IA | O próprio modelo de IA (tool calling) | O LLM decide, a cada mensagem, qual das 4 ações chamar |

Não existe um motor de processo (BPM/Step Functions/Temporal) nem coreografia por eventos neste domínio — ver [2-arquitetura.md](2-arquitetura.md#estilo-de-integração).

## Regras que mandam
Os limites e exceções desta perspectiva estão consolidados na [Referência](6-referencia.md#regras-de-negócio); consulte também as [dúvidas](6-referencia.md#dúvidas-e-perguntas).

## Entra e sai
| Direção | O quê | Com quem |
|---|---|---|
| Entra | Cadastro de dono/pet, registro de visita, perguntas em linguagem natural | Front-end (AngularJS no api-gateway), usuário do chat |
| Sai | Ficha do dono, lista de veterinários, respostas do assistente | Front-end, usuário do chat |
| Sai | Perguntas/comandos em linguagem natural | 🩷 OpenAI ou Azure OpenAI (provedor de LLM externo) |
| Entra | Configuração de todos os serviços | 🩷 Repositório Git externo `spring-petclinic-microservices-config` |
| Sai | Traces e métricas técnicas | 🩷 Zipkin, Prometheus, Grafana |

Não há troca com outros domínios de negócio (faturamento, estoque, laboratório) neste repositório.

## Linguagem
Os termos têm uma definição única na [Referência](6-referencia.md#glossário); consulte também as [dúvidas](6-referencia.md#dúvidas-e-perguntas).

## Indicadores
*(a confirmar — não há indicadores de negócio explícitos no código)*. O que existe são métricas
técnicas de volume/latência de chamadas (`@Timed petclinic.owner`, `petclinic.pet`,
`petclinic.visit`, expostas via Micrometer/Prometheus/Grafana) — não indicadores de negócio como
"taxa de retorno de donos" ou "tempo médio até a primeira visita". Proposta de indicadores a
validar com o negócio: número de donos/pets cadastrados por período, número de visitas
registradas por período, uso do assistente de IA (mensagens/ações por período).

**Fontes:** entidades e controllers de `customers-service`, `visits-service`, `vets-service` (regras de validação, campos obrigatórios); `PetclinicChatClient.java` e `PetclinicTools.java` (comportamento e limites do assistente de IA); `ApiGatewayController.java` (agregação da ficha do dono); `README.md` (descrição geral do projeto como demonstração Spring). Classificação do domínio (core/suporte/genérico), donos por papel e indicadores de negócio são deduções ou perguntas, marcadas *(a confirmar)* — não estão escritos em nenhum documento de negócio no repositório.
