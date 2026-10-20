# Documentação Sinter v3

Abra [a entrada dos três domínios](index.html). Cada domínio mantém seis páginas Markdown como fonte: Negócio, Arquitetura, Serviços, Jornadas, Infraestrutura e Referência. Cartão, resumos, grafo e site são projeções reproduzíveis dessas páginas.

Regras e glossário foram consolidados na Referência, com registros Rxx e perguntas Qxx completas. As páginas de contexto conservam sínteses e links. Infraestrutura mantém seu inventário canônico. A v2 e as fixtures foram preservadas.

As correções comprovadas incluem a validade de cartão no mês atual e o consumo real do catálogo na Boutique; cinco tabelas, três máquinas e acesso administrativo ao QR code no café; ordem dono→visitas, caminho do chat pelo gateway e capacidade de memória não comprovada na PetClinic. A Referência de cada domínio registra evidências e questões restantes.

Os serviços declaram ID e estado ativo/opcional/inativo. Cada linha de Consome declara um tipo controlado (`chama_api`, `consome_evento`, `acessa_dado`, `callback`, `inicializacao`, `configuracao`); cada jornada declara seus participantes. O grafo usa somente essas declarações, sem associar serviços por menção no texto. As arestas representam dependências do consumidor para o fornecedor, não a cronologia do fluxo. Relações não comprovadas mantêm a indicação “a confirmar”.

O site preserva parede e temas. A árvore usa IDs com contexto de página/serviço; links Markdown navegam internamente. O marcador `<!-- MAPA-PRINCIPAL -->` da Arquitetura recebe um único mapa de dependências gerado das mesmas relações do grafo. Outros diagramas têm perspectivas distintas (contexto, sequência, infraestrutura).

## Reprodução

Requer Python 3.10 ou posterior; os geradores não usam rede nem bibliotecas externas. A partir desta pasta:

```sh
python3 ferramentas/gerar_tudo.py
python3 ferramentas/verificar.py
```

Para um domínio isolado:

```sh
python3 ferramentas/gerar_llm.py CAMINHO_DO_DOMINIO --nome "Nome"
python3 ferramentas/gerar_site.py CAMINHO_DO_DOMINIO --nome "Nome"
```

[verificacao.json](verificacao.json) registra links, participantes, tipos, IDs, hashes dos originais, snapshots das fixtures e igualdade das saídas em duas gerações. [baseline-v2.json](ferramentas/baseline-v2.json) guarda os 279 hashes anteriores às edições. Os geradores locais são candidatos à revisão; a skill instalada e o PRD não foram alterados.

## Limites

A verificação factual é amostral sobre as fixtures locais; não certifica toda a documentação herdada. Não foram executadas aplicações nem publicadas mudanças. Dúvidas de negócio e configurações externas continuam explícitas. O cartão é um índice curto e preserva as perguntas inteiras; os resumos explicam serviços e jornadas.

O HTML abre sem servidor, mas depende dos CDNs Marked e Mermaid; não é um pacote offline. A busca filtra títulos da árvore. A verificação Python é estática; o smoke de navegador, quando presente, é registrado separadamente.
