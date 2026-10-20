---
review: versions
target: ../ARCHITECTURE-SPINE.md (seção Stack + tecnologias citadas nos ADs)
date: '2026-10-17'
method: 'npm registry (dist-tags, time, peerDependencies, engines), PyPI JSON, GitHub API, docs oficiais do Node, busca web'
---

# Revisão de versões — Sinter (spine de 2026-10-17)

## Veredito

Todas as tecnologias existem, estão ativas e cabem na arquitetura. A tabela Stack tem **quatro versões desatualizadas ou erradas**: yaml, @hono/node-server, R3F e o Vercel AI SDK com ai-sdk-ollama. Também tem **duas decisões que precisam de nota**: TypeScript 6.0 contra 7.0 e Node 24 com `node:sqlite` ainda em RC. Nada bloqueia a fatia 1. O único risco real de quebra é o R3F 9.7 com React 19.3, na fatia 2.

## Tabela de verificação

| Tecnologia | Na spine | Verificado (2026-10-17) | Status |
| --- | --- | --- | --- |
| Node.js | 24 LTS (mínimo) | 24.22.0 é a linha atual. O 24 sai de Active LTS para **Maintenance em ~2026-10-20**, e o **26 vira LTS em ~2026-10-28**. EOL do 24: 2028-04-30 | OK, com nota |
| TypeScript | 6.0 | `latest` = **7.0.2** (GA em 2026-07-08, compilador em Go). A última 6.x é 6.0.3 (2026-04-16). O 7.0 **não tem API programática**; a nova API vem no 7.1. O typescript-eslint ainda depende do 6 (pacote `@typescript/typescript6`) | Desatualizado, com justificativa possível |
| pnpm | 12.x | `latest` = **12.14.0** (2026-10-15). O 12.0 saiu em 2026-08-26 (reescrita em Rust) e já é a tag `latest` no npm | OK |
| zod | 4.x | `latest` = **4.6.7** (2026-10-12). O AI SDK 6 e o 7 aceitam `zod ^4.1.8` | OK |
| yaml (eemeli) | 2.8.x | `latest` = **2.9.1** (2026-09-11). O 2.9.0 saiu em 2026-05-11, e o 3.0.0 está em pré-release (`next` = 3.0.0-2) | **Desatualizado** |
| node:sqlite | embutido | Sem flag desde 22.13/23.4. É **Stability 1.2 (Release candidate)** no Node 24 (RC **a partir do 24.15.0**) e **continua RC no 26.12.0**, ou seja, não é estável | OK, com nota (e corrigir o memlog) |
| Graphify (`graphifyy`) | 0.9.x | PyPI **0.9.92** (2026-10-16), `requires_python >=3.10`. O repo mudou para **Graphify-Labs/graphify** (Apache-2.0). Saiu cerca de um patch por dia (0.9.65 → 0.9.92 em quatro semanas) | OK, mas fixar o patch |
| betterleaks | 1.x | GitHub betterleaks/betterleaks (MIT, ativo). Estável: **v1.9.0** (2026-09-29). **v2.0.0-rc.2** saiu em 2026-10-07. É binário, não está no npm | OK, com o 2.0 chegando |
| mammoth | 1.x | `latest` = **1.13.0** (2026-09-26) | OK |
| Hono | 4.x | `latest` = **4.13.13**. **Hono 5.0.0-rc.1** saiu em 2026-10-10 (engines: Node >=22.12) | OK, com o 5 chegando |
| @hono/node-server | "4.x" (agrupado com Hono) | `latest` = **2.1.5** (peer `hono ^4 \|\| ^5.0.0-0`, Node >=20). Não existe 4.x | **Versão errada** |
| React | 19.x | `latest` = **19.3.1** | OK |
| Vite | 8.x | `latest` = **8.3.4** (Node `^20.19 \|\| >=22.12`) | OK |
| @react-three/fiber | R3F 9.7 | `latest` = **9.8.2** (2026-10-14). O peer do **9.7.x é `react >=19 <19.3`**, então **não aceita o React 19.3**. O 9.8.x aceita `<19.4`. O 10.x está em alpha | **Desatualizado, com conflito de peer** |
| three.js | sem versão | `latest` = 0.186.1 (R3F pede `>=0.156`) | Falta a versão |
| Vercel AI SDK | `ai` 6.x (e "v6" no AD-9) | `latest` = **7.0.143**. O **v7 saiu em 2026-06-25** (ESM-only, Node >=22). O v6 segue na tag `ai-v6` (6.0.309), em manutenção | **Desatualizado** |
| @ai-sdk/anthropic, @ai-sdk/openai | sem versão | Para o v7: 4.x (`latest` 4.0.82 / 4.0.96). Para o v6: 3.x | Falta a versão |
| ai-sdk-ollama | 3.x | `latest` = **4.5.1** (peer `ai ^7.0.137`). A **3.x está congelada** em 3.8.8 (2026-06-18, peer `ai ^6`) | **Desatualizado** |

