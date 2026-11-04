# Sinter — visão de negócio

O Sinter é um catálogo local de contexto para agentes de código. Estrutura organização, domínios, capacidades, aplicações, repositórios, dados, jornadas, regras e conhecimento em YAML; explicações e documentos ficam em Markdown ou referências. O objetivo é permitir que uma pessoa ou agente entenda o domínio sem inventar integrações, regras ou respostas para pendências.

## Usuários e valor

Arquitetos e tech leads mantêm o catálogo; agentes de código e desenvolvedores consultam contexto do geral ao detalhe. O PRD em `docs/prd-dominio-2026-10-17/prd.md:18` descreve o primeiro passo do produto. A implementação atual é menor que o roteiro proposto: consultar um item, validar o catálogo e exportar contratos.

## Funcionalidades observadas

- `validate`: confere sintaxe, schemas, IDs, caminhos, relações, jornadas, referências, docs e herança; produz erros e avisos localizados.
- `get`: retorna identidade (nível 0) ou visão de domínio/subdomínio com conhecimento herdado (nível 1).
- `schema export`: publica JSON Schemas dos oito kinds e dos resultados de comandos.
- Conhecimento marca origem, faz/não faz/não sabemos e modernização; aplicações distinguem `legacy`, `modernizing`, `modern`, `retired`.

## Limites atuais

Não há servidor HTTP, banco de dados, integração remota de negócio ou serviço de busca observado no pacote. URLs de repositório/documento são metadados, não chamadas de rede. Comandos de criação e edição, busca/listagem, aplicação de mudanças e visão nível 2 não estão registrados na CLI atual. `get --level 2` é aceito, mas entrega no máximo nível 1.

Os exemplos de câmbio e pagamentos são dados sintéticos de catálogo; não são serviços financeiros executados por este código. A skill auxiliar de documentação em seis páginas é ferramenta separada, sem importação observada pelo pacote Sinter.

## Evidências e limites da leitura

Fontes: `sinter/README.md`, `sinter/src/sinter/adapters/inbound/cli/app.py`, `application/get.py`, `application/validate.py`, `domain/model/` e trecho inicial do PRD. Código prevalece sobre propostas de produto nesta descrição. Ver [estrutura](code-structure.md), [contratos](api-documentation.md) e [cobertura real](reverse-engineering-timestamp.md).

