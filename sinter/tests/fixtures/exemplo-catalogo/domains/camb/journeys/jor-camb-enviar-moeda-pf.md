# Enviar moeda (PF)

<!-- sinter:inicio — gerado a partir do YAML; não edite este bloco -->
> Jornada de [[dom-camb]] · gatilho: Cliente escolhe 'Enviar moeda' no app · resultado: Ordem liquidada via SWIFT e informada ao Bacen
> **Cotar**
>   1. Calcula a taxa e o valor final ([[sub-camb-cotacao]])
>   2. Confere se o cliente tem limite para o valor ([[sub-camb-limite]]) — se falhar: Sem limite → cliente não consegue seguir para contratar
>   3. Traz os dados cadastrais do cliente ([[sub-camb-dados-cliente]])
> **Contratar**
>   4. Registra o aceite do cliente ([[sub-camb-formalizacao]])
>   5. Gera a boleta da operação ([[sub-camb-boletagem]])
>   6. Completa dados para a operação ([[sub-camb-enriquecimento]])
>   7. Valida a operação antes de liquidar ([[sub-camb-validacao]]) — se falhar: Reprovada → operação não é liquidada [ASSUMPTION]
>   8. Registra na carteira de câmbio ([[sub-camb-carteira]])
>   9. Liquida a operação ([[sub-camb-liquidacao]])
>   10. Envia a ordem ao exterior (ext-swift)
>   11. Monitora prevenção à lavagem de dinheiro ([[sub-camb-pld]])
>   12. Informa a operação ao Banco Central (ext-bacen)
<!-- sinter:fim -->

## Contexto

_Por que esta jornada existe e quem a usa._

## Exceções e casos especiais

_O que os passos não contam: horários, retentativas, casos raros._
