---
id: cmp-config-server-app
kind: component
subject: component:config-server:app
camada: 5
status: proposed
realiza: [sys-config-server]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-config-server/src/main/java/org/springframework/samples/petclinic/config/ConfigServerApplication.java
    version: aefaf7f
    extraction: extracted
---

# ConfigServerApplication
| Campo | Valor |
|---|---|
| Tipo | endpoint (servidor Spring Cloud Config, `@EnableConfigServer` presumido) |
| Gatilho | HTTP, requisições de configuração dos demais serviços na subida |
| Entrada | nome da aplicação + perfil ativo |
| Saída | propriedades de configuração (YAML/properties) |
| Timeout / memória / concorrência | não configurado explicitamente; limite de memória do container: 512M (`docker-compose.yml`) |

## Dependências
- Repositório Git externo (ou filesystem local via perfil `native`)

## Erros e retentativas
- Os clientes usam `optional:configserver:...` — se o config-server estiver indisponível, a subida do serviço cliente **não falha** (import opcional), mas o serviço roda sem as propriedades externas.
