from typing import Any, Generator

import pytest
from http import HTTPStatus

from microservice.models.User import UserCreate
from tests.api.user_api_client import UsersApiClient

@pytest.fixture
def user_payload() -> dict[str, str]:
    """
        Фикстура для формирования данных пользователя.
        """
    return {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "avatar": "https://example.com/avatar.jpg"
    }

@pytest.fixture
def created_user_parametrized(users_api_client: UsersApiClient, request) -> Generator[Any, Any, None]:
    """
    Фикстура для создания пользователя.
    Принимает данные пользователя через request.param (для параметризации).
    После теста удаляет созданного пользователя.
    """
    payload = request.param
    response = users_api_client.create_user(payload)
    assert response.status_code == HTTPStatus.CREATED, response.text
    user = response.json()
    UserCreate.model_validate(user)
    yield user
    users_api_client.delete_user(user["id"])

@pytest.fixture
def created_user(users_api_client: UsersApiClient, user_payload) -> Generator[Any, Any, None]:
    """
    Фикстура для создания пользователя без параметризации.
    Создаёт пользователя с фиксированными данными, возвращает его.
    После теста удаляет созданного пользователя.
    """
    response = users_api_client.create_user(user_payload)
    assert response.status_code == HTTPStatus.CREATED, response.text
    user = response.json()
    UserCreate.model_validate(user)
    yield user
    users_api_client.delete_user(user["id"])