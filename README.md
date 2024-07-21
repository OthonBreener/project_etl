## Dependências obrigatórias

* Python 3.11.2
* Docker (27.0.3) e Docker Compose (v2.11.2)
* Git
* Poetry
* Pyenv (Opcional)


## Recursos utilizados

- fastapi: framework web
- sqlalchemy: ORM (Object Relational Mapper)
- alembic: ferramenta de migração de banco de dados
- ruff: linter e formatador de código
- taskipy: task runner (executor de comandos)
- pytest: test runner

## Como executar com o Docker Compose

Na raiz do projeto, execute o seguinte comando:
```bash
docker-compose up --build
```

Esse comando vai criar os containers dos bancos de dados e da aplicação. Popular
o banco de dados fonte com dados aleatórios, por padrão de 2024-01-01 até 2024-01-10,
e executar o pipeline para 2024-01-01.

Caso queira executar para outras datas, siga os passos:

* Primeiro, execute o seguinte comando na raiz do projeto:
```bash
docker exec -it project_etl-project_api-1 /bin/bash
```

* Dentro do container docker, execute:

```bash
python -i project/pipeline.py
```

* Por fim, dentro do terminal interativo do python, execute:

```python
from datetime import datetime

Pepiline(datetime(2024, 1, 2)).run()
```

Obs: altere a data que deseja executar o pipeline.

## Como executar o programa

1. Instale as dependências do projeto:
```bash
poetry env use 3.11.2
poetry install
```

2. Ative o ambiente virtual:
```bash
poetry shell
```

3. Execute o seguinte comando para criar os containers dos bancos de dados:
```bash
task init_db
```

4. Com os containers criados, rode os seguintes comandos para criar as tabelas:
```bash
task create_db_fonte
task create_db_alvo
```

4. Agora crie os dados fakes no banco de dados alvo:
```bash
python -i project/generate_datas.py

# dentro do terminal python

generate_datas()
```