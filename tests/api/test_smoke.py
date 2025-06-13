from http import HTTPStatus

import allure
import pytest
from tests.api.user_api_client import UsersApiClient

@pytest.mark.smoke
@allure.title("Проверка доступности сервиса")
def test_smoke_service_availability(users_api_client: UsersApiClient) -> None:
    with allure.step("GET /status"):
        response = users_api_client.get_status()
        assert response is not None
        assert response.status_code == HTTPStatus.OK

@pytest.mark.smoke
@allure.title("Smoke: Список пользователей доступен")
def test_smoke_get_users_availability(users_api_client: UsersApiClient) -> None:
    with allure.step("GET /api/users/"):
        response = users_api_client.get_all_users()
        assert response.status_code == HTTPStatus.OK

@pytest.mark.smoke
@allure.title("Smoke: Создание пользователя")
def test_smoke_create_user_availability(users_api_client: UsersApiClient) -> None:
    payload = {
        "email": "smoke@example.com",
        "first_name": "Smoke",
        "last_name": "Test",
        "avatar": "https://example.com/avatar.jpg"
    }
    with allure.step("POST /api/users/"):
        response = users_api_client.create_user(payload)
        assert response.status_code == HTTPStatus.CREATED

@pytest.mark.smoke
@allure.title("Smoke: Получение пользователя по id")
def test_smoke_get_new_user_by_id_availability(users_api_client: UsersApiClient) -> None:
    payload = {
        "email": "getid@example.com",
        "first_name": "SmokeGet",
        "last_name": "Test",
        "avatar": "https://example.com/avatar2.jpg"
    }
    response = users_api_client.create_user(payload)
    response_json = response.json()
    user_id = response_json['id']
    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.OK