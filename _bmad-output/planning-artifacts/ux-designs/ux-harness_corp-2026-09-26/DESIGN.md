---
name: Sinter
description: Identidade visual "Esmalte" do Sinter, app local para arquitetos, PMs e tech leads organizarem o contexto de domínios de software, e CLI para devs.
status: final
created: 2026-09-26
updated: 2026-09-26
sources:
  - ../../prds/prd-harness_corp-2026-09-26/prd.md
  - ../../briefs/brief-harness_corp-2026-09-26/brief.md
colors:
  # Superfícies (cerâmica escura, do mais externo para o mais elevado)
  backdrop: '#151719'
  chrome: '#1F2327'
  rail: '#1A1D20'
  canvas: '#2A2F34'
  surface: '#343A40'
  tile: '#3E454C'
  tile-highlight: '#4A525A'
  hairline: '#474E55'
  # Texto
  ink: '#E8E4DB'
  muted: '#9DA3A8'
  faint: '#6E757B'
  # Neon: o que está vivo
  neon: '#46F28E'
  neon-ink: '#0B2A17'
  # Esmaltes: tipos de integração
  glaze-api: '#7EA6F4'
  glaze-event: '#B69CF0'
  glaze-file: '#E2B566'
  # Estados
  conflict: '#EE6F7C'
  conflict-soft: '#F2B7BE'
  # Esmaltes de subdomínio (atribuídos em ordem; o domínio pode ter até 8)
  cluster-1: '#C9B8F2'
  cluster-2: '#7EA6F4'
  cluster-3: '#E2B566'
  cluster-4: '#B69CF0'
  cluster-5: '#8FD0E8'
  cluster-6: '#F0B27A'
  cluster-7: '#9FD9B0'
  cluster-8: '#F2D06B'
typography:
  display:
    fontFamily: 'Optima, "Avenir Next", sans-serif'
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.2'
  title:
    fontFamily: '"Avenir Next", "Helvetica Neue", sans-serif'
    fontSize: 18px
    fontWeight: '600'
    lineHeight: '1.3'
  body:
    fontFamily: '"Avenir Next", "Helvetica Neue", sans-serif'
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label:
    fontFamily: '"Avenir Next", "Helvetica Neue", sans-serif'
    fontSize: 12.5px
    fontWeight: '500'
    lineHeight: '1.4'
  caption:
    fontFamily: '"Avenir Next", "Helvetica Neue", sans-serif'
    fontSize: 11.5px
    fontWeight: '400'
    lineHeight: '1.4'
  code:
    fontFamily: 'Menlo, "SF Mono", monospace'
    fontSize: 12.5px
    fontWeight: '400'
    lineHeight: '1.7'
rounded:
  sm: 6px
  md: 10px
  lg: 14px
  xl: 16px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 20px
  '6': 24px
  rail-width: 76px
  list-width: 260px
  panel-width: 320px
components:
  button-primary:
    background: '{colors.neon}'
    foreground: '{colors.neon-ink}'
    radius: '{rounded.sm}'
    glow: '0 0 14px rgba(70,242,142,.35)'
  button-secondary:
    background: '{colors.surface}'
    foreground: '{colors.ink}'
    border: '{colors.hairline}'
    radius: '{rounded.sm}'
  system-card:
    background: 'gradient {colors.tile-highlight} → {colors.tile}'
    border: '{colors.hairline}'
    radius: '{rounded.lg}'
    tech-badge-radius: '{rounded.sm}'
  system-card-focus:
    border: '{colors.neon}'
    glow: 'blur 4px {colors.neon}'
  system-card-inferred:
    background: '{colors.canvas}'
    border: 'dotted 1.6px'
  system-card-no-access:
    background: 'transparent'
    border: 'dashed {colors.faint}'
  subdomain-group:
    background: 'rgba(255,255,255,.025)'
    border: 'cluster color at 35% (70% when it holds the focus)'
    radius: '{rounded.xl}'
  edge-label:
    background: '{colors.canvas}'
    border: 'type glaze'
    radius: '{rounded.full}'
    typography: '{typography.caption}'
  nav-rail-item-active:
    background: '{colors.surface}'
    indicator: '3px {colors.neon} with glow, on the rail edge'
  conflict-box:
    background: 'rgba(238,111,124,.07)'
    border: '{colors.conflict} at 45%'
    radius: '{rounded.md}'
  star:
    fill: 'radial gradient white → cluster color → {colors.canvas}'
    size: '4px + 1.4px por integração, máx. 16px'
  terminal:
    background: '{colors.rail}'
    typography: '{typography.code}'
