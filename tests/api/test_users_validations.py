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

@allure.title("Проверка валидации полей (email, avatar) при создании пользователя")
@pytest.mark.parametrize("payload,field", [
    (dict(BASE_PAYLOAD, email="invalidemail"), "email"),
    (dict(BASE_PAYLOAD, avatar="not-a-url"), "avatar"),
    (dict(BASE_PAYLOAD, email=""), "email"),
])
def test_invalid_fields_on_create(base_url, payload, field):
    resp = httpx.post(f"{base_url}/api/users/", json=payload)
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert field in resp.text

@allure.title("Создание пользователя без обязательного поля (email)")
def test_create_missing_required_field(base_url):
    bad_payload = dict(BASE_PAYLOAD)
    del bad_payload["email"]
    resp = httpx.post(f"{base_url}/api/users/", json=bad_payload)
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "email" in resp.text