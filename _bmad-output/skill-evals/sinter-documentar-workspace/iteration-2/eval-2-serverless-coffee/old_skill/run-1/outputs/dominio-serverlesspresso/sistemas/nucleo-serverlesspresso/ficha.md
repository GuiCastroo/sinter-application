---
id: sys-nucleo-serverlesspresso
kind: system
subject: system:nucleo-serverlesspresso
camada: 4
status: proposed
realiza: [sub-nucleo-e-identidade]
realizado-por: [cmp-nucleo-get-iot-endpoint, cmp-nucleo-pre-sign-up, cmp-nucleo-define-auth-challenge, cmp-nucleo-create-auth-challenge, cmp-nucleo-verify-auth-challenge, res-event-bus-serverlesspresso, res-user-pool-cognito, res-identity-pool-cognito, res-iot-core-realtime]
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/template.yaml"
    version: 9d494a2
    extraction: extracted
---
# nucleo-serverlesspresso
Pilha fundacional (`00-baseCore`): cria o barramento de eventos, o fluxo de autenticação sem senha do Cognito (login por SMS com código de 6 dígitos) e descobre o endpoint do AWS IoT Core usado pelo `publisher-service`.

| Campo | Valor |
|---|---|
| Subdomínio | Núcleo e identidade |
| Dono | Não identificado |
| Stack | AWS SAM (CloudFormation), Node.js 14.x para as lambdas |
| Repositório | `00-baseCore/` |
| Criticidade | Máxima — todos os outros sistemas dependem do bus e/ou do User Pool desta pilha (via SSM Parameter Store) |

## Contêineres
```mermaid
flowchart LR
  subgraph nucleo-serverlesspresso
    BUS[[EventBridge Serverlesspresso]]
    UP[Cognito User Pool]
    IP[Cognito Identity Pool]
    IOT[(IoT Core endpoint)]
    L1[pre-sign-up]
    L2[define-auth-challenge]
    L3[create-auth-challenge]
    L4[verify-auth-challenge-response]
    L5[get-iot-endpoint]
  end
  UP --> L1
  UP --> L2
  UP --> L3
  UP --> L4
  L5 --> IOT
  UP --> IP
```

## Expõe
- `ServerlesspressoEventBus` (EventBridge) — usado por todos os sistemas do domínio para publicar/consumir eventos
- User Pool / Identity Pool (Cognito) — autenticação usada por todas as APIs do domínio
- Endpoint do IoT Core — usado pelo `publisher-service`

## Consome
Nenhuma dependência de outro sistema do domínio.

## Dados
Nenhum banco de dados próprio (apenas um `LogGroupForEvents` para depurar eventos do bus).

## Estados
N/A.

## Qualidade
- Autenticação: MFA desligada, política de senha mínima (o "segredo" real é o código de 6 dígitos enviado por SMS via SNS)
- `GetIoTEndpointFunction` é um Custom Resource do CloudFormation — roda uma vez por deploy, não a cada requisição
- Outputs desta pilha (User Pool ID, ARN do bus, endpoint IoT) são publicados em **AWS Systems Manager Parameter Store**, e é assim que `01-appCore` e os módulos standalone (`8-order-journey`, `9-validator`, `7-metrics-service`) os descobrem — ver `infraestrutura/ambientes/`
