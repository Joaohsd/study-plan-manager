# Study Plan Manager

Uma aplicação para gerenciar planos de estudo, permitindo gerar planos através de inteligencia artificial, atualizar e monitorar metas e tarefas relacionadas.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **FastAPI**: Framework para criação da API.
- **PostgreSQL**: Banco de dados utilizado para armazenar os planos e tarefas.
- **asyncpg**: Biblioteca para interação assíncrona com PostgreSQL.
- **Google Generative AI**: Integração com a API Gemini para geração de planos de estudo personalizados.
- **Pydantic**: Validação de dados das requisições e modelos.
- **Flask e HTML**: Interface

---


## Funcionalidades (UI)

1. **Adicionar Planos de Estudo**: Crie planos com metas, prazos e horas diárias de estudo.
2. **Visualizar Planos**: Listagem de todos os planos criados.
3. **Excluir Planos**: Remoção de planos indesejados.
4. **Gerenciar Tarefas**: Visualizar, atualizar, excluir ou alternar o status de conclusão de tarefas associadas a um plano.
5. **Progresso Automático**: Calcula automaticamente o progresso de um plano com base no número de tarefas concluídas.
6. **Resetar Banco de Dados**: Remove todos os planos e tarefas.

## Funcionalidades (API)

### Planos de Estudo
- **Criar**: Adicionar novos planos de estudo com metas, prazos e horas diárias dedicadas.
- **Listar**: Recuperar todos os planos cadastrados ou um plano específico por ID.
- **Atualizar**: Alterar dados de um plano existente, como meta, prazo e progresso.
- **Excluir**: Remover um plano específico ou resetar todos os planos.

### Tarefas
- **Gerar**: Criar automaticamente tarefas com base nas metas do plano, utilizando a API Gemini.
- **Adicionar**: Inserir tarefas individuais a um plano específico.
- **Listar**: Recuperar todas as tarefas de um plano.
- **Atualizar**: Modificar detalhes de uma tarefa existente, como descrição, semana ou status de conclusão.
- **Excluir**: Remover uma tarefa específica.

---

## Configuração

### Requisitos
- Python 3.10+
- Docker e Docker Compose
- [Conta e chave de API para Google Generative AI](https://aistudio.google.com/apikey)

### Instalação
1. Clone o repositório:
   ```bash
   git clone git@github.com:Joaohsd/study-plan-manager.git
   cd study-plan-api
   ```

2. Configure as variáveis de ambiente:
   - `GOOGLE_API_KEY`: Chave da API do Google Generative AI.

3. Execução:
   ```bash
   docker compose up --build
   ```


---

## Endpoints

### Planos
- **POST `/api/v1/plans/`**: Criar um novo plano.
- **GET `/api/v1/plans/`**: Listar todos os planos.
- **GET `/api/v1/plans/{id}`**: Obter detalhes de um plano específico.
- **PATCH `/api/v1/plans/{id}`**: Atualizar um plano.
- **DELETE `/api/v1/plans/{id}`**: Remover um plano específico.

### Tarefas
- **POST `/api/v1/plans/{plan_id}/tasks/`**: Adicionar uma tarefa a um plano.
- **GET `/api/v1/plans/{plan_id}/tasks/`**: Listar todas as tarefas de um plano.
- **PATCH `/api/v1/plans/{plan_id}/tasks/{task_id}`**: Atualizar uma tarefa.
- **DELETE `/api/v1/plans/{plan_id}/tasks/{task_id}`**: Remover uma tarefa específica.

---

## Autores

| <img src="https://media.licdn.com/dms/image/v2/D4D03AQFll5Z9bN7-1g/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1732624923561?e=1738800000&v=beta&t=U0Fzd3A5C74jjb6vhrd4sCdaV7_xfoUiCR18ISL8ZXU" alt="Paulo" width="150" height="150"> | <img src="https://avatars.githubusercontent.com/u/66541032?v=4" alt="Joao" width="150" height="150"> |
|:------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------:|
| **Nome:** Paulo Henrique Lopes Júnior                                                                            | **Nome:** João Henrique Silva Delfino                                                                           |
| **Matrícula:** 1748                                                                       | **Matrícula:** ???                                                                       |
| **E-mail:** [paulo.ph@gec.inatel](mailto:paulo.ph@gec.inatel)                                | **E-mail:** [joao.h@gec.inatel.br](mailto:joao.h@gec.inatel.br)                                |
| **LinkedIn:** [Paulo Lopes](https://www.linkedin.com/in/paulolopestech/)                                | **LinkedIn:** [João Delfino](https://www.linkedin.com/in/joao-delfino/)                                |
