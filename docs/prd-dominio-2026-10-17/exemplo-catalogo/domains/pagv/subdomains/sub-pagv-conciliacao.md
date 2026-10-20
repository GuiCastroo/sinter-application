# Conciliação

<!-- sinter:inicio — gerado a partir do YAML; não edite este bloco -->
> Subdomínio de [[dom-pagv]] · Confere, todo dia, o que foi vendido contra o que o adquirente pagou.
> Aplicação `app-pagv-concil-batch` · modernizing · repos: repo-mainframe-pagv (batch/mainframe)
> Aplicação `app-pagv-conciliacao` · modern · repos: repo-conciliacao-service (api/java)
> Recebe de: [[ext-adquirente]] · [[sub-pagv-autorizacao]]
> Entrega para: [[dom-financeiro]]
> Regras: rule-pagv-conciliacao-d-mais-1 (+ as do domínio)
> Jornadas que passam aqui: [[jor-pagv-conciliar-dia]]
<!-- sinter:fim -->

## Como funciona

Todo dia, entre 02:00 e 07:00, a conciliação compara **o que foi vendido** (vendas capturadas em [[sub-pagv-autorizacao]]) com **o que o adquirente diz que pagou** (arquivo diário via SFTP). Hoje quem faz isso é o batch `CONC0100`, no mainframe, em três jobs: recebe o arquivo, cruza e gera o relatório ([[jor-pagv-conciliar-dia]]).

Desde outubro de 2026, o **Conciliação Service** roda em paralelo ao batch; as duas saídas são comparadas todo dia até o batch ser desligado (ADR-PAGV-004, herdada do domínio).

## Regras explicadas

### rule-pagv-conciliacao-d-mais-1
As vendas de um dia precisam estar conciliadas até as 07:00 do dia útil seguinte, porque o financeiro fecha o caixa às 08:00. Em feriado bancário o prazo vai para D+2, já que o adquirente não envia arquivo.

## Decisões

### ADR-PAGV-003 — Tolerância de centavos
**Contexto:** o adquirente arredonda taxas por transação e o total diverge em centavos quase todo dia; o financeiro gastava horas investigando diferenças de R$ 0,01.
**Alternativas:** (1) investigar tudo; (2) tolerância por lote; (3) tolerância por transação.
**Decisão:** tolerância de até R$ 0,05 **por transação**, aceita automaticamente. Por lote escondia erros reais somando centavos.
**Consequência:** o relatório separa "divergência tolerada" de "divergência real".

## Armadilhas

- O horário-limite do arquivo do adquirente **não é conhecido** (6h ou 8h?). Não assumir nenhum dos dois.
- Durante o paralelo, **não** corrigir divergências só num dos dois sistemas: a comparação diária perde o sentido.
