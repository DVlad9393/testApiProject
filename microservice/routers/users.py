from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from microservice.database import users
from microservice.database.users import get_user_from_db_by_id, get_users_from_db, get_user_from_db_by_email
from microservice.models.User import UserCreate, UserData, UserUpdate

router = APIRouter(prefix="/api/users")

@router.get("/{user_id}", response_model=UserData, status_code=HTTPStatus.OK,
            description="Получение пользователя по его уникальному идентификатору.")
def get_user(user_id: int) -> dict[str, Any]:
    """
        Получить информацию о пользователе по ID.

        **Параметры запроса:**
        - user_id (int) — уникальный идентификатор пользователя

        **Возвращает:**
        - словарь с информацией о пользователе из базы данных.

        **Ошибки:**
        - 404, если пользователь не найден.
    """
    user = get_user_from_db_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.model_dump()

@router.get("/", response_model=Page[UserData], status_code=HTTPStatus.OK,
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
    disable_installed_extensions_check()
    return paginate(list(get_users_from_db()))

@router.post("/", response_model=UserData, status_code=HTTPStatus.CREATED,
             description="Создать нового пользователя. Если пользователь с таким ID уже существует — будет ошибка.")
def create_user(new_user: UserCreate) -> UserData:
    """
        Создать нового пользователя.

        Args:
            new_user (UserCreate): Объект пользователя, содержащий необходимые данные для создания.

        Returns:
            UserData: Созданный пользователь с присвоенным идентификатором.

        Raises:
            HTTPException: 400, если пользователь с таким ID уже существует.
            HTTPException: 422, если переданы некорректные данные.

        Примечания:
            - Если пользователь с указанным ID уже существует, возвращается ошибка 400.
        """
    UserCreate.model_validate(new_user.model_dump())
    existing_user = get_user_from_db_by_email(new_user.email)
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    return users.create_user(new_user)


@router.patch("/{user_id}", response_model=UserData, status_code=HTTPStatus.OK,
            description="Обновить данные пользователя по его уникальному идентификатору.")
def update_user(user_id: int, user: UserUpdate) -> type[UserData]:
    """
        Обновить данные пользователя.

        Args:
            user_id (int): Уникальный идентификатор пользователя.
            user (UserData): Объект пользователя с обновленными данными.

        Returns:
            UserData: Обновлённый пользователь.

        Raises:
            HTTPException: 422, если передан некорректный идентификатор пользователя.
            HTTPException: 404, если пользователь не найден.

        Примечания:
            - Все поля, переданные в запросе, заменяют текущие значения пользователя.
        """
    if user_id < 1:
        raise HTTPException (status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)

@router.delete("/{user_id}", status_code=HTTPStatus.OK,
            description="Удалить пользователя по его уникальному идентификатору.")
def delete_user(user_id: int) -> dict[str, str]:
    """
        Удалить пользователя.

        Args:
            user_id (int): Уникальный идентификатор пользователя.

        Returns:
            dict[str, str]: Сообщение о результате удаления, например {"message": "User deleted"}.

        Raises:
            HTTPException: 422, если передан некорректный идентификатор пользователя.
            HTTPException: 404, если пользователь не найден.

        Примечания:
            - Пользователь будет удалён, если существует. Если не найден — ошибка 404.
        """
    if user_id < 1:
        raise HTTPException (status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user")
    users.delete_user(user_id)
    return {"message": "User deleted"}