## Achados

### V-1 (Alta, fatia 2): R3F 9.7 não aceita o React 19.3

O `@react-three/fiber@9.7.x` declara `react >=19 <19.3`. Com "React 19.x" e o `latest` em 19.3.1, uma instalação nova gera conflito de peer ou um runtime não suportado. O 9.8.x (desde 2026-09-22) cobre `<19.4`.

- **Correção:** `three.js + @react-three/fiber` → `R3F 9.8.x + three 0.186.x`.

### V-2 (Média, fatia 2): o Vercel AI SDK já está na v7

A v7 saiu em 2026-06-25. A v6 recebe só manutenção. O `ai-sdk-ollama` 3.x parou em junho, e a linha ativa (4.x) exige `ai ^7`. Começar a fatia 2 na v6 já nasce em linha legada. A v7 é ESM-only e pede Node >=22, o que é compatível com a spine.

- **Correção na Stack:** `` `ai` 7.x + `@ai-sdk/anthropic` 4.x, `@ai-sdk/openai` 4.x, `ai-sdk-ollama` 4.x ``.
- **Correção no texto do AD-9:** "Vercel AI SDK v6" → "Vercel AI SDK v7" (ou só "Vercel AI SDK", com a versão vindo da Stack). Lembrar também o memlog (linhas 12 e 22).

### V-3 (Média): yaml 2.8.x está desatualizado

O `yaml` 2.9.0 saiu em 2026-05-11 e o 2.9.1 em 2026-09-11. O 3.0 está em pré-release e não deve ser adotado agora.

- **Correção:** `yaml` → `2.9.x`.

### V-4 (Média): a versão do @hono/node-server está errada

A linha "Hono + @hono/node-server | 4.x" sugere 4.x para os dois pacotes, mas o `@hono/node-server` está na **2.x** (2.1.5). Além disso, o **Hono 5** está em RC desde 2026-10-10 e provavelmente sai antes da fatia 2. O node-server 2.1.x já aceita os dois.

- **Correção:** `Hono 4.x + @hono/node-server 2.x (fatia 2; reavaliar Hono 5 ao iniciar)`.

### V-5 (Média, decisão): TypeScript 6.0 contra 7.0

O `latest` do TypeScript já é o 7.0.2 (Go, GA em 2026-07-08). Ficar no 6.0 é defensável, porque o 7.0 não tem API programática e o typescript-eslint ainda depende do 6. Mesmo assim, a spine precisa dizer que é uma escolha consciente. Sem isso, alguém instala `typescript@latest` e recebe o 7. O Sinter não usa a API do compilador, então o impacto fica só no tooling.

- **Opção A (conservadora):** `TypeScript 6.0.x (migrar para 7.x quando o typescript-eslint suportar)`.
- **Opção B:** `TypeScript 7.0.x (tsc/build) + @typescript/typescript6 para o lint`.

### V-6 (Baixa): mínimo do Node e status do node:sqlite

- O `node:sqlite` só é **Release candidate (1.2) a partir do Node 24.15.0**. Antes disso, no 24, era experimental. "24 LTS (mínimo)" deveria ser **24.15+**.
- O 24 entra em **Maintenance LTS por volta de 2026-10-20** e o **26 vira Active LTS por volta de 2026-10-28**. Manter o 24 como mínimo é razoável, mas o alvo de desenvolvimento e CI deveria ser o 26.
- **O memlog está errado:** a linha 13 diz "estável no Node 26". A doc do 26.12.0 ainda marca **1.2 Release candidate**. Por isso, isolar o acesso ao SQLite atrás do adaptador (já previsto no hexágono) e fixar testes de API.
- **Correção:** `Node.js 24.15+ (mínimo; alvo 26 LTS)` e `SQLite: node:sqlite embutido (Stability 1.2 RC)`.

