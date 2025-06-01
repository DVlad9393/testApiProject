# FastAPI User Microservice

Микросервис для управления пользователями на FastAPI.

## Запуск

1. Установить зависимости:
    ```
    pip install poetry
    poetry lock (если проблемы с актуальностью в папке poetry.lock)
    poetry install
    poetry env activate (для активации виртуального окружения)
    ```
2. Запустить сервер:
    ```
    poetry run uvicorn microservice.main:app --reload
    ```

## Эндпоинты

- `GET /api/users/{user_id}` — получить пользователя по id.
- `POST /api/users/` — создать пользователя.
- `GET /api/users/` — получить всех пользователей.

## Структура проекта

- `main.py` — основной файл проекта.
- `models.py` — модели данных.
- `schemas.py` — схемы данных.
- `utils.py` — утилиты.
- `db.py` — база данных.
- 
Проверить, что сервер запущен можно по адресу http://localhost:8000/docs.

Запуск тестов

poetry run pytest --alluredir=allure-results

Запуск тестов с удалением предыдущих результатов
rm -rf allure-results && poetry run pytest -s --alluredir=allure-results