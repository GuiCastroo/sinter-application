---
id: env-core-00-basecore
kind: environment
subject: environment:core-00-basecore
camada: 6
status: proposed
realiza: [sys-nucleo-serverlesspresso]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "README.md; 00-baseCore/template.yaml"
    version: 9d494a2
    extraction: extracted
---
# Ambiente "core" (pilha 00-baseCore)
Primeira pilha a ser implantada (README raiz, seção "Installing the backend"), sempre na região `us-east-1` por instrução do README. Cria o bus de eventos, o Cognito e o endpoint IoT, e publica os identificadores desses recursos em **AWS Systems Manager Parameter Store** (`/Serverlesspresso/core/*`) para as pilhas seguintes consumirem via `AWS::SSM::Parameter::Value<String>`.

## Implantação
```mermaid
flowchart TB
  subgraph core["Pilha serverlesspresso-core (00-baseCore)"]
    BUS[[EventBridge Serverlesspresso]]
    UP[Cognito User Pool]
    IOT[(IoT Core endpoint)]
  end
  core -->|outputs| SSM[(SSM Parameter Store<br/>/Serverlesspresso/core/*)]
  SSM --> APPCORE[01-appCore]
  SSM --> STANDALONE["Módulos standalone<br/>(7-metrics, 8-order-journey, 9-validator)"]
```
