Aqui está o README adaptado para a sua aplicação FastAPI com PostgreSQL:

---

# Todo List API

Este repositório contém a **Todo List API**, uma aplicação de gerenciamento de tarefas desenvolvida em **FastAPI** com um banco de dados **PostgreSQL**. A API inclui autenticação com JWT, rotas para criar, atualizar, listar e excluir usuários e tarefas.


## Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/): Framework web para construção de APIs em Python.
- [PostgreSQL](https://www.postgresql.org/): Sistema de gerenciamento de banco de dados relacional.
- [Docker Compose](https://docs.docker.com/compose/): Ferramenta para definir e gerenciar multi-containers Docker para a aplicação.

## Instruções para Rodar a Aplicação

### Pré-requisitos

- **Docker** e **Docker Compose** instalados na máquina.

### Passo a Passo

1. **Configurar Variáveis de Ambiente**

   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

   ```plaintext
   POSTGRES_USER="user"
   POSTGRES_PASSWORD="user"
   POSTGRES_DB="todo_db"
   DATABASE_URL="postgresql://user:user@postgres:5432/todo_db"
   SECRET_KEY="your-secret-key-here"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

2. **Iniciar a Aplicação**

   Com as variáveis de ambiente configuradas, execute o comando abaixo para inicializar a aplicação e o banco de dados PostgreSQL:

   ```bash
   docker-compose up -d
   ```

3. **Executar Migrações**

   As migrações do banco de dados são aplicadas automaticamente ao iniciar o Docker Compose. Caso queira realizar alguma alteração nas migrações, use o comando:

   ```bash
   docker-compose exec api alembic upgrade head
   ```

4. **Acessar a Documentação da API**

   Com a aplicação em execução, acesse a documentação interativa da API através do Swagger no endereço [http://localhost:8000/docs](http://localhost:8000/docs).

5. **Parar a Aplicação**

   Para interromper e remover os contêineres Docker, utilize:

   ```bash
   docker-compose down
   ```

