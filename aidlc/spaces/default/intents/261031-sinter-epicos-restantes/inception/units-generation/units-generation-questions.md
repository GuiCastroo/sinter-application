# Decomposição das histórias restantes do Sinter

## Sources

- Pedido original em `../../project-description.json`: execução autônoma, uma história por vez, preservação do trabalho local, revisão e testes automáticos, sem push/publicação/deploy.
- `docs/prd-dominio-2026-10-17/epics.md`: critérios de aceite das 18 histórias.
- `_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md`: contratos AD-25–AD-48, com precedência definida sobre histórias.
- `aidlc/spaces/default/codekb/harness_corp/`: análise recente reaproveitada.

## Q1. [Arquiteto] Fronteira das unidades

A. Uma unidade por história, cobrindo implementação, contratos e testes dessa capacidade.
B. Uma unidade por camada arquitetural.
X. Other (please specify)

[Answer]: A — instrução explícita de executar uma história por vez.

## Q2. [Arquiteto] Granularidade

A. As 18 histórias existentes: 2.1–2.6, 3.1–3.7, 4.1–4.5; concluir a implementação local da 2.1 antes de ampliar consultas.
B. Agrupar histórias por épico.
X. Other (please specify)

[Answer]: A — escopo fornecido pela pessoa; 3.7 aparece depois do Épico 4 no arquivo e está incluída.

## Q3. [Arquiteto] Dependências e execução

A. DAG com dependências técnicas reais; execução serial de uma história inteira por vez.
B. Paralelismo entre unidades independentes.
X. Other (please specify)

[Answer]: A — execução serial explicitamente solicitada. O DAG representa dependências, sem inventar dependências apenas para impor serialização.

## Q4. [Arquiteto] Contratos entre unidades

A. Reutilizar Request/Result, portas, registro de kinds e serviços puros da arquitetura, registrando decisões técnicas locais.
B. Criar APIs independentes por história.
X. Other (please specify)

[Answer]: A — decisão técnica delegada, baseada nas AD-26, AD-28, AD-38–AD-46. Rejeitada duplicação de contratos porque quebraria a fonte única de visões e serialização.

## Q5. [Arquiteto] Modelo de entrega

A. Mesma CLI Python hexagonal e pacote de skills; verificação local, sem publicar/push/deploy.
B. Serviços distribuídos independentes.
X. Other (please specify)

[Answer]: A — arquitetura e restrição explícita do pedido. A alternativa B acrescentaria infraestrutura e contrariaria o escopo.

## Plano de decomposição

As unidades são incrementos no mesmo pacote, implantadas em conjunto. `service` indica incremento da CLI executável; `spec` indica skill interpretada pelo agente. Nenhuma unidade introduz serviço remoto.

| Unit ID | Directory | História e capacidade | Kind | Depende de |
|---|---|---|---|---|
| U1 | u1-get-niveis | 2.1 — níveis 0/1 e herança; concluir trabalho local | service | Nenhuma |
| U2 | u2-calculados | 2.2 — repos, fronteiras, modernização e dados calculados | service | U1 |
| U3 | u3-jornadas | 2.3 — jornada, navegação e nível 2 | service | U1; U2 |
| U4 | u4-read | 2.4 — leitura por seção e sumário Markdown | service | Nenhuma |
| U5 | u5-find-areas | 2.5 — busca, listas e navegação por área | service | U1 |
| U6 | u6-avaliacao-ia | 2.6 — fatos do gabarito, roteiro e medição SM-2 | spec | U2; U3; U4; U5 |
| U7 | u7-catalog-init | 3.1 — iniciar catálogo e Git local | service | Nenhuma |
| U8 | u8-apply-dry-run | 3.2 — validar catálogo proposto, diff e resumo sem gravação | service | U13 |
| U9 | u9-apply | 3.3 — gravação transacional e commit restrito aos destinos | service | U8; U13 |
| U10 | u10-new-domain | 3.4 — rascunho de domínio e validação antecipada | service | U7; U9 |
| U11 | u11-new-subdomain-journey | 3.5 — rascunhos e edição do sumário preservando comentários | service | U10; U9 |
| U12 | u12-get-raw | 3.6 — conteúdo bruto, item contêiner e edição pelo apply | service | U1; U9 |
| U13 | u13-fmt | 3.7 — formatador canônico e aviso no validate | service | Nenhuma |
| U14 | u14-sinter-find | 4.1 — skill somente leitura e evals | spec | U3; U4; U5 |
| U15 | u15-entrevista | 4.2 — entrevista guiada, referências e evals | spec | U5; U10; U11; U12 |
| U16 | u16-skill-criar | 4.3 — busca, criação e confirmação antes de aplicar | spec | U15; U8; U9; U10 |
| U17 | u17-skill-estruturar | 4.4 — edição e estruturação de domínio existente | spec | U16; U11; U12 |
| U18 | u18-skills-install | 4.5 — empacotar e instalar skills com proteção de alterações locais | service | U14; U17 |

O primeiro incremento U1 já exercita CLI → caso de uso → domínio/portas → catálogo real. O DAG permite unidades independentes; o pedido mantém a execução serial. A escolha econômica da ordem pertence ao planejamento de entrega.

## Preservação e verificações

- Registrar baseline de testes e lista de alterações antes de modificar o código; preservar inclusive arquivos não rastreados.
- Cada história recebe evidência por critério de aceite, revisão e correções; executar verificações de contrato, camadas, lint, tipos e regressões aplicáveis.
- Formatação precede dry-run/aplicação porque a comparação canônica e a validação de FileFacts devem usar a mesma implementação.
- A arquitetura vence a duplicação de modelos YAML em assets de skills: modelos vêm de `sinter new --json`.
- Evals com LLM e SM-2 exigem execuções reais identificadas; não apresentar testes estáticos como prova de comportamento de modelo nem inventar notas. Identificar acesso indispensável quando chegar a essas histórias.
- Commits que a CLI cria são verificados em repositórios sintéticos de teste; nenhuma publicação ou push autorizado.

## Plan Approval

Approve Plan — gerar os quatro artefatos das unidades e submetê-los à revisão arquitetural.
Revise Plan — ajustar fronteiras, kinds ou dependências antes da geração.

[Answer]: Approve Plan