### V-7 (Baixa): Graphify muda demais para "0.9.x" aberto

O 0.9.92 saiu em 2026-10-16, com cerca de 27 patches desde 2026-09-20, o que é sinal de projeto pré-1.0 instável. O repositório agora é `Graphify-Labs/graphify` (Apache-2.0) e exige Python >=3.10. Como o adaptador lê `graph.json`, uma mudança de formato entre patches quebra a importação em silêncio.

- **Correção:** `graphifyy 0.9.92 (pin exato via uv; atualização deliberada)`. O `sinter doctor` deve checar a versão e o Python >=3.10.

### V-8 (Baixa): betterleaks 2.0 está em RC

O 1.9.0 é o estável atual, e o v2.0.0-rc.2 saiu em 2026-10-07 (adiciona scan de contêineres). O projeto é MIT e ativo. "1.x" está correto, mas o adaptador `SecretScanner` deve fixar a versão do binário e o formato do relatório JSON.

- **Correção:** `betterleaks 1.9.x (avaliar 2.x quando sair do RC)`.

### V-9 (Info): três itens confirmados sem mudança

- **zod 4.x:** está no 4.6.7.
- **mammoth 1.x:** está no 1.13.0.
- **pnpm 12.x:** está no 12.14.0 e já é a tag `latest`. A reescrita em Rust mantém o lockfile e os comandos do 11.

## Stack sugerida (só as linhas que mudam)

| Name | Version |
| --- | --- |
| Node.js | 24.15+ (mínimo; alvo 26 LTS) |
| TypeScript | 6.0.x (7.x quando o typescript-eslint suportar) |
| yaml (eemeli/yaml) | 2.9.x |
| SQLite | `node:sqlite` embutido (Stability 1.2 RC) |
| Graphify (`graphifyy`, Python >=3.10 via uv) | 0.9.92 (pin exato) |
| betterleaks | 1.9.x |
| Hono + @hono/node-server (fatia 2) | Hono 4.x + node-server 2.x (reavaliar Hono 5) |
| three.js + @react-three/fiber (fatia 2) | R3F 9.8.x + three 0.186.x |
| Vercel AI SDK (fatia 2) | `ai` 7.x + `@ai-sdk/anthropic` 4.x, `@ai-sdk/openai` 4.x, `ai-sdk-ollama` 4.x |

Fora da tabela, também é preciso trocar "Vercel AI SDK v6" no AD-9 e corrigir as linhas 12, 13 e 22 do `.memlog.md`.

## Fontes

- npm registry (`registry.npmjs.org`): dist-tags, `time`, `peerDependencies` e `engines` de zod, yaml, hono, @hono/node-server, mammoth, typescript, pnpm, vite, react, @react-three/fiber, three, ai, @ai-sdk/anthropic, @ai-sdk/openai e ai-sdk-ollama, consultados em 2026-10-17.
- PyPI: https://pypi.org/pypi/graphifyy/json
- GitHub API: betterleaks/betterleaks (releases v1.9.0, v2.0.0-rc.1, v2.0.0-rc.2) e Graphify-Labs/graphify.
- Node.js: https://nodejs.org/docs/latest-v24.x/api/sqlite.html (v24.22.0) e https://nodejs.org/api/sqlite.html (v26.12.0); https://endoflife.date/nodejs
- TypeScript 7.0 GA: https://gihyo.jp/article/2026/07/typescript-7-0 , https://ecorpit.com/typescript-7-migration-readiness-eslint-astro-blockers-2026/ , https://www.visualstudiomagazine.com/articles/2026/03/23/typescript-6-0-ships-as-final-javascript-based-release-clears-path-for-go-native-7-0.aspx
- pnpm 12: https://socket.dev/blog/pnpm-12 , https://infoq.com/news/2026/09/pnpm-12-rust
- AI SDK 7 (migração): https://mcpservers.org/pt-BR/agent-skills/vercel/ai/migrate-ai-sdk-v6-to-v7
