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