from http import HTTPStatus
import allure
from tests.api.user_api_client import UsersApiClient
from tests.test_fixtures import created_user

@allure.title("Проверка удаления пользователя (DELETE)")
def test_delete_user(users_api_client: UsersApiClient, created_user):
    user_id = created_user['id']
    with allure.step(f"DELETE /api/users/{user_id}"):
        response = users_api_client.delete_user(user_id)
        assert response.status_code == HTTPStatus.OK, response.text

    with allure.step(f"GET /api/users/{user_id}"):
        response = users_api_client.get_user(user_id)
        assert response.status_code == HTTPStatus.NOT_FOUND