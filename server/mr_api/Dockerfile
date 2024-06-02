FROM python:3.12.1

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY server/mr_api/pyproject.toml ./ 

COPY server/mr_api/poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY server/mr_api ./

COPY server/mr_api/.env .env

CMD ["python", "-m", "src.composites.app"]
