FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 project.api:app