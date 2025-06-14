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
   2. Запустить сервер в контейнере (предварительно установить docker):
       ```
      Запуск docker compose
      docker compose up -d (без сборки)
      docker compose up --build

      Отключение docker compose
      docker compose down
    ```

## Эндпоинты

- `GET /api/users/{user_id}` — получить пользователя по id.
- `POST /api/users/` — создать пользователя.
- `GET /api/users/` — получить всех пользователей.
- `PUT /api/users/{user_id}` — обновить пользователя по id.
- `DELETE /api/users/{user_id}` — удалить пользователя по id.
- `GET /api/status/` — получить статус сервера.

## Структура проекта

- `microservice` — FastAPI приложение.
- `microservice/database` — модуль для работы с базой данных.
- `microservice/models` — модели данных.
- `microservice/routers` — маршруты API.
- `tests` — тесты.
Проверить, что сервер запущен можно по адресу http://localhost:8002/docs.

Запуск тестов

poetry run pytest --alluredir=allure-results

Запуск тестов снаружи (вне контейнера) с удалением предыдущих результатов (по умолчанию)
cp .env.local .env
rm -rf allure-results && poetry run pytest -s --alluredir=allure-results

Запуск тестов снаружи (вне контейнера) с сохранением предыдущих результатов через переменную окружения dev
rm -rf allure-results && poetry run pytest --env=dev -s --alluredir=allure-results

Адреса GitHub Pages с результатами тестов:
- dev https://dvlad9393.github.io/testApiProject/dev/
- stage https://dvlad9393.github.io/testApiProject/stage/
- prod https://dvlad9393.github.io/testApiProject/prod/