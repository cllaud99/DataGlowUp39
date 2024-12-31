# Use a Python runtime as a base image
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copie o restante do código para o diretório de trabalho
COPY . /app

# Comandos a serem executados ao iniciar o contêiner
CMD ["task", "run"]