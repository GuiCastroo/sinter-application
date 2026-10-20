---
id: cmp-order-manager-sanitize-order
kind: component
subject: component:order-manager-service:sanitize-order
camada: 5
status: proposed
realiza: [sys-order-manager-service]
realizado-por: []
provenance:
  - source: repo:serverless-coffee
    locator: "backends/5-order-manager/functions/sanitize/app.js"
    version: 9d494a2
    extraction: extracted
---
# sanitize-order
Confere se a bebida pedida e seus modificadores existem no cardápio vigente antes de gravar o pedido.

| Campo | Valor |
|---|---|
| Tipo | lambda |
| Gatilho | Invocação direta (`lambda:invoke`) pela `order-manager-state-machine` |
| Entrada | `{body: {drink, modifiers, userId}, menu: {Item: <cardápio em formato DynamoDB AttributeValue>}}` |
| Saída | `true`/`false` (booleano) |
| Timeout / memória / concorrência | 20 s / 128 MB |

## Dependências
- Nenhuma chamada externa; opera só sobre o payload recebido (usa `dynamodb-data-types` para "desembrulhar" o formato DynamoDB do cardápio)

## Erros e retentativas
Sem tratamento de exceção explícito no código — se `event.menu.Item` vier vazio/malformado, a função lança e a state machine aplica o `Retry` de 6 tentativas configurado no state `Sanitize order`. Nota de qualidade: a função não tem bloco `try/catch`, então qualquer erro de parsing derruba a invocação inteira.
