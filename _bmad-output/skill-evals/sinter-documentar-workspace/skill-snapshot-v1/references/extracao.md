# Onde procurar cada coisa

Tudo o que for lido literalmente é `extracted`. O que for deduzido é `inferred`.

## Infraestrutura (camada 6)

| Fonte | O que extrair |
|---|---|
| Terraform (`*.tf`) | `aws_lambda_function`, `aws_sqs_queue`, `aws_sns_topic`, `aws_dynamodb_table`, `aws_db_instance`, `aws_s3_bucket`, `aws_api_gateway*`, `aws_msk_cluster`, equivalentes GCP/Azure; variáveis por ambiente (`*.tfvars`, workspaces) |
| AWS SAM / CloudFormation (`template.yaml`, `*.cfn.*`) | `Resources` com tipos `AWS::Serverless::Function`, `AWS::SQS::Queue` etc.; `Events` das funções = gatilhos |
| Serverless Framework (`serverless.yml`) | `functions` (cada uma é um componente), `events` (gatilhos), `resources`, `provider.environment` (nomes, nunca valores secretos) |
| AWS CDK (`cdk.json`, `lib/*.ts`) | construções `new lambda.Function`, `new sqs.Queue`… |
| Kubernetes (`*.yaml`, Helm `values.yaml`) | `Deployment`, `Service`, `Ingress`, `CronJob`, `ConfigMap` (nomes), réplicas e recursos |
| Docker Compose (`docker-compose.yml`) | serviços, bancos e filas locais que revelam dependências |

## Componentes e sistemas (camadas 4 e 5)

| Fonte | O que extrair |
|---|---|
| Manifestos (`package.json`, `pom.xml`, `build.gradle`, `go.mod`, `pyproject.toml`, `*.csproj`) | stack, frameworks, clientes de fila e banco |
| Entradas (handlers de lambda, `main`, controllers, rotas) | endpoints expostos, gatilhos |
| OpenAPI / Swagger | contratos de API (cite o arquivo) |
| AsyncAPI, schemas Avro/Protobuf/JSON Schema | contratos de eventos |
| Clientes HTTP e SDKs (URLs base, `@FeignClient`, `axios.create`, `requests`) | quem chama quem |
| Produtores e consumidores (`publish`, `send`, `@KafkaListener`, `consumer.subscribe`, `sqs.receiveMessage`) | eventos e filas |
| Migrações (`db/migration`, `migrations/`, `schema.prisma`, entidades ORM) | modelo de dados |
| Enums e máquinas de estado (`status`, `state`) | estados das entidades |
| Configuração de resiliência (timeouts, retries, circuit breakers) | regras e requisitos de qualidade |

## Documentos (camadas 1, 2 e transversal)

| Fonte | O que extrair |
|---|---|
| `README.md`, `docs/`, wikis exportadas | propósito, dono, fluxos descritos, glossário |
| ADRs (`docs/adr`, `decisions/`) | decisões |
| `CODEOWNERS` | donos |
| Guias de contribuição e lint | padrões |

## Segredos

Se encontrar chaves, tokens, senhas ou strings de conexão com credencial: **não copie o valor**. Registre no `RELATORIO.md` só o arquivo, a linha e o tipo, para alguém tratar.

## Quando não há evidência

Se a ligação entre dois sistemas não aparece no código (ex.: chamada por URL montada em tempo de execução), registre como `inferred`, explique o indício e inclua uma pergunta no relatório.
