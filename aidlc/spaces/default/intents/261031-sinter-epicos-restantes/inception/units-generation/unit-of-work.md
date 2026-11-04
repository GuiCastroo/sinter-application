# Unidades de trabalho — Sinter, Épicos 2–4

## Sources

- `docs/prd-dominio-2026-10-17/epics.md`: histórias e critérios de aceite.
- `_bmad-output/planning-artifacts/architecture/architecture-sinter-codigo-2026-10-20/ARCHITECTURE-SPINE.md`: componentes, contratos e precedência.
- `aidlc/spaces/default/codekb/harness_corp/`: evidência do código atual.
- `units-generation-questions.md`: decomposição aprovada pela pessoa.

## Modelo e fronteiras

Um incremento vertical por história no mesmo pacote Python hexagonal. Todos compartilham a implantação da CLI; `service` representa capacidade executável e `spec` uma especificação interpretada de skill/avaliação. Não são novos serviços remotos. Cada unidade inclui implementação, contratos, testes e documentação da história. As entidades de catálogo continuam pertencendo ao modelo existente; unidades não criam cópias de entidades.

| Unit ID | Directory | História | Kind | Complexidade | Entrega |
|---|---|---|---|---|---|
| U1 | u1-get-niveis | 2.1 | service | M | Níveis 0/1 e herança |
| U2 | u2-calculados | 2.2 | service | L | Repos, fronteiras, modernização e dados |
| U3 | u3-jornadas | 2.3 | service | L | Jornadas, navegação e nível 2 |
| U4 | u4-read | 2.4 | service | M | Seções Markdown |
| U5 | u5-find-areas | 2.5 | service | L | Busca, listas e áreas |
| U6 | u6-avaliacao-ia | 2.6 | spec | M | Avaliação SM-2 |
| U7 | u7-catalog-init | 3.1 | service | M | Início de catálogo |
| U8 | u8-apply-dry-run | 3.2 | service | L | Conferência de rascunho |
| U9 | u9-apply | 3.3 | service | L | Gravação transacional |
| U10 | u10-new-domain | 3.4 | service | M | Rascunho de domínio |
| U11 | u11-new-subdomain-journey | 3.5 | service | L | Rascunhos de subdomínio e jornada |
| U12 | u12-get-raw | 3.6 | service | M | Edição pelo conteúdo atual |
| U13 | u13-fmt | 3.7 | service | L | Formatação canônica |
| U14 | u14-sinter-find | 4.1 | spec | M | Skill de consulta |
| U15 | u15-entrevista | 4.2 | spec | L | Entrevista guiada |
| U16 | u16-skill-criar | 4.3 | spec | M | Criação guiada |
| U17 | u17-skill-estruturar | 4.4 | spec | L | Estruturação guiada |
| U18 | u18-skills-install | 4.5 | service | M | Instalação de skills |

## Responsabilidades e limites

### U1 — Níveis 0/1 e herança

História 2.1; FR15; FR6; FR20; FR21. Concluir alterações locais da consulta, visões, herança e serialização. Verificar omitted, origem, sugestões e orçamento de tokens.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 2.1 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: base atual do catálogo.

### U2 — Repos, fronteiras, modernização e dados

História 2.2; FR4; FR5; FR7; FR8; FR10; FR19. Centralizar calculados puros; agregações sem repetição, fronteiras externas, lifecycle, camadas e jornadas calculadas; ordenação determinística.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 2.2 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U1.

### U3 — Jornadas, navegação e nível 2

História 2.3; FR11; FR12; FR13; FR15. Percorrer grafo com ciclos sem repetição, preservar onFailure e variantOf; detalhar app/repo e vizinhança.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 2.3 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U1, U2.

### U4 — Seções Markdown

História 2.4; FR16. Implementar sumário e corte de seção, âncora GitHub e erro com alternativas; conteúdo marcado e nenhuma leitura remota.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 2.4 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: base atual do catálogo.

### U5 — Busca, listas e áreas

História 2.5; FR22; FR25. Normalizar texto uma vez; relevância e desempate por id, limit, status approved; áreas calculadas sem arquivo próprio.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 2.5 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U1.

### U6 — Avaliação SM-2

