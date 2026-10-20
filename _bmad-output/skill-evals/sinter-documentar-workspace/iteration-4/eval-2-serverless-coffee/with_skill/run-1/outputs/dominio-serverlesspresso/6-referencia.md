# Referência: Serverlesspresso

> **Em resumo:** definições únicas do domínio — glossário, regras com ID, padrões, como rodar e
> testar uma mudança, e um só registro de pendências. Decisões de arquitetura ficam em
> [Arquitetura](2-arquitetura.md#decisões-que-moldam); código inativo, em
> [Infraestrutura](5-infraestrutura.md#código-encontrado-mas-não-implantado-a-confirmar).

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
| R05 | Pedidos por cliente | 1 (`maxOrdersPerUser`) | `01-appCore/initDB/initMenuState.JSON` — valor de config; verificação em runtime não encontrada ([Q03](#pendências)) |
| R06 | Leitura do QR code | `GET /qr-code` só para o grupo admin | `backends/9-validator/code/getCode.js` |

## Padrões
- **IaC:** AWS SAM (`template.yaml`) em quase todos os serviços; um deles (`extensions/WaitTimes`)
  usa AWS CDK em TypeScript — única exceção no repositório.
- **Runtime:** Node.js 14.x em praticamente todos os lambdas (handlers `exports.handler`, SDK v2
  `aws-sdk`).
- **Orquestração:** Amazon States Language (`*.asl.json`) versionado separado do `template.yaml`,
  injetado via `DefinitionSubstitutions`.
- **Testes:** não há suíte automatizada efetiva nem CI (ver [Como começar](#como-começar)).
- **Nomeação de eventos:** `{Serviço}.{Acontecimento}` (ex.: `Validator.NewOrder`,
  `OrderProcessor.WorkflowStarted`); o order-manager foge um pouco do padrão e embute o `eventId`
  no meio (`OrderManager.Order{eventId}-COMPLETED`).

## Como começar
1. **Deploy:** `00-baseCore` primeiro (`sam build && sam deploy --guided`, stack
   `serverlesspresso-core`, região `us-east-1`), depois `01-appCore` (stack `serverlesspresso`).
   `7-metrics-service` e cada pasta em `extensions/` são opcionais e implantadas à parte.
2. **Testar uma mudança:** não há teste automatizado que rode offline. O único `npm test` com
   arquivo (`extensions/WaitTimes`, Jest) é um exemplo vazio comentado, e o `mocha tests/unit/` de
   `GenerateHtml` aponta para uma pasta inexistente. O caminho real é o *harness* local, que chama o
   handler com um evento de exemplo **contra recursos AWS já implantados** (precisa de credenciais):
   - Validar QR: `node localTest.js` em `backends/9-validator/code` (evento em `test/testEvent.json`).
   - Publicar no IoT: `node localTest.js` em `backends/6-publisher-service/code`; o evento
     `test/testEvent.json` é um bom **exemplo de envelope** (`detail-type`
     `OrderManager.WaitingCompletion`, `detail` com `orderId`, `orderNumber`, `state`, `drinkOrder`,
     `userId`, `robot`, `TS`).
   - Recibo: `node testharness.js` em `backends/8-order-journey/functions/GenerateHtml`.
   Para o fluxo inteiro, faça um pedido e acompanhe a execução das duas máquinas no console do
   Step Functions pelo `orderId`. *Comandos não executados nesta revisão.*
3. **Onde fica cada coisa:** `backends/<n>-<nome>/` por serviço; `functions/`/`code/` = lambdas,
   `statemachine/` = ASL, `RestAPIs/api.yaml` ou `api.yaml` = contrato REST.
4. **Mudanças mais comuns:**
   - **Cardápio ou limites de um evento:** editar a linha `config-{eventId}` na `ConfigTable` (não
     há endpoint de escrita para o cardápio, só para `storeOpen`).
   - **Capacidade simultânea:** editar o `20` em
     `backends/4-order-processing/statemachine/op.asl.json` e reimplantar `01-appCore`
     (`maxOrdersInQueue` não tem efeito).
   - **Novo consumidor de eventos:** seguir `extensions/_extension-model/` (regra nova no
     EventBridge, sem tocar no core); usar o envelope acima como exemplo de entrada.
5. **Publicar:** `sam deploy`; limpeza via `aws cloudformation delete-stack --stack-name <nome>`.

## Pendências
Registro único de perguntas em aberto e conflitos entre fontes. Fatos confirmados não entram aqui.

| ID | Tipo | Assunto | Pergunta ou conflito | Impacto | Evidência | Quem responde |
|---|---|---|---|---|---|---|
| Q01 | Produto | Cobrança | Existe plano de cobrança? Hoje não há passo de pagamento | Mudaria o fluxo do pedido inteiro | Ausência de código de pagamento | Mantenedores |
| Q02 | Produto | Indicadores | Quais indicadores medem o sucesso de um evento? | Só existem `WaitTimes` e métricas operacionais | `extensions/WaitTimes/README.md` | Mantenedores |
| Q03 | Produto | Um pedido por cliente | `maxOrdersPerUser = 1` é regra real ou só config? | Não se pode prometer "um café por pessoa" | `initMenuState.JSON`; nenhuma checagem encontrada | Dev |
| Q04 | Arquitetura | Dois workflows | As duas máquinas via `TaskToken` foram escolha deliberada ou efeito da divisão em módulos do workshop? | Define se vale unificar | `op.asl.json`, `om.asl.json` | Arquitetura |
| Q05 | Conflito | Capacidade | Config diz `maxOrdersInQueue: 10`; o ASL fixa `20` e não lê a config | Mudar a config não muda a capacidade | `op.asl.json` (`Is capacity available?`) | Arquitetura |
| Q06 | Técnica | Código inativo | `1-counting-service` e os lambdas órfãos de `4-order-processing/functions` podem ser removidos? | Risco de editar o caminho errado | [Infraestrutura](5-infraestrutura.md#código-encontrado-mas-não-implantado-a-confirmar) | Tech lead |
| Q07 | Técnica | `POST /order` | O endpoint de `backends/4-order-processing/api.yaml` é usado por algum frontend externo? | Nenhuma stack o implanta | `api.yaml` | Tech lead |
| Q08 | Técnica | Falha no IoT | Há alarme ou DLQ quando `publisher-service` falha ao publicar? | App pode parar de atualizar sem alerta | `publishToIOT.js` só loga | Tech lead |
| Q09 | Produto | Motivo do cancelamento | A operação precisa distinguir desistência, erro e falta de insumo? | Cancelamento manual não registra motivo | eventos em `backends/5-order-manager/` | Produto |
| Q10 | Produto | Edição do cardápio | Qual o procedimento para editar o cardápio durante o evento? | Só há edição direta na `ConfigTable` | `backends/2-config-service/`, `initMenuState.JSON` | Operação |

**Segredos:** nenhuma chave, token ou senha em texto claro nos arquivos lidos.

**Fontes:** código citado nas páginas anteriores; ausência de `CODEOWNERS`, `docs/adr` e pipeline
de CI verificada por busca; harnesses e eventos de teste citados em "Como começar".
