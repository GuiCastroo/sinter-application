---
id: cmp-nucleo-get-iot-endpoint
kind: component
subject: component:nucleo-serverlesspresso:get-iot-endpoint
camada: 5
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "00-baseCore/GetIoTEndpoint.js; 00-baseCore/template.yaml#L89-L114"
    version: 9d494a2
    extraction: extracted
---
# get-iot-endpoint
Custom Resource que descobre o endpoint de dados do AWS IoT Core da conta, para o `publisher-service` publicar mensagens MQTT.

| Campo | Valor |
|---|---|
| Tipo | job (Lambda-backed CloudFormation Custom Resource) |
| Gatilho | `Custom::IotEndpoint` no ciclo de vida do CloudFormation |
| Entrada | Nenhuma (chama `iot:DescribeEndpoint`) |
| Saída | `IotEndpointAddress`, exportado como output da pilha e como parâmetro SSM |
| Timeout / memória / concorrência | 3 s / 128 MB |

## Dependências
- AWS IoT (`iot:DescribeEndpoint`)

## Erros e retentativas
Não há tratamento de erro visível no arquivo lido (arquivo fora do escopo detalhado desta extração); assume-se o comportamento padrão de Custom Resource (falha reportada ao CloudFormation).
