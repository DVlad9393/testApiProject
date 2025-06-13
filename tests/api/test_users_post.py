from http import HTTPStatus

import allure

from microservice.models.User import UserData
from tests.api.user_api_client import UsersApiClient


@allure.title("Проверка создания нового пользователя")
def test_create_user(users_api_client: UsersApiClient) -> None:
    payload = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "avatar": "https://example.com/avatar.jpg"
    }
    with allure.step("POST /api/users/"):
        response = users_api_client.create_user(payload)
        assert response.status_code == HTTPStatus.CREATED, response.text
        user = response.json()
        UserData.model_validate(user)
        user_data = UserData(**response.json())
        assert user_data.email == "test@example.com"
        user_id = user['id']
        with allure.step(f"GET /api/users/{user_id}"):
            response = users_api_client.get_user(user_id)
            assert response.status_code == HTTPStatus.OK