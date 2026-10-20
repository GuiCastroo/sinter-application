---
id: cmp-genai-vectorstore-loader
kind: component
subject: component:genai-service:vector-store-controller
camada: 5
status: proposed
realiza: [sys-genai-service]
realizado-por: []
provenance:
  - source: repo:spring-petclinic-microservices
    locator: spring-petclinic-genai-service/src/main/java/org/springframework/samples/petclinic/genai/VectorStoreController.java
    version: aefaf7f
    extraction: extracted
---

# VectorStoreController
Carrega os dados dos veterinários no vector store em memória, para permitir busca semântica pela tool `listVets`.

| Campo | Valor |
|---|---|
| Tipo | worker (listener de evento de startup) |
| Gatilho | evento `ApplicationStartedEvent` (na subida do serviço) |
| Entrada | arquivo `vectorstore.json` (classpath), se existir; caso contrário, resposta de `GET /vets` do `vets-service` |
| Saída | `VectorStore` populado em memória; opcionalmente grava um novo `vectorstore.json` em arquivo temporário local |
| Timeout / memória / concorrência | bloqueante (`.block()` na chamada reativa a `vets-service`) — roda uma única vez no startup |

## Dependências
- `vets-service` (`GET /vets`, via `WebClient` com `http://vets-service/`, resolvido por `lb://` + Eureka) — só é chamado se `vectorstore.json` não existir no classpath
- Sistema de arquivos local (grava arquivo temporário com permissões restritas `rwx------`)

## Erros e retentativas
- Sem tratamento de retry; se `vets-service` estiver indisponível no exato momento do startup e não houver `vectorstore.json`, o carregamento falha (comportamento de propagação não detalhado nas fontes lidas — **inferido**, a confirmar).
