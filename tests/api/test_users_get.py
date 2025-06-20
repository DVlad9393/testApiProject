from http import HTTPStatus

import allure
import pytest

from microservice.models.User import UserData
from tests.user_api_client import UsersApiClient


@pytest.mark.usefixtures("fill_test_data")
@pytest.mark.parametrize("user_id", [1, 2])
@allure.title("Проверка получения пользователя по id")
def test_get_user(users_api_client: UsersApiClient, user_id: int) -> None:
    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        UserData.model_validate(user)
        assert user["id"] == user_id

@pytest.mark.usefixtures("fill_test_data")
@pytest.mark.parametrize("user_id", [35,-1,517,0])
@allure.title("Проверка получения пользователя по несуществующему id")
def test_get_nonexistent_user(users_api_client: UsersApiClient, user_id: int) -> None:
    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.usefixtures("fill_test_data")
@pytest.mark.parametrize("user_id", ['dhfghf',3.14,True])
@allure.title("Проверка получения пользователя по невалидному типу данных id")
def test_get_invalid_id_user(users_api_client: UsersApiClient, user_id: int) -> None:
    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY