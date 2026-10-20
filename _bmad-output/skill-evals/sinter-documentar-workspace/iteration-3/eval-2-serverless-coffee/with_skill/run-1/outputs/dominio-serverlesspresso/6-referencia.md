# Referência: Serverlesspresso

> **Em resumo:** glossário, regras, decisões reconstruídas, padrões de código e um guia rápido para
> rodar o projeto localmente. A seção mais importante para quem for mexer aqui é "Dúvidas e
> perguntas": lista o código órfão encontrado e os conflitos entre a config e o código.

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
| `eventId` | Identificador de um evento pop-up (ex.: `ABC`); particiona config, tokens e pedidos |
| Token / QR code | Código de curta duração que libera um pedido; renovado a cada janela de 5 min |
| `TaskToken` | Ficha emitida pelo Step Functions ao pausar (`waitForTaskToken`); guardada no DynamoDB e usada por outro processo para chamar `SendTaskSuccess` |
| `orderId` | Identificador único do pedido, gerado (`nanoid`) no momento da validação do QR code |
| `orderNumber` | Número sequencial exibido ao cliente, gerado só depois que ele envia a bebida |
| `ORDERSTATE` | Estado do pedido, sempre `{eventId}-{ESTADO}` (`CREATED`, `COMPLETED`, `CANCELLED`) |
| `drinkOrder` | JSON da bebida escolhida + modificadores, validado contra o cardápio |
| `baristaUserId` | Identificador do barista que assumiu o pedido (`action=make`) |
| `robot` | Marca um pedido como gerado por simulação (`OrderRobotExtension`), não por cliente real |
| Bus `Serverlesspresso` | Event bus custom do EventBridge; todo evento de negócio passa por ele |
| Barista | Quem prepara e conclui (ou cancela) o pedido |
| Recibo (Journey) | Página HTML final com a trilha de eventos de um pedido |

## Regras de negócio
| ID | Regra | Valor atual | Onde está implementada |
|---|---|---|---|
| R01 | Pedidos simultâneos | máx. 20 | `backends/4-order-processing/statemachine/op.asl.json` (`Is capacity available?`) |
| R02 | Tokens (QR) por janela | 10 a cada 5 min, por evento | `01-appCore/initDB/initMenuState.JSON` (`drinksPerBarcode`), `backends/9-validator/code/getCode.js` |
| R03 | Tempo para o cliente enviar a bebida | 5 min | `op.asl.json` (`HeartbeatSeconds: 300`) |
| R04 | Tempo para o barista concluir | 15 min | `op.asl.json` (`HeartbeatSeconds: 900`) |
| R05 | Pedidos por cliente | 1 (`maxOrdersPerUser`) | `01-appCore/initDB/initMenuState.JSON` — *(a confirmar: não achamos onde é checado em runtime)* |

## Decisões
Nenhum ADR foi encontrado no repositório (`docs/` só tem um template de Pull Request). As três
decisões abaixo foram **reconstruídas a partir do código**, não de um documento de decisão real:

| # | Contexto | Escolha | Consequência |
|---|---|---|---|
| 1 | Um pedido precisa esperar minutos por ações humanas (cliente escolher bebida, barista concluir) sem manter função alguma "viva" | Duas máquinas de Step Functions: uma pausa com `waitForTaskToken`, a outra recebe a ação via API e resume a primeira com `SendTaskSuccess`, usando o DynamoDB como elo | Acoplamento indireto entre as duas máquinas via a linha do pedido; se o token for perdido ou sobrescrito, o pedido só termina no timeout |
| 2 | Três frontends (cliente, barista, admin) precisam de atualização em tempo real sem polling | AWS IoT Core (MQTT), alimentado por lambdas "publisher" que escutam o bus por prefixo de `detail-type` | Acoplamento por convenção de nome: um evento novo só chega ao frontend se algum publisher já escutar aquele prefixo |
| 3 | Cada evento pop-up precisa de config própria (cardápio, limites, aberto/fechado) | Uma única tabela indexada por `config-{eventId}`, alterada via API e propagada por DynamoDB Streams | Todo serviço que precisa do cardápio lê a mesma tabela direto, em vez de manter cópia local por evento |

## Padrões
- **IaC:** AWS SAM (`template.yaml`) em quase todos os serviços; um deles (`extensions/WaitTimes`)
  usa AWS CDK em TypeScript — única exceção no repositório.
- **Runtime:** Node.js 14.x em praticamente todos os lambdas (handlers `exports.handler`, SDK v2
  `aws-sdk`).
- **Orquestração:** Amazon States Language (`*.asl.json`) versionado separado do `template.yaml`,
  injetado via `DefinitionSubstitutions`.
- **Testes:** cada serviço tem um `localTest.js`/`testharness.js` ad-hoc para rodar o handler local
  com um evento de exemplo; os READMEs mencionam Mocha em `functions/*/tests`, mas poucos arquivos
  de teste formais foram encontrados *(a confirmar)* — não há pipeline de CI configurado (`.github`
  só tem templates de Issue/PR).
- **Nomeação de eventos:** `{Serviço}.{Acontecimento}` (ex.: `Validator.NewOrder`,
  `OrderProcessor.WorkflowStarted`); o order-manager foge um pouco do padrão e embute o `eventId`
  no meio (`OrderManager.Order{eventId}-COMPLETED`).

## Como começar
1. **Deploy:** `00-baseCore` primeiro (`sam build && sam deploy --guided`, stack
   `serverlesspresso-core`, região `us-east-1`), depois `01-appCore` (stack `serverlesspresso`).
   `7-metrics-service` e cada pasta em `extensions/` são opcionais e implantados à parte.
2. **Testar localmente:** entrar na pasta do lambda e rodar `node localTest.js` (ou
   `testharness.js`), ou `npm test` onde houver `package.json` com Mocha.
3. **Onde fica cada coisa:** `backends/<n>-<nome>/` por serviço; `functions/`/`code/` = lambdas,
   `statemachine/` = ASL, `RestAPIs/api.yaml` ou `api.yaml` = contrato REST.
4. **As 3 mudanças mais comuns:**
   - Mudar o cardápio ou limites de um evento → editar a linha `config-{eventId}` na `ConfigTable`
     (não há endpoint de escrita para o cardápio, só para `storeOpen`).
   - Mudar o limite de pedidos simultâneos → editar o número `20` fixo em
     `backends/4-order-processing/statemachine/op.asl.json` (não é parâmetro).
   - Adicionar um novo consumidor de eventos → seguir o modelo em `extensions/_extension-model/`
     (regra de EventBridge nova, sem tocar no core).
5. **Publicar:** `sam deploy` (guiado ou com `samconfig.toml` salvo); limpeza via
   `aws cloudformation delete-stack --stack-name <nome>`.

## Dúvidas e perguntas

**Conflitos entre fontes:**
- 🟥 `maxOrdersInQueue: 10` (na config do evento) vs. limite real de `20` pedidos simultâneos, fixo
  no ASL do order-processor — os dois existem, nenhum lê o outro.

**Segredos:** nenhuma chave, token ou senha em texto claro foi encontrada nos arquivos lidos
(buscado por padrões comuns de chave AWS, senha e chave privada). Nada a reportar aqui.

**Código encontrado mas aparentemente não implantado** *(ver também [5-infraestrutura.md](./5-infraestrutura.md#código-encontrado-mas-não-implantado-a-confirmar)):*
- `backends/1-counting-service/` (`getOrderId.js`, `resetOrderId.js`) — sem `template.yaml`, sem
  referência cruzada; duplica o que o order-processor já faz inline.
- `backends/4-order-processing/functions/capacity/isCapacityAvailable.js` e `functions/resumeWF/app.js`
  — não aparecem em nenhum template implantado.
- `backends/4-order-processing/api.yaml` (`POST /order` → EventBridge) — não é incluído por
  nenhuma stack encontrada; não identificamos quem o chamaria.

As questões por papel estão reunidas em [Perguntas para decisão](#perguntas-para-decisão).

**Fontes:** leitura direta de todo o código citado nas seções anteriores; ausência de
`CODEOWNERS`, `docs/adr`, ou pipeline de CI verificada por busca no repositório.

## Dúvidas de contexto

O cancelamento manual não registra motivo estruturado; o timeout possui causa. Confirmar se a operação precisa distinguir desistência, erro e falta de insumo. Fonte: eventos em `backends/5-order-manager/`.

A API altera `storeOpen`; não foi encontrada rota para editar `menu`. Confirmar o procedimento operacional de edição direta na `ConfigTable`. Fontes: `backends/2-config-service/`, `01-appCore/initDB/initMenuState.JSON`. Conflito de capacidade, cobrança e código inativo estão registrados acima e em Q01/Q05/Q06/Q07.

## Perguntas para decisão

| ID | Papel | Pergunta |
|---|---|---|
| Q01 | PM | Existe plano de cobrança/pagamento? Hoje não há nenhum passo de pagamento no domínio. |
| Q02 | PM | Quais são os indicadores de sucesso de um evento (KPIs)? Não encontramos nada documentado além do que a extensão `WaitTimes` calcula. |
| Q03 | PM | `maxOrdersPerUser = 1` é uma regra real hoje ou só um valor de config sem efeito? |
| Q04 | Arquiteto | Por que duas máquinas de Step Functions em vez de uma? O acoplamento via `TaskToken` no DynamoDB foi uma escolha deliberada ou uma consequência de como o workshop foi montado em módulos? |
| Q05 | Arquiteto | Vale a pena mover o limite de capacidade (hoje fixo em `20` no ASL) para a tabela de config, já que ela já tem um campo parecido (`maxOrdersInQueue`) sem uso? |
| Q06 | Tech lead | `1-counting-service` e os dois lambdas órfãos de `4-order-processing/functions` podem ser removidos, ou há algum plano de reativá-los? |
| Q07 | Tech lead | O endpoint `POST /order` em `backends/4-order-processing/api.yaml` é usado por algum dos 3 frontends externos (não incluídos neste repositório)? |
| Q08 | Tech lead | Existe algum alarme/DLQ para quando `publisher-service` falha ao publicar no IoT (hoje só loga e segue)? |

## Evidências da revisão v3

`01-appCore/template.yaml:143,197,317,497,648` declara cinco tabelas; `:67,759,791` declara três máquinas (duas do pedido e uma do recibo). `backends/9-validator/code/getCode.js:11–28` restringe GET /qr-code ao grupo admin.

Caminhos relativos à fixture local do domínio; snapshots e hashes em `verificacao.json` da iteração. As aplicações não foram executadas.
