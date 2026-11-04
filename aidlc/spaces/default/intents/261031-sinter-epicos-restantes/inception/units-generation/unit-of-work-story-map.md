# Mapa de histórias e requisitos para unidades

## Sources

IDs FR e histórias transcritos de `docs/prd-dominio-2026-10-17/epics.md`; arquitetura de código citada em `unit-of-work.md`. Não há requirements.md/stories.md gerados neste fluxo porque essas etapas foram dispensadas no plano aprovado.

## Histórias existentes

| História externa | Unit ID | Directory |
|---|---|---|
| US2.1 | U1 | u1-get-niveis |
| US2.2 | U2 | u2-calculados |
| US2.3 | U3 | u3-jornadas |
| US2.4 | U4 | u4-read |
| US2.5 | U5 | u5-find-areas |
| US2.6 | U6 | u6-avaliacao-ia |
| US3.1 | U7 | u7-catalog-init |
| US3.2 | U8 | u8-apply-dry-run |
| US3.3 | U9 | u9-apply |
| US3.4 | U10 | u10-new-domain |
| US3.5 | U11 | u11-new-subdomain-journey |
| US3.6 | U12 | u12-get-raw |
| US3.7 | U13 | u13-fmt |
| US4.1 | U14 | u14-sinter-find |
| US4.2 | U15 | u15-entrevista |
| US4.3 | U16 | u16-skill-criar |
| US4.4 | U17 | u17-skill-estruturar |
| US4.5 | U18 | u18-skills-install |

## Requisitos existentes

| Requisito | Unit ID | Directory |
|---|---|---|
| FR15 | U1; U3; U6 | u1-get-niveis; u3-jornadas; u6-avaliacao-ia |
| FR6 | U1 | u1-get-niveis |
| FR20 | U1 | u1-get-niveis |
| FR21 | U1 | u1-get-niveis |
| FR4 | U2 | u2-calculados |
| FR5 | U2 | u2-calculados |
| FR7 | U2; U11 | u2-calculados; u11-new-subdomain-journey |
| FR8 | U2 | u2-calculados |
| FR10 | U2 | u2-calculados |
| FR19 | U2 | u2-calculados |
| FR11 | U3; U11 | u3-jornadas; u11-new-subdomain-journey |
| FR12 | U3; U11 | u3-jornadas; u11-new-subdomain-journey |
| FR13 | U3; U6 | u3-jornadas; u6-avaliacao-ia |
| FR16 | U4; U6 | u4-read; u6-avaliacao-ia |
| FR22 | U5; U6 | u5-find-areas; u6-avaliacao-ia |
| FR25 | U5 | u5-find-areas |
| FR1 | U7 | u7-catalog-init |
| FR18 | U8; U9; U13 | u8-apply-dry-run; u9-apply; u13-fmt |
| FR3 | U10 | u10-new-domain |
| FR2 | U12 | u12-get-raw |
| FR14 | U12 | u12-get-raw |
| FR23 | U12 | u12-get-raw |
| FR24 | U14; U15; U16; U17; U18 | u14-sinter-find; u15-entrevista; u16-skill-criar; u17-skill-estruturar; u18-skills-install |

## Cobertura e verificação

Todas as 18 histórias estão atribuídas uma vez; FR24 é transversal às skills. Dentro de cada unidade: preservar baseline → implementar camadas necessárias → testes por critério de aceite → revisar e corrigir → registrar evidência. A ordem entre unidades pertence a Delivery Planning.

NFR1 e NFR2 são verificados em U1–U5 e no SM-2 U6; NFR3 no conjunto integrado; NFR4 em U9/U12/U13; NFR5 em consultas e skills; NFR6 preservado pelo load comum. Não reimplementar critérios já satisfeitos no Epic 1.

