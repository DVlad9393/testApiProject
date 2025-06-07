from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from typing import Dict

from microservice.models import UserData, UserResponse, AppStatus
from microservice.db import users_db, support_info

router = APIRouter()

users: Dict[int, UserData] = {}

@router.get("/status", response_model=AppStatus, status_code=HTTPStatus.OK,
            description="Проверка доступности сервиса. Возвращает статус сервиса и наличие пользователей.")
def status() -> AppStatus:
    """
        Проверить доступность сервиса.

        **Параметры запроса:**
        — отсутствуют

        **Возвращает:**
        - Объект AppStatus, содержащий флаг users (True, если есть хотя бы один пользователь; иначе False).

        **Ошибки:**
        — Не возвращает ошибок.
        """
    return AppStatus(users=bool(users))

@router.get("/api/users/{user_id}", response_model=UserResponse, status_code=HTTPStatus.OK,
            description="Получение пользователя по его уникальному идентификатору.")
def get_user(user_id: int) -> UserResponse:
    """
        Получить информацию о пользователе по ID.

        **Параметры запроса:**
        - user_id (int, path) — уникальный идентификатор пользователя

        **Возвращает:**
        - Объект UserResponse, включающий данные пользователя (UserData) и support-информацию (SupportData).

        **Ошибки:**
        - 404, если пользователь не найден.
        """
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(data=user, support=support_info)

@router.post("/api/users/", response_model=UserData, status_code=HTTPStatus.OK,
             description="Создать нового пользователя. Если пользователь с таким ID уже существует — будет ошибка.")
def create_user(user: UserData) -> UserData:
    """
        Создать нового пользователя.

        **Параметры запроса:**
        - user (UserData, body) — JSON-объект пользователя с полями id, email, first_name, last_name, avatar

        **Возвращает:**
        - Объект UserData с данными созданного пользователя.

        **Ошибки:**
        - 400, если пользователь с таким id уже существует.
        """
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user
    return user

@router.get("/api/users/", response_model=Page[UserData], status_code=HTTPStatus.OK,
            description="Получение всех пользователей с поддержкой пагинации (параметры page и size).")
def get_all_users() -> Page:
    """
        Получить список всех пользователей с пагинацией.

        **Параметры запроса:**
        - page (int, query, необязательно, по умолчанию 1) — номер страницы
        - size (int, query, необязательно, по умолчанию 50) — количество элементов на странице

        **Возвращает:**
        - Объект Page[UserData] со списком пользователей (`items`), количеством элементов (`total`),
        страниц (`pages`), текущей страницей (`page`) и размером страницы (`size`).

        **Ошибки:**
        — Не возвращает ошибок.
        """
    return paginate(list(users_db.values()))