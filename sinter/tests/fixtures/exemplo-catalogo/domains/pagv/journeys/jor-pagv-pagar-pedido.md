# Pagar um pedido

<!-- sinter:inicio — gerado a partir do YAML; não edite este bloco -->
> Jornada de [[dom-pagv]] · gatilho: Cliente clica em 'Pagar' no checkout · resultado: Pagamento capturado e evento PagamentoAprovado publicado
> **Pagar**
>   1. Escolhe forma de pagamento e parcelas ([[sub-pagv-checkout]])
>   2. Consulta antifraude ([[sub-pagv-autorizacao]]) — se falhar: Negado → pagamento recusado; cliente vê 'tente outro cartão'
>   3. Autoriza e captura no adquirente ([[sub-pagv-autorizacao]]) — se falhar: Timeout → não captura; nada é cobrado
>   4. Avisa os outros domínios ([[sub-pagv-autorizacao]])
<!-- sinter:fim -->

## Contexto

_Por que esta jornada existe e quem a usa._

## Exceções e casos especiais

_O que os passos não contam: horários, retentativas, casos raros._
