import httpx
import pytest
from http import HTTPStatus
import allure

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
def test_405_method_not_allowed(base_url, method, url):
    req = getattr(httpx, method)
    resp = req(f"{base_url}{url}")
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED

@allure.title("404 и 422 ошибки на PATCH и DELETE по некорректным и несуществующим id")
@pytest.mark.parametrize("user_id", [-1, 0, 999999])
def test_delete_patch_not_found_or_unprocessable(base_url, user_id):
    if user_id < 1:
        resp = httpx.patch(f"{base_url}/api/users/{user_id}", json=BASE_PAYLOAD)
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        resp = httpx.delete(f"{base_url}/api/users/{user_id}")
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        resp = httpx.patch(f"{base_url}/api/users/{user_id}", json=BASE_PAYLOAD)
        assert resp.status_code == HTTPStatus.NOT_FOUND
        resp = httpx.delete(f"{base_url}/api/users/{user_id}")
        assert resp.status_code == HTTPStatus.NOT_FOUND

@allure.title("404 Not Found на удалённого пользователя")
def test_404_on_deleted_user(base_url):
    resp = httpx.post(f"{base_url}/api/users/", json=BASE_PAYLOAD)
    assert resp.status_code == HTTPStatus.CREATED
    user_id = resp.json()["id"]
    resp = httpx.delete(f"{base_url}/api/users/{user_id}")
    assert resp.status_code == HTTPStatus.OK
    resp = httpx.get(f"{base_url}/api/users/{user_id}")
    assert resp.status_code == HTTPStatus.NOT_FOUND