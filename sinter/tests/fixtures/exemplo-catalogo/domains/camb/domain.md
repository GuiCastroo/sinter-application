# Câmbio

<!-- sinter:inicio — gerado a partir do YAML; não edite este bloco -->
> Domínio **CAMB** · área `area-cambio` · Permite que clientes comprem e enviem moeda estrangeira, da cotação até a liquidação e o reporte ao Banco Central.
> Subdomínios (ordem de leitura):
>   - [[sub-camb-cotacao]] — Calcula a taxa e o valor final da operação.
>   - [[sub-camb-limite]] — Confere se o cliente pode operar o valor pedido.
>   - [[sub-camb-dados-cliente]] — Traz os dados do cliente necessários para a operação.
>   - [[sub-camb-formalizacao]] — Registra o aceite do cliente e os termos da operação.
>   - [[sub-camb-boletagem]] — Gera a boleta (o registro da operação de câmbio).
>   - [[sub-camb-enriquecimento]] — Completa a operação com os dados exigidos para liquidar.
>   - [[sub-camb-validacao]] — Confere a operação antes de liquidar.
>   - [[sub-camb-carteira]] — Registra a operação na carteira de câmbio.
>   - [[sub-camb-liquidacao]] — Liquida a operação e dispara o envio ao exterior.
>   - [[sub-camb-pld]] — Monitora prevenção à lavagem de dinheiro.
> Jornadas: [[jor-camb-enviar-moeda-pf]]
> Regras do domínio todo: rule-camb-nao-liquidar-sem-validacao · rule-camb-reportar-bacen-d0
> Decisões: ADR-CAMB-001 (Cotação calculada em tempo real) · ADR-CAMB-002 (Tirar boletagem e liquidação do mainframe)
> Regulações: reg-bcb-cambio · reg-pld · reg-lgpd
> Aplicações por estado: legacy 2 · modern 8 · modernizing 1
<!-- sinter:fim -->

## Como funciona

_Escreva aqui, em texto corrido, como o domínio funciona de ponta a ponta._

## Decisões

_O texto completo de cada ADR listada acima: contexto, alternativas consideradas e por que esta foi escolhida._

## Armadilhas

_O que costuma dar errado e o que quem chega novo precisa saber._
