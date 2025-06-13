import pytest
from http import HTTPStatus
import allure

from tests.api.user_api_client import UsersApiClient

BASE_PAYLOAD = {
    "email": "valid@example.com",
    "first_name": "Valid",
    "last_name": "Tester",
    "avatar": "https://example.com/avatar.jpg"
}

@allure.title("405 Method Not Allowed на запрещённые эндпоинты")
@pytest.mark.parametrize("method,url", [
    ("put", "/api/users/"),
    ("delete", "/api/users/"),
    ("patch", "/api/users/"),
    ("post", "/api/users/1"),
])
def test_405_method_not_allowed(users_api_client: UsersApiClient, method, url):
    resp = users_api_client.request_custom(method, url, json=BASE_PAYLOAD)
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED

@allure.title("404 и 422 ошибки на PATCH и DELETE по некорректным и несуществующим id")
@pytest.mark.parametrize("user_id", [-1, 0, 999999])
def test_delete_patch_not_found_or_unprocessable(users_api_client: UsersApiClient, user_id):
    if user_id < 1:
        resp = users_api_client.update_user(user_id, BASE_PAYLOAD)
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        resp = users_api_client.delete_user(user_id)
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        resp = users_api_client.update_user(user_id, BASE_PAYLOAD)
        assert resp.status_code == HTTPStatus.NOT_FOUND
        resp = users_api_client.delete_user(user_id)
        assert resp.status_code == HTTPStatus.NOT_FOUND

@allure.title("404 Not Found на удалённого пользователя")
def test_404_on_deleted_user(users_api_client: UsersApiClient):
    resp = users_api_client.create_user(BASE_PAYLOAD)
    assert resp.status_code == HTTPStatus.CREATED
    user_id = resp.json()["id"]
    resp = users_api_client.delete_user(user_id)
    assert resp.status_code == HTTPStatus.OK
    resp = users_api_client.get_user(user_id)
    assert resp.status_code == HTTPStatus.NOT_FOUND