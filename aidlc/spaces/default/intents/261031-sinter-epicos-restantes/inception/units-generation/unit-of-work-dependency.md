# Dependências das unidades

## Sources

`unit-of-work.md`, `units-generation-questions.md`, epics.md e ARCHITECTURE-SPINE.md referenciados no inventário de unidades.

## DAG

Uma aresta significa que código ou teste de uma unidade consome a capacidade da dependência. A execução é serial por solicitação da pessoa, mesmo onde não há aresta. A ordem econômica pertence a Delivery Planning.

```yaml
units:
  - name: u1-get-niveis
    kind: service
    depends_on: []
  - name: u2-calculados
    kind: service
    depends_on: [u1-get-niveis]
  - name: u3-jornadas
    kind: service
    depends_on: [u1-get-niveis, u2-calculados]
  - name: u4-read
    kind: service
    depends_on: []
  - name: u5-find-areas
    kind: service
    depends_on: [u1-get-niveis]
  - name: u6-avaliacao-ia
    kind: spec
    depends_on: [u2-calculados, u3-jornadas, u4-read, u5-find-areas]
  - name: u7-catalog-init
    kind: service
    depends_on: []
  - name: u8-apply-dry-run
    kind: service
    depends_on: [u13-fmt]
  - name: u9-apply
    kind: service
    depends_on: [u8-apply-dry-run, u13-fmt]
  - name: u10-new-domain
    kind: service
    depends_on: [u7-catalog-init, u9-apply]
  - name: u11-new-subdomain-journey
    kind: service
    depends_on: [u10-new-domain, u9-apply]
  - name: u12-get-raw
    kind: service
    depends_on: [u1-get-niveis, u9-apply]
  - name: u13-fmt
    kind: service
    depends_on: []
  - name: u14-sinter-find
    kind: spec
    depends_on: [u3-jornadas, u4-read, u5-find-areas]
  - name: u15-entrevista
    kind: spec
    depends_on: [u5-find-areas, u10-new-domain, u11-new-subdomain-journey, u12-get-raw]
  - name: u16-skill-criar
    kind: spec
    depends_on: [u15-entrevista, u8-apply-dry-run, u9-apply, u10-new-domain]
  - name: u17-skill-estruturar
    kind: spec
    depends_on: [u16-skill-criar, u11-new-subdomain-journey, u12-get-raw]
  - name: u18-skills-install
    kind: service
    depends_on: [u14-sinter-find, u17-skill-estruturar]
```

## Integrações

U1–U5 compartilham Level0/Level1/Level2 e serviços de texto. U8/U9 consomem o formatador U13, codec e catálogo imutável do Epic 1. U10/U11/U12 integram autoria e apply; seus testes de integração precisam de U9. U14–U17 consomem somente comandos CLI estruturados; U18 empacota as duas skills após suas extensões. U6 mede fatos das consultas completas.

## Independência técnica

U1, U4, U7 e U13 podem ser construídas isoladamente sobre a base atual. U14 e U15 podem coexistir depois das respectivas dependências, mas a execução continua serial. Não há inferência de autorização de paralelismo.

## Primeiro incremento integrado

U1 exercita CLI, caso de uso, portas e catálogo real sem depender de capacidade futura. Caminho funcional: get dom-pagv --level 1 --json, com herança e contratos de saída testados. O plano base não adiciona infraestrutura ou novo bootstrap.

