# Exemplo de catálogo — Sinter (passo 1: Domínio)

Dados fictícios. Um manifesto por arquivo, como no catálogo real. A pasta inteira é a referência do [PRD](../prd.md).

```text
exemplo-catalogo/
├── organization.yaml                  # áreas, domínios, vocabulário da empresa
├── repositories.yaml                  # id → endereço de cada repo de código
├── regulations/                       # regulações moram na raiz (valem para vários domínios)
│   └── reg-lgpd.yaml  reg-bcb-cambio.yaml  reg-pld.yaml  …
├── standards/                         # padrões corporativos
│   └── std-api-rest.yaml  std-eventos-kafka.yaml  …
└── domains/
    ├── pagv/                          # Pagamentos (Varejo) · id-domínio PAGV
    │   ├── domain.yaml                # propósito, faz/não faz/não sabemos, regras do domínio todo, modernização, conhecimento
    │   ├── subdomains/
    │   │   ├── sub-pagv-checkout.yaml       # moderno
    │   │   ├── sub-pagv-autorizacao.yaml    # moderno
    │   │   └── sub-pagv-conciliacao.yaml    # 2 aplicações: batch legado + serviço novo
    │   │       (as APLICAÇÕES ficam DENTRO do arquivo do subdomínio, cada uma com seus N repos)
    │   ├── journeys/
    │   │   ├── jor-pagv-pagar-pedido.yaml   # jornada moderna com falhas por passo
    │   │   └── jor-pagv-conciliar-dia.yaml  # jornada batch (agenda + jobs)
    │   ├── decisions/                 # ADRs (ADR-PAGV-001, -003, -004)
    │   ├── relations/
    │   │   └── rel-…--modernized_by--….yaml # o batch é substituído pelo microserviço
    │   └── docs/                      # os .md citados pelos campos docs: (o resto é link)
    │       ├── negocio/politica-estorno.md
    │       └── atas/ata-2026-10-03.md
    └── camb/                          # Câmbio · id-domínio CAMB (do Exemplo.drawio.xml)
        ├── domain.yaml                # propósito, 10 subdomínios, regulações (Bacen, PLD)
        ├── subdomains/                # uma "caixinha" do desenho = um subdomínio
        │   ├── sub-camb-cotacao.yaml  sub-camb-limite.yaml  sub-camb-dados-cliente.yaml
        │   ├── sub-camb-formalizacao.yaml  sub-camb-boletagem.yaml  sub-camb-enriquecimento.yaml
        │   └── sub-camb-validacao.yaml  sub-camb-carteira.yaml  sub-camb-liquidacao.yaml  sub-camb-pld.yaml
        ├── decisions/                 # ADRs do câmbio
        ├── journeys/
        │   └── jor-camb-enviar-moeda-pf.yaml  # jornada em etapas; cada passo abre um subdomínio
        └── relations/
            └── rel-…liquidacao-legado--modernized_by--….yaml  # LIQ0100 → serviço novo
```

## Por onde começar a ler

1. `domains/pagv/domain.yaml`: a visão geral do domínio.
2. `domains/pagv/subdomains/sub-pagv-conciliacao.yaml`: um subdomínio com legado.
3. `domains/pagv/journeys/jor-pagv-pagar-pedido.yaml`: o que acontece, passo a passo.
4. `domains/camb/journeys/jor-camb-enviar-moeda-pf.yaml`: jornada em etapas, cada passo é um subdomínio.

## Onde ficam os documentos

Todo nível tem um campo `docs:` — domínio, subdomínio, aplicação, **cada repo** da aplicação e jornada. Cada item aponta para um `.md` da pasta `docs/` do domínio (`path`) **ou** para um link (`url`: wiki, Confluence, arquivo dentro do repo), com `type`: `negocio`, `ata`, `pauta`, `runbook`, `arquitetura`, `gerado` ou `link`. Um doc já citado em outro nível é reaproveitado com `{ ref: <id> }`, sem repetir.

Regulações, padrões e decisões continuam sendo itens próprios (`regulations:`, `standards:`, `decisions:`), porque têm vida própria e valem para vários lugares.

## Regra de ouro

Cada fato é escrito em **um lugar só**. As **regras** são frases curtas e ficam dentro do domínio (as que valem para todos) ou do subdomínio (as daquela parte); a explicação longa vai para a página `.md` do nível. O subdomínio guarda as suas aplicações; cada aplicação diz se é legado e quais repos a compõem. Tudo o que junta isso (quantos legados há, quais repos o domínio tem, o que é herdado) é **calculado** pela CLI. A exceção é a lista `subdomains` do domínio: ela fica escrita como **sumário** para quem lê o arquivo, e o `validate` garante que bate com os subdomínios. Os comentários `$ sinter get …` dentro dos arquivos mostram o que a CLI devolveria.

O catálogo passa nas regras do PRD com **zero erros**. Os únicos avisos são os domínios vizinhos que não estão catalogados (`dom-risco`, `dom-contas`…), que o PRD trata como aviso e não como erro.
