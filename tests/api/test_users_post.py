import httpx
import allure
from pydantic import BaseModel

class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

@allure.title("Проверка создания нового пользователя")
def test_create_user(base_url):
    payload = {
        "id": 999,
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "avatar": "https://example.com/avatar.jpg"
    }
    with allure.step("POST /api/users/"):
        response = httpx.post(f"{base_url}/api/users/", json=payload)
        assert response.status_code == 200, response.text
        user_data = UserData(**response.json())
        assert user_data.email == "test@example.com"