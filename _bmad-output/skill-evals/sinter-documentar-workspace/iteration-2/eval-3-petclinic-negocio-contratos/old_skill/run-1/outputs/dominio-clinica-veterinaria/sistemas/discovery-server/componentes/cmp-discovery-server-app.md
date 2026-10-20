---
id: cmp-discovery-server-app
kind: component
subject: component:discovery-server:app
camada: 5
status: proposed
realiza: [sys-discovery-server]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-discovery-server/src/main/java/org/springframework/samples/petclinic/discovery/DiscoveryServerApplication.java
    version: aefaf7f
    extraction: extracted
---

# DiscoveryServerApplication
| Campo | Valor |
|---|---|
| Tipo | endpoint (servidor Eureka) |
| Gatilho | HTTP, heartbeats de registro dos demais serviços |
| Entrada | registro/renovação de instância (nome do serviço, host, porta) |
| Saída | lista de instâncias vivas por nome de serviço |
| Timeout / memória / concorrência | padrões do Eureka (não sobrescritos nas fontes lidas) |

## Dependências
- `config-server` (import opcional de configuração)

## Erros e retentativas
- Comportamento padrão do Eureka (auto-preservação, expiração de lease); nada customizado identificado nas fontes lidas.
