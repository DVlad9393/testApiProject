# FastAPI User Microservice

Микросервис для управления пользователями на FastAPI.

## Запуск

1. Установить зависимости:
    ```
    pip install -r requirements.txt
    ```
2. Запустить сервер:
    ```
    uvicorn microservice.main:app --reload
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

pytest --alluredir=allure-results