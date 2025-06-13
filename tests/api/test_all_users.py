from http import HTTPStatus

import allure
import pytest

from microservice.models.User import UserData
from tests.api.user_api_client import UsersApiClient

@pytest.fixture
def users(users_api_client: UsersApiClient) -> dict[int, UserData]:
    """
        Фикстура для получения всех пользователей через API клиента.

        Выполняет запрос к ручке получения всех пользователей с помощью UsersApiClient,
        валидирует статус-код ответа и возвращает словарь, в котором ключ — id пользователя,
        а значение — объект пользователя в виде dict.

        Returns:
            dict[int, UserData]: Маппинг user_id -> user (dict с данными пользователя),
                                 полученный из ответа API.
        """
    with allure.step("GET /api/users/"):
        response = users_api_client.get_all_users()
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        return {user['id']: user for user in data.get("items", [])}

@pytest.mark.usefixtures("fill_test_data")
@allure.title("Проверка получения всех пользователей")
def test_get_all_users(users_api_client: UsersApiClient) -> None:
    with allure.step("GET /api/users/"):
        response = users_api_client.get_all_users()
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert isinstance(data, dict)
        for user in data.get("items"):
            UserData.model_validate(user)

@pytest.mark.usefixtures("fill_test_data")
@allure.title("Проверка отсутствия дубликата существующих пользователей")
def test_users_no_duplicates(users) -> None:
    with allure.step("GET /api/users/"):
        users_ids = set(users.keys())
        assert len(users_ids) == len(users), "Дубликаты пользователей найдены"