# Modelos por tipo de item

Todos começam com o cabeçalho YAML descrito no SKILL.md. Abaixo, só o corpo. Omita seções que não se aplicam; não deixe seção vazia.

## canvas (negocio/canvas.md): a porta de entrada da camada 1

Uma página só, para alguém de negócio entender o domínio em 2 minutos. **Só o principal**: no máximo 5 itens por bloco, frases curtas, sem jargão técnico. Cada bloco é uma seção `##`, e o site desenha os blocos como um canvas. Tudo o que for dedução sua fica marcado com "(a confirmar)".

```markdown
# Canvas do domínio <Nome>

## Propósito
<Uma ou duas frases: por que este domínio existe para a empresa.>

## Para quem
- <cliente ou ator> — <o que ele quer>

## Proposta de valor
- <o que o domínio entrega que importa para o negócio>

## Capacidades principais
- [<capacidade>](../capacidades/<slug>.md) — <uma linha>

## Fluxos principais
- [<fluxo>](../fluxos/<slug>.md) — <uma linha>

## Eventos que importam
- <evento de negócio> — <o que significa>

## Regras críticas
- [<regra>](../regras-de-negocio/<slug>.md)

## Indicadores
- <indicador> (a confirmar)

## Fronteiras
- Dentro: <…>
- Fora: <…>

## Linguagem
- **<termo>**: <definição curta>

## Riscos e dúvidas
- <o que ninguém sabe responder ainda>
```

## capability (capacidades/<slug>.md)

```markdown
# <Nome em linguagem de negócio>
<Uma frase: o que a empresa consegue fazer.>

## Fluxos que a realizam
- [<fluxo>](../fluxos/<fluxo>.md)

## Sistemas envolvidos
- <sistema> — <papel>
```

## flow (fluxos/<slug>.md): fluxo macro, camada 1

```markdown
# <Nome do fluxo>
<Objetivo do fluxo para o negócio.>

## Atores
- <ator> — <papel>

## Etapas
| # | Etapa | Ator | Decisão ou resultado | Técnica |
|---|---|---|---|---|
| 1 | <etapa em linguagem de negócio> | <ator> | <…> | [passo 2–4](./<slug>.sequencia.md#passo-2) |

## Diagrama
<flowchart com subgraph por ator; ver diagramas.md>

## Indicadores
- <indicador> (a confirmar com o PM)

## Regras que governam
- [<regra>](../regras-de-negocio/<regra>.md)
```

## flow sequence (fluxos/<slug>.sequencia.md): passo a passo técnico, camada 3

```markdown
# <Nome do fluxo>: sequência técnica
Realiza as etapas do [fluxo macro](./<slug>.md).

## Diagrama
<sequenceDiagram; ver diagramas.md>

## Passos
### Passo 1
<quem chama quem, contrato, dados principais>
### Caminho de erro
<o que acontece quando cada chamada falha>
```

## domain (README.md): camada 2

```markdown
# Domínio <Nome>
<Propósito.>

## Fronteiras
- Dentro: <…>
- Fora: <…>

## Dono
<pessoa ou time>

## Subdomínios
| Subdomínio | Responsabilidade | Sistemas |
|---|---|---|

## Contexto
<C4Context ou flowchart; ver diagramas.md>

## Eventos de domínio
| Evento | Produtor | Consumidores | Contrato |
|---|---|---|---|
```

## subdomain (subdominios/<slug>.md)

```markdown
# Subdomínio <Nome>
<Responsabilidade.>

## Sistemas
| Sistema | Papel |
|---|---|

## Fluxos executados aqui
- [<fluxo>](../fluxos/<fluxo>.sequencia.md)
```

## system (sistemas/<s>/ficha.md)

```markdown
# <sistema>
<Responsabilidade em uma frase.>

| Campo | Valor |
|---|---|
| Subdomínio | |
| Dono | |
| Stack | |
| Repositório | |
| Criticidade | (a confirmar) |

## Contêineres
<C4Container ou flowchart; ver diagramas.md>

## Expõe
| Contrato | Tipo | Detalhe |
|---|---|---|

## Consome
| Sistema | Contrato | Tipo |
|---|---|---|

## Dados
<erDiagram das entidades principais>

## Estados
<stateDiagram-v2 das entidades com ciclo de vida>

## Qualidade
- Timeouts, retentativas, limites encontrados
```

## component (sistemas/<s>/componentes/<slug>.md)

```markdown
# <componente>
<O que faz.>

| Campo | Valor |
|---|---|
| Tipo | lambda / endpoint / worker / job |
| Gatilho | |
| Entrada | |
| Saída | |
| Timeout / memória / concorrência | |

## Dependências
- <recurso ou sistema> — <para quê>

## Erros e retentativas
<…>
```

## resource (infraestrutura/recursos/<slug>.md)

```markdown
# <recurso>
| Campo | Valor |
|---|---|
| Tipo | banco / fila / tópico / bucket / função / cluster |
| Tecnologia | |
| Ambientes | |
| Definido em | <arquivo de infra como código> |

## Usado por
- <componente ou sistema> — <leitura, escrita, publica, consome>
```

## environment (infraestrutura/ambientes/<slug>.md)

```markdown
# Ambiente <nome>
<Diferenças relevantes em relação aos outros ambientes.>

## Implantação
<flowchart de implantação; ver diagramas.md>
```

## contract (sistemas/<s>/contratos/<slug>.md)

```markdown
# <METHOD /path> ou <NomeDoEvento>
| Campo | Valor |
|---|---|
| Tipo | API / evento / arquivo |
| Produtor | |
| Consumidores | |
| Especificação | <caminho do OpenAPI/AsyncAPI, se houver> |

## Exemplo
<payload mínimo, sem dado pessoal>
```

## rule (regras-de-negocio/<slug>.md)

```markdown
# <Regra>
<O que o negócio exige, com o valor atual.>

## Onde está implementada
- <sistema/arquivo>

## Conflito
<se `conflito: true`: as versões e as fontes de cada uma>
```

## decision (decisoes/ADR-NNN-<slug>.md)

```markdown
# ADR-NNN <Título>
Status: <proposta | aceita | substituída> — Data: <AAAA-MM-DD>

## Contexto
## Opções consideradas
## Decisão
## Consequências
```

## standard (padroes/<slug>.md)

```markdown
# <Padrão>
<Como fazemos.>

## Exemplo
## Onde se aplica
```

## term (glossario/<slug>.md)

```markdown
# <Termo>
<Definição única.>

Não confundir com: <termos próximos>
```
