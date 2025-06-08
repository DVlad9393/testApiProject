import httpx
from http import HTTPStatus
import allure

@allure.title("Проверка удаления пользователя (DELETE)")
def test_delete_user(base_url: str):
    payload = {
        "email": "deletetest@example.com",
        "first_name": "Delete",
        "last_name": "Tester",
        "avatar": "https://example.com/delete-avatar.jpg"
    }
    response = httpx.post(f"{base_url}/api/users/", json=payload)
    assert response.status_code == HTTPStatus.CREATED, response.text
    user = response.json()
    user_id = user['id']

    with allure.step(f"DELETE /api/users/{user_id}"):
        response = httpx.delete(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK, response.text

    with allure.step(f"GET /api/users/{user_id}"):
        response = httpx.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND