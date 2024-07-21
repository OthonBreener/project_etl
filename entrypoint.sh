#!/bin/sh

# Executa as migrações do banco de dados
cd project/orm_fonte && poetry run alembic upgrade head
cd ../orm_alvo && poetry run alembic upgrade head
cd /app

# Inicia a aplicação (em background)
poetry run uvicorn --host 0.0.0.0 --port 8000 project.api:app & APP_PID=$!

# Garente que a aplicação esteja pronta para receber requisições
sleep 10

# Cria os dados fakes no banco de dados alvo e executa o pipeline (depende da aplicação estar rodando)
poetry run python -m project.main

# Para a aplicação (em background)
kill $APP_PID

# Executa novamente a aplicação (em foreground)
poetry run uvicorn --host 0.0.0.0 --port 8000 project.api:app