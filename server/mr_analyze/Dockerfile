FROM python:3.12.1

RUN pip install --no-cache-dir poetry

WORKDIR /app
COPY server/pyproject.toml ./ 
COPY server/poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY server ./

COPY server/.env .env

CMD ["python", "-m", "src.composites.app"]
