from http import HTTPStatus
import allure

from tests.user_api_client import UsersApiClient

BASE_PAYLOAD = {
    "email": "valid@example.com",
    "first_name": "Valid",
    "last_name": "Tester",
    "avatar": "https://example.com/avatar.jpg"
}

@allure.title("Пользовательский флоу: создать, прочитать, обновить, удалить")
def test_user_flow_crud(users_api_client: UsersApiClient):
    resp = users_api_client.create_user(BASE_PAYLOAD)
    assert resp.status_code == HTTPStatus.CREATED
    user = resp.json()
    user_id = user["id"]
    resp = users_api_client.get_user(user_id)
    assert resp.status_code == HTTPStatus.OK
    update = dict(BASE_PAYLOAD, first_name="Updated")
    resp = users_api_client.update_user(user_id, update)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["first_name"] == "Updated"
    resp = users_api_client.delete_user(user_id)
    assert resp.status_code == HTTPStatus.OK