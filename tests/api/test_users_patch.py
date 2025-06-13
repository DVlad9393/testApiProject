from http import HTTPStatus
import allure

from tests.api.user_api_client import UsersApiClient


@allure.title("Проверка обновления данных пользователя (PATCH)")
def test_update_user(users_api_client: UsersApiClient):
    payload = {
        "email": "patchtest@example.com",
        "first_name": "Patch",
        "last_name": "Tester",
        "avatar": "https://example.com/patch-avatar.jpg"
    }
    response = users_api_client.create_user(payload)
    assert response.status_code == HTTPStatus.CREATED, response.text
    user = response.json()
    user_id = user['id']

    update_payload = {
        "email": user["email"],
        "first_name": "Patched",
        "last_name": user["last_name"],
        "avatar": "https://example.com/patched.jpg"
    }
    with allure.step(f"PATCH /api/users/{user_id}"):
        response = users_api_client.update_user(user_id, update_payload)
        assert response.status_code == HTTPStatus.OK, response.text
        updated_user = response.json()
        assert updated_user["first_name"] == "Patched"
        assert updated_user["avatar"] == "https://example.com/patched.jpg"

    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        assert user["first_name"] == "Patched"
        assert user["avatar"] == "https://example.com/patched.jpg"