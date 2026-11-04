# Responsabilidade da entrega

## Sources

- `../units-generation/unit-of-work.md`: fronteiras e entregas.
- `../units-generation/unit-of-work-dependency.md`: DAG técnico aprovado.
- `../units-generation/unit-of-work-story-map.md`: histórias e requisitos atribuídos.
- `docs/prd-dominio-2026-10-17/epics.md` e `_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md`: critérios e contratos existentes.

## Alocação

Todos os Bolts, uma passagem de construção por história, são executados pelo `aidlc-developer-agent` (AI). A formação de equipe foi dispensada. Uma história ativa por vez; sem equipes paralelas. O responsável conduz implementação e testes; o revisor independente declarado pela etapa confere o resultado e devolve achados para correção.

| Responsabilidade | Responsável |
|---|---|
| Implementar U1–U18 serialmente | aidlc-developer-agent |
| Revisão independente | Revisor declarado em Code Generation |
| Verificação integrada final | Lead de Build and Test |
| Decisões técnicas locais | Lead com base nos documentos, registradas por história |
| Autorização protegida indispensável | Pessoa |

Nenhum colaborador adicional será convocado em etapas inline com colaboradores desligados. O responsável não desfaz mudanças existentes. Não há equipe externa, contato por mensagem, publicação ou execução de deploy.

