#!/bin/sh

# Executa as migrações do banco de dados
cd project/orm_fonte && poetry run alembic upgrade head
cd ../orm_alvo && poetry run alembic upgrade head
cd /app

# Cria os dados fakes no banco de dados alvo
poetry run python -m project.main

# Inicia a aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 project.api:app