# Runbook — Conciliação

> Doc citado em `sub-pagv-conciliacao` · tipo: runbook

## Arquivo do adquirente não chegou

1. Confirmar no SFTP se o arquivo do dia existe.
2. Se não existir até 08:00, acionar o adquirente e avisar o financeiro.
3. Reprocessar com o job `CONC0100` manualmente quando o arquivo chegar.
