from http import HTTPStatus

import httpx
import allure
import pytest

from microservice.models.User import UserData

@pytest.fixture
def users(base_url: str) -> dict[int, UserData]:
    with allure.step("GET /api/users/"):
        response = httpx.get(f"{base_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        return response.json()

@pytest.mark.usefixtures("fill_test_data")
@allure.title("Проверка получения всех пользователей")
def test_get_all_users(base_url: str) -> None:
    with allure.step("GET /api/users/"):
        response = httpx.get(f"{base_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert isinstance(data, dict)
        for user in data.get("items"):
            UserData.model_validate(user)

@pytest.mark.usefixtures("fill_test_data")
@allure.title("Проверка отсутствия дубликата существующих пользователей")
def test_users_no_duplicates(users) -> None:
    with allure.step("GET /api/users/"):
        users_ids = set(users.keys())
        assert len(users_ids) == len(users), "Дубликаты пользователей найдены"