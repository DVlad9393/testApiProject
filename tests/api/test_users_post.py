from http import HTTPStatus

import allure

from microservice.models.User import UserData
from tests.api.user_api_client import UsersApiClient
from tests.test_fixtures import user_payload

@allure.title("Проверка создания нового пользователя")
def test_create_user(users_api_client: UsersApiClient, user_payload) -> None:
    with allure.step("POST /api/users/"):
        response = users_api_client.create_user(user_payload)
        assert response.status_code == HTTPStatus.CREATED, response.text

        user = response.json()
        UserData.model_validate(user)
        user_data = UserData(**response.json())
        assert user_data.email == "test@example.com"

    user_id = user['id']
    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.OK, response.text

        user_fetched = response.json()
        UserData.model_validate(user_fetched)
        assert user_fetched["id"] == user_id
        assert user_fetched["email"] == user_payload["email"]
        assert user_fetched["first_name"] == user_payload["first_name"]
        assert user_fetched["last_name"] == user_payload["last_name"]
        assert user_fetched["avatar"] == user_payload["avatar"]