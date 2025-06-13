from http import HTTPStatus
import allure
from tests.api.user_api_client import UsersApiClient

@allure.title("Проверка удаления пользователя (DELETE)")
def test_delete_user(users_api_client: UsersApiClient):
    payload = {
        "email": "deletetest@example.com",
        "first_name": "Delete",
        "last_name": "Tester",
        "avatar": "https://example.com/delete-avatar.jpg"
    }
    response = users_api_client.create_user(payload)
    assert response.status_code == HTTPStatus.CREATED, response.text
    user = response.json()
    user_id = user['id']

    with allure.step(f"DELETE /api/users/{user_id}"):
        response = users_api_client.delete_user(user_id)
        assert response.status_code == HTTPStatus.OK, response.text

    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.NOT_FOUND