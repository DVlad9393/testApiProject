FROM python:3.13

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./microservice /code/microservice

CMD ["poetry", "run", "uvicorn", "microservice.main:app", "--host", "0.0.0.0", "--port", "80"]