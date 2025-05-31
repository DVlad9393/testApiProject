import httpx
import allure

@allure.title("Проверка получения всех пользователей")
def test_get_all_users(base_url: str) -> None:
    with allure.step("GET /api/users/"):
        response = httpx.get(f"{base_url}/api/users/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, dict)
        assert all("id" in user for user in data.values())