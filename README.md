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

## Como executar os testes

Para executar os testes você deve ter as dependências do projeto instaladas.
Para isso, siga os passos:

1. Defina a versão utilizada e crie a env (caso não tenho o python 3.11.2, recomendo o uso do pyenv):
```bash
poetry env use 3.11.2
```

2. Ative o ambiente virtual:
```bash
poetry shell
```

3. Instale as dependêcias:
```bash
poetry install
```

4. Na raiz do projeto, execute o seguinte comando:

```bash
task test
```

Esse comando irá rodar os testes e retornar o html do coverage no final.