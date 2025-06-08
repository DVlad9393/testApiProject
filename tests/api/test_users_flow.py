import httpx
from http import HTTPStatus
import allure

BASE_PAYLOAD = {
    "email": "valid@example.com",
    "first_name": "Valid",
    "last_name": "Tester",
    "avatar": "https://example.com/avatar.jpg"
}

@allure.title("Пользовательский флоу: создать, прочитать, обновить, удалить")
def test_user_flow_crud(base_url):
    resp = httpx.post(f"{base_url}/api/users/", json=BASE_PAYLOAD)
    assert resp.status_code == HTTPStatus.CREATED
    user = resp.json()
    user_id = user["id"]
    resp = httpx.get(f"{base_url}/api/users/{user_id}")
    assert resp.status_code == HTTPStatus.OK
    update = dict(BASE_PAYLOAD, first_name="Updated")
    resp = httpx.patch(f"{base_url}/api/users/{user_id}", json=update)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["first_name"] == "Updated"
    resp = httpx.delete(f"{base_url}/api/users/{user_id}")
    assert resp.status_code == HTTPStatus.OK