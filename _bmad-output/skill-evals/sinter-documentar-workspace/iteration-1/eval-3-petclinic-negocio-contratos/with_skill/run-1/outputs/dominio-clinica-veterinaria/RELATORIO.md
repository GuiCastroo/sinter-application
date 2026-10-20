# Relatório de documentação — Domínio Clínica Veterinária

Gerado a partir do repositório `spring-petclinic-microservices` (commit `aefaf7fa9eb0ab911a24c346ca0e4dc5837251c7`, 2026-09-23), lido em modo somente leitura em `.../fixtures/spring-petclinic-microservices`. Nenhum arquivo da fonte foi alterado.

Foco pedido: **capacidades de negócio, contratos das APIs e modelo de dados de cada serviço** — as camadas de infraestrutura e plataforma foram documentadas de forma mais enxuta, o suficiente para manter a rastreabilidade completa (capacidade → fluxo → sequência → sistema → componente → recurso).

## Itens por camada

| Camada | Tipo | Quantidade | `extracted` | `inferred` |
|---|---|---|---|---|
| 1. Negócio | capacidade | 5 | 0 | 5 |
| 1. Negócio | fluxo macro | 4 | 0 | 4 |
| 2. Domínio | domínio (README) | 1 | 0 | 1 (síntese) |
| 3. Subdomínio | subdomínio | 5 | 5 (estrutura) | — |
| 3. Subdomínio | sequência técnica | 4 | 4 | 0 |
| 4. Sistema | ficha de sistema | 8 | 8 | — |
| 4. Sistema | contrato de API | 15 | 15 | 0 |
| 5. Componente | componente | 12 | 12 | 0 |
| 6. Infraestrutura | recurso | 6 | 4 | 2 (topologia de banco em produção) |
| 6. Infraestrutura | ambiente | 2 | 2 | 0 |
| Transversal | termo (glossário) | 4 | 4 | 0 |
| Transversal | regra de negócio | 5 | 5 | 0 (1 com conflito registrado) |
| Transversal | padrão | 2 | 2 | 0 |
| Transversal | decisão (ADR) | 0 | — | — |
| **Total** | | **73 arquivos** | | |

A camada de negócio (capacidades e fluxos macro) é, como esperado, majoritariamente `inferred` — não havia brief de negócio, PRD ou backlog no repositório; as capacidades foram propostas a partir do que os sistemas realmente fazem no código.

## Conflitos encontrados

1. **`reg-tipos-de-pet`** — o `customers-service` não rejeita um `typeId` inexistente ao criar/atualizar um pet (`ifPresent` silencioso), enquanto a expectativa de negócio implícita é que todo pet tenha um tipo válido dentre os 6 cadastrados. Pode ser bug ou comportamento aceito — **a confirmar com o time de desenvolvimento**.
2. **`reg-degradacao-visitas`** — o `api-gateway` trata a falha de `visits-service` com fallback gracioso (lista vazia), mas não trata a falha de `customers-service` no mesmo endpoint de agregação. Assimetria não explicada no código.
3. **`res-mysql-visits`** — a FK `visits.pet_id → pets.id` só pode ser garantida pelo banco se ambas as tabelas estiverem no mesmo schema MySQL; em uma topologia de "um banco por serviço" (mais provável em microsserviços), a integridade passaria a depender só da aplicação. A topologia real de bancos em produção não está neste repositório.

## Segredos encontrados (só localização, sem valores)

- `spring-petclinic-genai-service/src/main/resources/application.yml` — referencia as variáveis de ambiente `AZURE_OPENAI_KEY`, `AZURE_OPENAI_ENDPOINT` e `OPENAI_API_KEY` (esta última com default `demo`, não sensível). Nenhum valor de chave foi lido ou copiado; apenas o nome da variável e o arquivo.
- `docker-compose.yml` — repassa as mesmas três variáveis de ambiente ao container `genai-service` (`environment:`), sem valores fixos no arquivo.

Nenhuma outra credencial, token ou string de conexão foi encontrada nos arquivos lidos.

