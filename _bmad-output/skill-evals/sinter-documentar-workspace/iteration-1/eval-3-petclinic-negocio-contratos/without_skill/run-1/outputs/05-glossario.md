# Glossário do Domínio — Clínica Veterinária

| Termo | Definição no contexto deste sistema | Onde vive |
|---|---|---|
| **Owner (Tutor)** | Pessoa dona de um ou mais pets, cadastrada com nome, endereço, cidade e telefone | `customers-service` |
| **Pet** | Animal de estimação vinculado a exatamente um Owner e a exatamente um PetType | `customers-service` |
| **PetType** | Categoria/espécie do pet (ex.: cat, dog, lizard, snake, bird, hamster) | `customers-service` |
| **Vet (Veterinário)** | Profissional do corpo clínico da clínica, com nome e zero ou mais Specialties | `vets-service` |
| **Specialty (Especialidade)** | Área de atuação de um veterinário (ex.: radiology, surgery, dentistry) | `vets-service` |
| **Visit (Visita)** | Registro de um atendimento realizado a um Pet, com data e descrição textual | `visits-service` |
| **Owner Details** | Visão agregada de um tutor + seus pets + as visitas de cada pet, montada pelo api-gateway a partir de dois serviços | `api-gateway` (BFF) |
| **Chat / Assistente da clínica** | Ponto de entrada conversacional que interpreta perguntas/comandos em linguagem natural e aciona tools de negócio | `genai-service` |
| **Tool (ferramenta de IA)** | Função exposta ao modelo de linguagem para consultar ou alterar dados reais do domínio (listar tutores/vets, cadastrar tutor/pet) | `genai-service` |
| **Vector store** | Índice de embeddings dos veterinários usado para busca semântica (RAG) nas perguntas sobre corpo clínico | `genai-service` |
| **Circuit Breaker** | Mecanismo de resiliência que interrompe chamadas a um serviço instável e retorna uma resposta alternativa (fallback) | `api-gateway` (rotas + BFF) |
| **Service Discovery / Eureka** | Registro dinâmico de instâncias de serviço, usado para resolver nomes lógicos (`customers-service`, `vets-service`, etc.) em endereços reais | `discovery-server`, consumido por todos |
| **Config Server** | Fonte centralizada de configuração (`application.yml` remoto) consumida por todos os serviços na subida | `config-server` |

## Convenções observadas no código

- Nomes de serviço usados no service discovery são sempre em kebab-case e coincidem com `spring.application.name` de cada módulo (`customers-service`, `vets-service`, `visits-service`, `genai-service`, `api-gateway`, `discovery-server`, `admin-server`).
- IDs de entidades são sempre inteiros autoincrementais (`Integer id`, `GenerationType.IDENTITY`), nunca UUID, em todos os serviços de negócio.
- Datas de nascimento/visita trafegam no formato `yyyy-MM-dd` nos contratos JSON, mesmo quando armazenadas internamente como `Date`/`Timestamp`.
