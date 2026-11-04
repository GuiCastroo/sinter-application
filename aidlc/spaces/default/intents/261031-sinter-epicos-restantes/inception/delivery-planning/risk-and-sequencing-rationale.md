# Riscos e justificativa de sequência

## Sources

- `../units-generation/unit-of-work.md`: fronteiras e entregas.
- `../units-generation/unit-of-work-dependency.md`: DAG técnico aprovado.
- `../units-generation/unit-of-work-story-map.md`: histórias e requisitos atribuídos.
- `docs/prd-dominio-2026-10-17/epics.md` e `_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md`: critérios e contratos existentes.

## Heurística

Valor primeiro nas consultas já iniciadas, depois redução de risco da escrita antes de autoria e skills. O formato canônico vem antes de apply para evitar comparações inconsistentes. A alternativa de ordem numérica integral foi rejeitada porque 3.7 é dependência de 3.2/3.3; paralelismo foi rejeitado pelo pedido de uma história por vez. Sem modelo numérico de priorização: não há estimativas de custo de atraso fornecidas para sustentar pontuações.

## Caminho de dependência

O caminho técnico de maior exposição à escrita passa por U13 → U8 → U9 → U10 → U11/U12 → U15 → U16 → U17 → U18. U1 destrava consultas; U3/U4/U5 destravam avaliação e a skill de leitura. Não há inversão topológica no plano. O DAG é a fonte autoritativa para escolher unidades prontas; este plano registra preferência econômica sem alterar seus vínculos.

## Registro de riscos

| Risco | Probabilidade | Impacto | Mitigação e unidade |
|---|---|---|---|
| Perder trabalho local da 2.1 | Média | Alto | Baseline antes de alterações, inspeção de diff, estender código atual U1 |
| Nível 1 exceder tokens | Média | Alto | Testes da fixture CAMB e heurística única U1–U6 |
| Consulta omitir fatos ou inventar certeza | Média | Alto | Contratos, herança com origem, gaps, Q9 e gabarito U1–U6 |
| Alterar YAML/comentários ou comparar formato como dados | Alta | Alto | Round-trip, idempotência e teste da fixture U13/U8/U9 |
| Commit incluir mudanças alheias ou deixar gravação parcial | Média | Alto | dirty por destino, commit_only e rollback com falha induzida U9 |
| Caminhos fora da raiz / symlinks | Média | Alto | Contenção em adaptadores e testes negativos U4/U9/U18 |
| Evals de LLM sem executor ou identificação | Média | Alto | Inspecionar executor em U6/U14; evidência real ou pendência explícita, nunca simular notas |
| Skill duplicar manifesto ou ignorar confirmação | Média | Alto | AD-42, CLI JSON e evals U15–U17 |
| Assets/schema fora do wheel | Média | Alto | Empacotamento e instalação isolada U18 |

## Condição de parada

Falhas de teste/revisão com correção técnica disponível são corrigidas automaticamente. Parar só por informação indispensável ausente, autorização protegida ou impossibilidade real sem solução dentro do escopo. Nenhum critério de aceite é marcado concluído sem evidência.

