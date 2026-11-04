# Dependências externas

## Sources

- `../units-generation/unit-of-work.md`: fronteiras e entregas.
- `../units-generation/unit-of-work-dependency.md`: DAG técnico aprovado.
- `../units-generation/unit-of-work-story-map.md`: histórias e requisitos atribuídos.
- `docs/prd-dominio-2026-10-17/epics.md` e `_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md`: critérios e contratos existentes.

## Mapa

Um Bolt, uma passagem de construção por história, depende inicialmente apenas do repositório local, do ambiente Python e do Git. Nenhuma API remota ou dado privado é necessário para o produto.

| Dependência | Responsável | Bolts/unidades | Prazo | Contingência |
|---|---|---|---|---|
| Python/uv e dependências declaradas | Ambiente local; lead verifica | Todas | Verificação no baseline | Usar ambiente existente; pedir autorização de instalação apenas se indispensável |
| Git 2.40+ e identidade sintética de teste | Adaptador/testes | U7/U9 e autoria | Verificar antes do uso | Repositórios de teste isolados; nenhuma publicação |
| Autorização do comando de verificação | Pessoa | Checkpoints de construção | Pergunta protegida antes da construção | Aguardar sem atribuir autorização à autonomia |
| Executor real de evals LLM e identificação de modelo | Lead investiga ferramentas disponíveis | U6/U14–U17 | Antes da primeira avaliação | Usar executor disponível; se indisponível, pedir somente acesso indispensável e não fabricar resultados |
| skills-ref 0.1.x | Dependência de desenvolvimento conforme arquitetura | U14/U15/U18 | Antes do teste das skills | Validar ferramenta e ambiente; não tratar checagem própria como execução de skills-ref |

Não há entrega de outra equipe, API de produção, janela de dado, push ou deploy prevista.

