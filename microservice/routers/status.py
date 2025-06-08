from http import HTTPStatus

from fastapi import APIRouter

from microservice.database.engine import check_availability_db
from microservice.models.AppStatus import AppStatus

router = APIRouter()

# users: Dict[int, UserData] = {}

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

    return AppStatus(database=bool(check_availability_db()))