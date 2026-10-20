# Pagamentos (Varejo)

<!-- sinter:inicio — gerado a partir do YAML; não edite este bloco -->
> Domínio **PAGV** · área `area-varejo` · Recebe, autoriza e concilia os pagamentos das lojas online e físicas do varejo.
> Subdomínios (ordem de leitura):
>   - [[sub-pagv-checkout]] — Monta o pagamento do pedido: forma, parcelas e confirmação ao cliente.
>   - [[sub-pagv-autorizacao]] — Consulta antifraude, autoriza e captura o pagamento no adquirente.
>   - [[sub-pagv-conciliacao]] — Confere, todo dia, o que foi vendido contra o que o adquirente pagou.
> Jornadas: [[jor-pagv-pagar-pedido]] · [[jor-pagv-conciliar-dia]]
> Regras do domínio todo: rule-pagv-estorno-ate-90-dias · rule-pagv-nunca-guardar-cartao
> Decisões: ADR-PAGV-001 (Tokenizar cartão no adquirente) · ADR-PAGV-004 (Substituir o batch CONC0100 em paralelo)
> Regulações: reg-lgpd · reg-bcb-pagamentos-instantaneos
> Aplicações por estado: modern 3 · modernizing 1
<!-- sinter:fim -->

## Como funciona

_Escreva aqui, em texto corrido, como o domínio funciona de ponta a ponta._

## Decisões

_O texto completo de cada ADR listada acima: contexto, alternativas consideradas e por que esta foi escolhida._

## Armadilhas

_O que costuma dar errado e o que quem chega novo precisa saber._
