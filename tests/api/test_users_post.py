from http import HTTPStatus

import httpx
import allure

from microservice.models.User import UserData

@allure.title("Проверка создания нового пользователя")
def test_create_user(base_url: str) -> None:
    payload = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "avatar": "https://example.com/avatar.jpg"
    }
    with allure.step("POST /api/users/"):
        response = httpx.post(f"{base_url}/api/users/", json=payload)
        assert response.status_code == HTTPStatus.CREATED, response.text
        user = response.json()
        UserData.model_validate(user)
        user_data = UserData(**response.json())
        assert user_data.email == "test@example.com"
        user_id = user['id']
        with allure.step(f"GET /api/users/{user_id}"):
            response = httpx.get(f"{base_url}/api/users/{user_id}")
            assert response.status_code == HTTPStatus.OK