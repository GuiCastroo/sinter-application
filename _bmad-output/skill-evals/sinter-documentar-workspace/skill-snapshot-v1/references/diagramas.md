# Padrões de diagrama (Mermaid)

Um diagrama por pergunta. Poucos elementos (até ~12), rótulos curtos, nomes iguais aos do código.

## Fluxo macro com raias (camada 1)

Sem nomes de sistemas: só atores e etapas de negócio.

```mermaid
flowchart LR
  subgraph Cliente
    A[Escolhe produtos] --> B[Escolhe parcelas]
  end
  subgraph Loja
    B --> C{Pagamento aprovado?}
    C -- sim --> D[Confirma pedido]
    C -- não --> E[Oferece outro meio]
  end
```

## Mapa de capacidades (camada 1)

```mermaid
flowchart TB
  subgraph Vendas
    V1[Vender à vista]
    V2[Vender parcelado]
  end
  subgraph Financeiro
    F1[Conciliar pagamentos]
    F2[Estornar compra]
  end
```

## Contexto do domínio (camada 2)

```mermaid
flowchart LR
  Cliente((Cliente)) --> PAG[Domínio Pagamentos]
  PAG --> ADQ[Adquirente externo]
  PAG --> CONT[Domínio Contabilidade]
  PED[Domínio Pedidos] --> PAG
```

## Sequência entre sistemas (camada 3)

Mostre respostas, eventos assíncronos (`-)`) e ao menos um caminho de erro relevante (`alt`).

```mermaid
sequenceDiagram
  participant Site
  participant CO as checkout-api
  participant GW as payments-gateway
  Site->>CO: POST /payments
  CO->>GW: POST /authorize
  alt autorizado
    GW-->>CO: 200 autorizado
    GW-)Contabilidade: PaymentAuthorized
  else negado ou timeout 10 s
    GW-->>CO: 402 negado
    CO-->>Site: oferecer outro meio
  end
```

## Contêiner do sistema (camada 4)

```mermaid
flowchart LR
  subgraph checkout-api
    API[API REST]
    L1[lambda-authorize]
    L2[lambda-notify]
  end
  API --> L1
  L1 --> DB[(payments-db)]
  L1 --> Q[[payment-events]]
  Q --> L2
```

## Dados (camada 4)

```mermaid
erDiagram
  PAYMENT ||--o{ INSTALLMENT : tem
  PAYMENT }o--|| ORDER : paga
```

## Estados (camada 4)

```mermaid
stateDiagram-v2
  [*] --> criado
  criado --> em_analise
  em_analise --> autorizado
  em_analise --> negado
  autorizado --> capturado
  capturado --> estornado
```

## Implantação (camada 6)

```mermaid
flowchart TB
  subgraph prod["Produção (sa-east-1)"]
    APIGW[API Gateway] --> L1[lambda-authorize]
    L1 --> DB[(RDS payments-db)]
    L1 --> SQS[[SQS payment-events]]
  end
```