---

## Brand & Style

O Sinter recebe conhecimento espalhado (repos, Confluence, PDFs, conversas) e o funde em algo sólido e confiável. O nome vem de *sinterizar*: fundir partículas soltas em uma peça. A identidade visual, chamada **Esmalte**, leva essa ideia para a tela.

- **O fundo é cerâmica escura**, em tons de grés cinza. Não é preto, e não é o "modo escuro" genérico.
- **O que já foi aprovado parece esmaltado**: cartões sólidos, levemente vidrados, com um ponto neon.
- **O que ainda é inferido aparece como partículas soltas**: linhas pontilhadas e poeira de pontos, algo que ainda não "sinterizou".
- **O neon verde marca o que está vivo**: o foco, o passo atual, o aprovado, a ação principal.

O público é técnico e exigente (arquitetos e tech leads). O tom visual é **preciso e calmo, com um único momento de espetáculo: o mundo do domínio**, um globo que gira com os subdomínios como constelações. Toda a ousadia está ali e no neon; o resto da interface é silencioso.

Referências trazidas pelo fundador: IcePanel (acabamento de modelagem C4, foco, fluxos, níveis de zoom) e Graphify (grafo esférico luminoso).

## Colors

- **Superfícies** (`{colors.backdrop}` → `{colors.tile-highlight}`): cinco camadas de cerâmica. Quanto mais elevado o elemento, mais clara a superfície. O canvas do mapa é `{colors.canvas}` com uma grade de pontos discreta.
- **Neon (`{colors.neon}`)**: é a única cor de ação e de "vivo". Usos permitidos:
  - sistema ou item em foco
  - passo atual de um fluxo
  - indicador de aprovado
  - botão primário
  - item ativo da navegação
  - saída "aplicado" na CLI

  Nunca usar como decoração, fundo de área grande ou cor de texto corrido. Se tudo brilha, nada brilha.
- **Esmaltes de integração**: API em cobalto (`{colors.glaze-api}`), evento em lilás (`{colors.glaze-event}`), arquivo/batch em âmbar (`{colors.glaze-file}`). O lilás substitui o verde-celadon original para não competir com o neon.
- **Conflito (`{colors.conflict}`)**: conflitos, integrações inferidas esperando confirmação, contadores de pendência. Aparece sempre em caixa de fundo suave (`conflict-box`), nunca como fundo cheio.
- **Esmaltes de subdomínio** (`cluster-1` a `cluster-8`): identificam cada constelação no Mundo, no Grafo e nas Caixas. São atribuídos na ordem em que os subdomínios são criados e se mantêm estáveis entre as visões.
- **Âmbar** também sinaliza "atenção": rascunho, desatualizado, edição manual detectada.

## Typography

- **Display: Optima** (com Avenir Next como fallback). Aparece só em nomes de domínio e subdomínio, nos títulos de tela e nos números grandes de resumo (34 sistemas, 88% aprovado). É o toque "cerâmico", humanista.
- **Interface: Avenir Next** em todo o resto, com a escala `title` 18, `body` 14, `label` 12,5 e `caption` 11,5.
- **Código: Menlo**, usado na CLI, em trechos de código citados como fonte, em caminhos de arquivo e na árvore do `.sinter/`.
- Frases com inicial maiúscula e o resto em minúsculas. **Não usar caixa-alta em rótulos**, com uma exceção: as siglas de tipo de artefato dentro de *badges* (ADR, PRD, EVT, SYS), que são identificadores.
- Linhas de texto com no máximo cerca de 75 caracteres nos painéis de leitura.

## Layout & Spacing

A estrutura do app é fixa, em quatro colunas:

```
┌──────┬──────────────┬───────────────────────────┬──────────────┐
│ Trilho│ Lista        │ Área de trabalho          │ Painel de    │
│ 76 px │ 260 px       │ (canvas ou conteúdo)      │ detalhe      │
│ nav   │ navegar      │ trabalhar                 │ inspecionar  │
└──────┴──────────────┴───────────────────────────┴──────────────┘
```

**Navegar à esquerda, trabalhar no centro, inspecionar à direita.** Essa decisão foi pedida explicitamente pelo fundador: menu e listas ficam à esquerda. A barra superior tem a marca, o caminho (breadcrumb), o seletor de nível (Empresa, Domínio, Sistema, Componente) e, quando existe, o seletor de visão (Mundo, Grafo, Caixas).

A escala de espaçamento é de base 4. Controles flutuantes sobre o canvas (busca, camadas, legenda, player de fluxo e minimapa) ficam a 16 px das bordas.

## Elevation & Depth

A profundidade vem de **luz, não de sombra**:
- **Cartões**: gradiente vertical sutil (topo mais claro) e sombra curta.
- **Foco**: brilho neon (desfoque de 4 a 5 px) em volta do elemento.
- **Painéis flutuantes sobre o canvas** (player de fluxo, menus): fundo com 94% de opacidade e desfoque do que está atrás.
- **Mundo 3D**: a profundidade é real. Estrelas atrás do globo desbotam, e as da frente ficam maiores e mais nítidas.

## Shapes

- Os raios crescem com o tamanho do elemento: `sm` para botões e *badges*, `md` para caixas de conteúdo, `lg` para cartões de sistema e `xl` para grupos de subdomínio.
- Rótulos de integração são pílulas (`full`).
- Sistemas externos e sem acesso usam **contorno tracejado**, sem preenchimento.
- Sistemas inferidos usam **contorno pontilhado**, que lembra partículas.

## Components

- **Cartão de sistema:** *badge* de tecnologia (duas letras com a cor da linguagem: Kt, Jv, Py, Go, Nd, Ts), nome, stack em `caption` e um ponto neon no canto quando aprovado. Variantes: foco (borda neon com brilho), inferido (pontilhado), sem acesso (tracejado, com o texto "sem acesso de leitura"), fora do foco (opacidade de 40%).
- **Grupo de subdomínio:** caixa com o ponto da cor do subdomínio, o nome em `display` e a contagem de sistemas.
- **Rótulo de integração:** pílula com o contrato (`POST /authorize`, `PaymentAuthorized`) e borda na cor do tipo. Integrações agregadas mostram quantidade e tipo ("3 integrações, arquivo").
- **Estrela (Mundo e Grafo):** esfera com gradiente radial na cor do subdomínio. O tamanho é proporcional ao número de integrações. A estrela selecionada fica neon, com um anel.
- **Marcador de passo de fluxo:** círculo numerado. O passo atual é neon e brilha; os feitos ficam contornados; os próximos ficam apagados.
- **Caixa de conflito ou pergunta:** usa `conflict-box`, com título, explicação e ações.
- **Chip de anexo:** *badge* do tipo (PDF, DOCX, PNG, ADR), nome, metadado e remover; borda neon quando o arquivo já foi processado.
- **Linha do bastão (pacote de contexto):** linha vertical neon até a camada atual e cinza depois dela. Os pontos são neon cheio (feito), anel neon (atual) ou cinza (aguardando).
- **Terminal (CLI):** o mesmo esquema de cores. `+` e "Pronto" em neon, `~` e `!` em âmbar, nomes de arquivos exportados em cobalto.

## Do's and Don'ts

- **Fazer:** reservar o neon para o que está vivo; manter as cores de subdomínio iguais nas três visões; mostrar a fonte de todo item; esmaecer o que está fora do foco em vez de esconder.
- **Fazer:** mostrar o inferido como partículas e o aprovado como sólido. Essa é a assinatura visual do produto.
- **Não fazer:** fundos pretos puros, gradientes decorativos, rótulos em caixa-alta, cartões todos iguais com a mesma sombra, emojis na interface.
- **Não fazer:** usar o neon em mais de uma ação primária por área, nem como cor de texto longo.
- **Não fazer:** animações de entrada em cada seção. O único movimento autônomo é a rotação lenta do Mundo, e ela para com "reduzir movimento" do sistema operacional.
