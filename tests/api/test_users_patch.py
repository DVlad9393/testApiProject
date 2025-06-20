from http import HTTPStatus
import allure
import pytest

from microservice.models.User import UserUpdate, UserData
from tests.user_api_client import UsersApiClient
from tests.test_fixtures import created_user_parametrized

@pytest.mark.parametrize(
    "created_user_parametrized",
    [
        {
            "email": "patchtest1@example.com",
            "first_name": "Patch1",
            "last_name": "Tester1",
            "avatar": "https://example.com/patch1.jpg"
        },
        {
            "email": "patchtest2@example.com",
            "first_name": "Patch2",
            "last_name": "Tester2",
            "avatar": "https://example.com/patch2.jpg"
        },
    ],
    indirect=True
)
@allure.title("Проверка обновления данных пользователя (PATCH)")
def test_update_user(users_api_client: UsersApiClient, created_user_parametrized):
    user_id = created_user_parametrized['id']
    update_payload = {
        "email": created_user_parametrized["email"],
        "first_name": "Patched",
        "last_name": created_user_parametrized["last_name"],
        "avatar": "https://example.com/patched.jpg"
    }
    with allure.step(f"PATCH /api/users/{user_id}"):
        response = users_api_client.update_user(user_id, update_payload)
        assert response.status_code == HTTPStatus.OK, response.text
        updated_user = response.json()
        UserUpdate.model_validate(updated_user)
        assert updated_user["first_name"] == "Patched"
        assert updated_user["avatar"] == "https://example.com/patched.jpg"

    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        UserData.model_validate(user)
        assert user["first_name"] == "Patched"
        assert user["avatar"] == "https://example.com/patched.jpg"