## Lacunas relevantes (não é bug, é ausência de evidência)

- **Nenhum ADR, brief de negócio ou documento de arquitetura** foi encontrado no repositório (a pasta `docs/` só contém imagens). Por isso, a pasta `decisoes/` não foi criada — não havia decisão real para documentar, e nenhuma foi inventada.
- **Nenhum evento assíncrono** (fila, tópico, webhook) existe neste código — toda comunicação é HTTP síncrona via Eureka. Registrado explicitamente no `README.md` do domínio.
- **A configuração real de banco de dados em produção** (MySQL: host, credenciais, uma instância por serviço ou compartilhada) vive num repositório Git externo (`spring-petclinic-microservices-config`), referenciado pelo `config-server` mas fora do escopo lido.
- **Dono/CODEOWNERS**: nenhum dos 8 sistemas tem dono formalmente identificado no repositório.
- **Portas de negócio em produção**: `docker-compose.yml` fixa portas (8081–8084, 8080, 8761, 8888, 9090), mas os `application.yml` dos serviços de negócio não têm `server.port` explícito — a porta efetiva fora do compose local não está confirmada.

## Perguntas para as pessoas

**Para o PM / dono do produto:**
1. As capacidades propostas (`cap-cadastro-clientes-pets`, `cap-gestao-corpo-clinico`, `cap-registro-consultas`, `cap-atendimento-omnicanal`, `cap-atendimento-inteligente`) refletem como o negócio pensa esse domínio, ou faltam capacidades reais (agendamento, faturamento, prontuário clínico) que simplesmente não têm código ainda?
2. Existe um fluxo de cadastro/gestão do corpo clínico (contratar/editar veterinário) que não está neste repositório?
3. Quais indicadores de negócio importam para cada fluxo (volume, tempo de atendimento, taxa de uso do assistente virtual)? Nenhum foi encontrado no código.

**Para o arquiteto:**
4. A topologia real de banco de dados em produção é um MySQL por serviço (`customers`, `vets`, `visits` separados) ou uma instância compartilhada? Isso muda a análise de acoplamento e a regra de FK `visits.pet_id → pets.id`.
5. A assimetria no `ApiGatewayController` (fallback só para `visits-service`, não para `customers-service`) é intencional?
6. Existe algum outro domínio (fora deste repositório) que consome ou é consumido por este? O contexto de domínio ficou "isolado" por falta de evidência, não necessariamente porque é isolado de fato.

**Para o tech lead / dev:**
7. `customers-service` permite salvar um pet com `typeId` inválido sem erro (o tipo simplesmente fica nulo) — é o comportamento esperado?
8. Qual é o timeout efetivo do circuit breaker do `api-gateway` (`getOwnerDetails` e o do Resilience4j nas rotas)? Não encontrado em `application.yml`.
9. Onde a `ChatMemory` do `genai-service` é persistida (em memória do processo, Redis, banco)? Não identificado nas fontes lidas.

## Estrutura gerada

```
dominio-clinica-veterinaria/
  README.md
  capacidades/            (5)
  fluxos/                 (4 fluxos macro + 4 sequências técnicas)
  subdominios/            (5)
  sistemas/
    customers-service/    (ficha + 2 componentes + 8 contratos)
    vets-service/         (ficha + 1 componente + 1 contrato)
    visits-service/       (ficha + 1 componente + 3 contratos)
    api-gateway/          (ficha + 2 componentes + 2 contratos)
    genai-service/        (ficha + 3 componentes + 1 contrato)
    config-server/        (ficha + 1 componente)
    discovery-server/     (ficha + 1 componente)
    admin-server/         (ficha + 1 componente)
  infraestrutura/
    recursos/             (6)
    ambientes/            (2)
  glossario/              (4)
  regras-de-negocio/      (5)
  padroes/                (2)
  RELATORIO.md
```

Todos os itens nascem com `status: proposed`. Cabe a uma pessoa (PM para negócio/domínio, arquiteto/tech lead para sistema/infra) revisar e promover para `approved`.
