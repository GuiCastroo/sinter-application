# Documentação v3 — entender com menos leitura

Data: 2026-09-30. Avaliação solicitada por Gui sob três perspectivas: desenvolvimento (Amelia), produto (John) e arquitetura (Winston). Dois subagentes avaliaram desenvolvimento e produto; o coordenador assumiu arquitetura. O objeto são as três documentações da iteration-3, não a qualidade dos sistemas demonstrativos.

## Recomendação principal

Manter um conjunto único de informações e oferecer percursos curtos por papel. O contexto necessário já está majoritariamente presente. A próxima simplificação deve retirar reformulações, links genéricos repetidos e detalhes fora da perspectiva do leitor; deve preservar fronteiras, regras que mudam o resultado, relações, dados e consequências de falha.

Não confundir três objetivos: entender o sistema, planejar uma mudança e implementar sem consultar código. A documentação deve atender bem os dois primeiros e orientar a consulta ao código no terceiro. Copiar todas as classes, payloads e testes para a documentação aumenta manutenção e não substitui a fonte executável.

## Cortes concretos

| Ação | O que mudar | O que precisa sobreviver |
|---|---|---|
| Remover | “Em uma frase” quando repete “Em resumo”, nos três Negócios | Propósito, público e fronteira no resumo inicial |
| Resumir | “Por que existe” | Declarar que é demonstração e o que ela demonstra; retirar classificação core/genérico quando é só conjectura sem uso decisório |
| Unificar | Dúvidas e perguntas / Dúvidas de contexto / Perguntas para decisão | Um registro com pergunta, impacto, evidência e papel responsável; conflitos conhecidos não são perguntas |
| Remover | Blocos que apenas repetem “consulte Referência” após cada jornada | Um acesso geral e links locais para regras específicas relevantes |
| Unificar | Decisões em Arquitetura e Referência | Decisão + consequência na Arquitetura; fontes e indicação de inferência preservadas |
| Mover | Relação de tecnologias ausentes, detalhes de handlers e inventários opcionais fora de contexto | Uma frase sobre o estilo de integração; detalhes técnicos sob consulta em Serviços/Infraestrutura |
| Mover | Histórico editorial “Evidências da revisão v3” | Registro da revisão separado; referências factuais continuam junto às afirmações que sustentam |
| Manter | Sequências dos fluxos complexos, dados, interfaces e efeitos de falha | Não substituir uma sequência temporal por um mapa de dependências |

**Um corte que precisa de ajuste:** na v3, “Regras que mandam” passou a apontar genericamente para Referência. Manter duas ou três regras/consequências essenciais em linguagem de negócio torna essa página compreensível sozinha; a definição completa continua canônica na Referência. Redução de repetição não significa proibir sínteses locais úteis.

## Percursos de leitura, sem criar três cópias da documentação

| Papel | Começar por | Consultar depois | Pode deixar para uma tarefa específica |
|---|---|---|---|
| PM | Resumo, fronteira, atores e jornada principal em Negócio | Regras essenciais, consequências de falha e decisões de produto pendentes | Métodos, portas, classes, recursos e comandos de implantação |
| Dev | Resumo do sistema e serviço que vai mudar | Contrato/dados/falhas, jornada afetada e Como começar | Catálogo completo dos outros serviços e extensões não usadas |
| Arquiteto | Fronteira, contexto, responsabilidades e mapa | Jornada principal, propriedade dos dados, decisões e riscos | Detalhamento dos handlers e comandos cotidianos |

Esses percursos cabem em três grupos de links no índice atual. Não é necessário criar páginas novas por papel ou fundir páginas que respondem perguntas diferentes.

## Acréscimos pequenos que compensam a leitura

- **Dev:** um caminho de execução/teste de uma mudança representativa, com pré-requisitos, comando e resultado esperado. Referenciar o teste real; não copiar uma suíte inteira.
- **PM:** distinguir comportamento de demonstração, hipótese e regra confirmada. Não criar metas, roadmap ou papéis que não existem nas fontes.
- **Arquiteto:** explicitar o escopo do mapa e quais relações ele omite; separar dependência, sequência de execução e inicialização. Um exemplo de contrato crítico quando os campos relevantes não estão localizáveis basta.

## Cuidados por domínio

- **Boutique:** manter visível que pagamento, frete e email são simulados. “Cliente foi cobrado” precisa dessa qualificação; compensação é relevante se a integração virar real. Preservar a ordem checkout → pagamento → envio.
- **Serverlesspresso:** preservar a diferença entre limite de capacidade no ASL e configuração não usada, os dois momentos de espera e o vínculo por token. Não resumir como “nada síncrono”: há acessos diretos a dados e callbacks. Código inativo e extensões não devem dominar a primeira leitura.
- **PetClinic:** preservar dono/pet/visita, ausência de validação cruzada de petId e fallback que exibe visitas vazias. Explicar o gateway na entrada do chat e a chamada direta do genai para customers. Não prometer topologia de produção nem capacidade da memória que não foram confirmadas.

## Critério de aceite de uma próxima simplificação

O leitor deve conseguir dizer: para quem serve, o que faz e não faz, qual fluxo importa, quem guarda os dados, quais componentes participam, como uma falha aparece ao usuário e onde confirmar uma regra ou executar uma alteração. Cortar conteúdo somente quando essas respostas continuam acessíveis sem adivinhação.

As recomendações deste relatório não foram aplicadas aos documentos. A v3 continua disponível em [index.html](../index.html); a análise individual traz evidências e tarefas por papel.

## Relatórios individuais

- [Amelia — desenvolvimento](amelia-dev.md)
- [John — produto](john-pm.md)
- [Winston — arquitetura](winston-arquitetura.md)
