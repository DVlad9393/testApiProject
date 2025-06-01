from http import HTTPStatus

import httpx
import allure
import pytest

from microservice.models import UserResponse

@pytest.mark.parametrize("user_id", [1, 2])
@allure.title("Проверка получения пользователя по id")
def test_get_user(base_url: str, user_id: int) -> None:
    with allure.step(f"GET /api/users/{user_id}"):
        response = httpx.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK, response.text
        user = response.json()
        UserResponse.model_validate(user)
        assert user["data"]["id"] == user_id

@pytest.mark.parametrize("user_id", [21,-1,517,0])
@allure.title("Проверка получения пользователя по несуществующему id")
def test_get_nonexistent_user(base_url: str, user_id: int) -> None:
    with allure.step(f"GET /api/users/{user_id}"):
        response = httpx.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND, response.text

@pytest.mark.parametrize("user_id", ['dhfghf',3.14,True])
@allure.title("Проверка получения пользователя по невалидному типу данных id")
def test_get_invalid_id_user(base_url: str, user_id: int) -> None:
    with allure.step(f"GET /api/users/{user_id}"):
        response = httpx.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text