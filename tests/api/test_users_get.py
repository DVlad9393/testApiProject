import httpx
import allure
from pydantic import BaseModel

class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class UserResponse(BaseModel):
    data: UserData
    support: dict

@allure.title("Проверка получения пользователя по id")
def test_get_user(base_url):
    user_id = 1
    with allure.step(f"GET /api/users/{user_id}"):
        response = httpx.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == 200, response.text
        user_resp = UserResponse(**response.json())
        assert user_resp.data.id == user_id