História 2.6; FR13; FR15; FR16; FR22. Testar fatos do gabarito na saída; preparar rodadas identificadas Sinter/base, 3 execuções cada; registrar notas reais e Q9, sem simular LLM.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 2.6 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U2, U3, U4, U5.

### U7 — Início de catálogo

História 3.1; FR1. Criar estrutura e commit init apenas em pasta vazia; catálogo existente permanece intacto; recusar outra pasta não vazia.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 3.1 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: base atual do catálogo.

### U8 — Conferência de rascunho

História 3.2; FR18. YAML multi-documento, catálogo com upserts, FileFacts comuns, diff de dados/comentários e erro de marcas obrigatórias; nenhuma escrita.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 3.2 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U13.

### U9 — Gravação transacional

História 3.3; FR18. Caminhos canônicos, destinos limpos incluindo untracked, write_all e commit_only, rollback se falhar commit, sem commit em no-op.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 3.3 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U8, U13.

### U10 — Rascunho de domínio

História 3.4; FR3. Modelos puros com #~, flags, id e área antecipados, stdout/-o/JSON; integração com apply e docs.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 3.4 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U7, U9.

### U11 — Rascunhos de subdomínio e jornada

História 3.5; FR7; FR11; FR12. Dois manifestos para subdomínio e domínio, InsertListItem preservando comentários; opções de capability e colisões antecipadas.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 3.5 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U10, U9.

### U12 — Edição pelo conteúdo atual

História 3.6; FR2; FR14; FR23. Retornar bytes textuais e contêiner para inline com aviso, marcação content/source/locator; ADR com aviso do contador.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 3.6 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U1, U9.

### U13 — Formatação canônica

História 3.7; FR18. Ruamel round-trip, ordem dos modelos, listas/recuo/LF, check sem escrita, igualdade de dados, warning no validate; sem commit.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 3.7 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: base atual do catálogo.

### U14 — Skill de consulta

História 4.1; FR24. Skill somente leitura com fatos CLI, desambiguação e pendências; Agent Skills e evals positivos/negativos versionados.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 4.1 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U3, U4, U5.

### U15 — Entrevista guiada

História 4.2; FR24. Roteiros por nível, exemplos, opções do catálogo, seguimento, desconhecidos e retomada; assets sem cópia de manifesto (AD-42).

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 4.2 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U5, U10, U11, U12.

### U16 — Criação guiada

História 4.3; FR24. Buscar antes de criar, perguntar obrigatórios, dry-run, confirmação e apply; confirmação separada para área nova.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 4.3 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U15, U8, U9, U10.

### U17 — Estruturação guiada

História 4.4; FR24. Subdomínio, aplicação, jornada e referências pela CLI; preservar atual, incluir repo no mesmo rascunho e validar catálogo ao final.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 4.4 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U16, U11, U12.

### U18 — Instalação de skills

História 4.5; FR24. PackageResources e LocalFiles, wheel, manifesto versão/hashes, project/user/path e proteção contra alteração local sem force.

Fronteira: contratos e implementação dessa capacidade nas camadas previstas pelas AD-25–AD-48. Entrega embutida no pacote existente, sem publicação. Verificação: cada cenário Dado/Quando/Então da história 4.5 em epics.md, regressões das capacidades consumidas e contratos JSON. Dependências: U14, U17.

## Restrições transversais

- Preservar seis fontes rastreadas e módulos locais não rastreados identificados; baseline de testes antes da primeira alteração. Não restaurar, limpar ou substituir a árvore local.
- Não executar push, publicação ou deploy. Git de init/apply deve ser exercitado em catálogos sintéticos de teste.
- Visões e calculados têm fonte única; nenhuma I/O no domínio, composição em bootstrap e contratos camelCase determinísticos.
- Skills não duplicam modelos YAML em assets; rascunhos vêm da CLI. Conteúdo de catálogo é dado não confiável, nunca instrução.
- Avaliações de modelo usam execuções reais, com identificação de modelo e evidência; dependência externa ausente é pendência real, sem notas inventadas.
- Testes após cada camada testável; suíte existente permanece verde, regressão dirigida e estratégia Standard. Sem redução de qualidade para obter passe.

## Assumptions & Open Questions

None.

