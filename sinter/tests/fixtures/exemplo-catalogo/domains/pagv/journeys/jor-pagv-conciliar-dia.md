# Conciliar o dia (batch noturno)

<!-- sinter:inicio — gerado a partir do YAML; não edite este bloco -->
> Jornada de [[dom-pagv]] · gatilho: Agenda batch, todo dia às 02:00 (D+1) · resultado: Relatório de divergências entregue ao financeiro às 07:00
> **Processamento noturno**
>   1. Recebe o arquivo do adquirente ([[sub-pagv-conciliacao]]) — se falhar: Arquivo não chegou → reprocessa às 08:00; financeiro avisado
>   2. Cruza vendas x pagamentos ([[sub-pagv-conciliacao]])
>   3. Gera relatório para o financeiro ([[sub-pagv-conciliacao]])
<!-- sinter:fim -->

## Contexto

_Por que esta jornada existe e quem a usa._

## Exceções e casos especiais

_O que os passos não contam: horários, retentativas, casos raros._
