# Avaliação: a IA entende o domínio? (SM-2)

Questionário usado na métrica **SM-2** do [PRD](prd.md#8-métricas-de-sucesso), sobre o domínio **Pagamentos (Varejo) — PAGV** do [exemplo-catalogo](exemplo-catalogo/README.md).

## Como aplicar

1. **Rodada Sinter:** o agente recebe só a saída de `sinter get dom-pagv --level 1` e pode pedir mais níveis (`get … --level 2`, `read <doc>#âncora`).
2. **Rodada base:** o mesmo agente recebe o mesmo conhecimento em texto corrido (os `.md` do domínio, sem a estrutura).
3. Cada rodada é feita **3 vezes**; anote o agente e o modelo usados.
4. Pontuação por pergunta: **1** (certa), **0** (errada ou incompleta), **−1** (inventou uma resposta onde o gabarito diz "pendência"). Meta: média ≥ 9/10 e nenhum −1.

## Perguntas e gabarito

| # | Pergunta | Gabarito | Onde está |
|---|---|---|---|
| 1 | Para que existe o domínio PAGV, em uma frase? | Recebe, autoriza e concilia os pagamentos das lojas online e físicas do varejo. | `domain.yaml → purpose` |
| 2 | O PAGV cuida de antifraude? | Não. Antifraude é do domínio Risco (`dom-risco`); o PAGV só consulta. | `domain.yaml → doesNot` |
| 3 | Quais subdomínios o PAGV tem? | Checkout, Autorização e Conciliação. | `subdomains/` (calculado) |
| 4 | Existe legado no PAGV? Qual, e para onde vai? | Sim: o batch `CONC0100` (mainframe), em modernização, sendo substituído pelo Conciliação Service, rodando em paralelo por 3 meses (ADR-PAGV-004). | `sub-pagv-conciliacao.yaml → applications`, relação `modernized_by` |
| 5 | Quais regulações valem para a Conciliação? | Arranjos de pagamento (própria) + LGPD e Pix (herdadas do domínio). | `sub-pagv-conciliacao.yaml` + herança |
| 6 | Em que ordem acontece o pagamento de um pedido? | Escolher forma e parcelas → consultar antifraude → autorizar e capturar no adquirente → avisar os outros domínios (evento PagamentoAprovado). | `jor-pagv-pagar-pedido.yaml` |
| 7 | O que acontece se o antifraude negar? | O pagamento é recusado e o cliente vê "tente outro cartão". | passo `antifraude → onFailure` |
| 8 | Qual é a parcela mínima? | R$ 10,00. | `rule-pagv-parcela-minima-10-reais` |
| 9 | Qual é o horário-limite do arquivo do adquirente? | **Pendência:** não se sabe (docs dizem 6h, operação diz 8h). Inventar um horário vale −1. | `sub-pagv-conciliacao.yaml → unknowns` |
| 10 | Em quais repos está o código da Conciliação? | `repo-mainframe-pagv` (caminho `cobol/CONC*`) e `repo-conciliacao-service`. | aplicações do subdomínio (repos calculados) |

## Registro

| Data | Rodada | Agente / modelo | Execução 1 | Execução 2 | Execução 3 | Média | Inventou? |
|---|---|---|---|---|---|---|---|
| | Sinter | | | | | | |
| | Base | | | | | | |
