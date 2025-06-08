from http import HTTPStatus

import httpx
import allure
import pytest

@pytest.mark.smoke
@allure.title("Проверка доступности сервиса")
def test_smoke_service_availability(base_url: str) -> None:
    with allure.step("GET /status"):
        response = httpx.get(f"{base_url}/status")
        assert response is not None
        assert response.status_code == HTTPStatus.OK

@pytest.mark.smoke
@allure.title("Smoke: Список пользователей доступен")
def test_smoke_get_users_availability(base_url: str) -> None:
    with allure.step("GET /api/users/"):
        response = httpx.get(f"{base_url}/api/users/")
        assert response.status_code == HTTPStatus.OK

@pytest.mark.smoke
@allure.title("Smoke: Создание пользователя")
def test_smoke_create_user_availability(base_url: str) -> None:
    payload = {
        "email": "smoke@example.com",
        "first_name": "Smoke",
        "last_name": "Test",
        "avatar": "https://example.com/avatar.jpg"
    }
    with allure.step("POST /api/users/"):
        response = httpx.post(f"{base_url}/api/users/", json=payload)
        assert response.status_code == HTTPStatus.CREATED

@pytest.mark.smoke
@allure.title("Smoke: Получение пользователя по id")
def test_smoke_get_new_user_by_id_availability(base_url: str) -> None:
    payload = {
        "email": "getid@example.com",
        "first_name": "SmokeGet",
        "last_name": "Test",
        "avatar": "https://example.com/avatar2.jpg"
    }
    response = httpx.post(f"{base_url}/api/users/", json=payload)
    response_json = response.json()
    user_id = response_json['id']
    with allure.step(f"GET /api/users/{user_id}"):
        response = httpx.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK