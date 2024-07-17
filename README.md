## Dependências obrigatórias

* Python 3.11.* (ou superior)
* Docker (27.0.3) e Docker Compose (v2.11.2)
* Git

## Recursos utilizados

- fastapi: framework web
- sqlalchemy: ORM (Object Relational Mapper)
- ruff: linter e formatador de código
- taskipy: task runner (executor de comandos)
- pytest: test runner
- poetry: gerenciador de dependências

Para criar o banco de dados: docker exec -it postgres_fonte psql -U user1 -d postgres -c "CREATE DATABASE postgres_fonte;"
