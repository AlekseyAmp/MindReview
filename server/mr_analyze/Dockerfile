FROM python:3.12.1

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY server/mr_analyze/pyproject.toml ./ 

COPY server/mr_analyze/poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY server/mr_analyze ./

COPY server/mr_analyze/.env .env

CMD ["python", "-m", "src.composites.analyze"]
