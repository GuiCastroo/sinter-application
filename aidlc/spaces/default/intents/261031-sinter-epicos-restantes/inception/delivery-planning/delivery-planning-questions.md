# Decisões de planejamento de entrega

## Sources

- `../units-generation/unit-of-work.md`: fronteiras e entregas.
- `../units-generation/unit-of-work-dependency.md`: DAG técnico aprovado.
- `../units-generation/unit-of-work-story-map.md`: histórias e requisitos atribuídos.
- `docs/prd-dominio-2026-10-17/epics.md` e `_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md`: critérios e contratos existentes.

## Q1. [Responsável pela entrega] Prioridade

A. Concluir consultas e comprovar fidelidade; reduzir risco da escrita antes das skills.
B. Começar pelas skills.
X. Other (please specify)

[Answer]: A — decisão técnica delegada pela pessoa, baseada no trabalho já iniciado e nas dependências.

## Q2. [Responsável pela entrega] Pontuação

A. Justificativa qualitativa baseada em valor e risco; sem pontuação inventada.
B. Modelo quantitativo com custos de atraso fornecidos.
X. Other (please specify)

[Answer]: A — não há métricas econômicas para sustentar a alternativa B.

## Q3. [Responsável pela entrega] Tamanho

A. Uma unidade/história por passagem de construção.
B. Agrupar histórias por épico.
X. Other (please specify)

[Answer]: A — instrução explícita da pessoa.

## Q4. [Responsável pela entrega] Execução

A. Serial e unit-major, com revisão/testes/correções automáticos.
B. Paralela.
X. Other (please specify)

[Answer]: A — instrução explícita da pessoa.

## Q5. [Responsável pela entrega] Dependências externas

A. Ambiente local e ferramentas de teste; evals LLM requerem evidência real.
B. Integração com produção.
X. Other (please specify)

[Answer]: A — arquitetura local e proibição de publicação.

## Q6. [Responsável pela entrega] Risco prioritário

A. Preservar trabalho local, fidelidade das consultas e integridade da escrita.
B. Velocidade à custa de validação.
X. Other (please specify)

[Answer]: A — preservar local e verificar todos os critérios foram solicitados.

## Respostas por incremento

Cada linha de bolt-plan.md identifica unidade, demonstração e hipótese; Definition of Done e team-allocation.md definem conclusão e responsável para todas as linhas. Não há decisões técnicas indispensáveis em aberto. Autorização do comando de verificação é registrada separadamente pelo checkpoint protegido.

