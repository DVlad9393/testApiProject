from http import HTTPStatus

from tests.utils import get_total_pages
import httpx
import allure
import pytest
import math

@pytest.mark.usefixtures("fill_test_data")
@pytest.mark.parametrize("size", [1, 3, 7, 10, 20])
@allure.title("Проверка количества объектов на странице при size={size}")
def test_pagination_total_count(base_url: str, size: int, total_users):
    page = get_total_pages(size)
    total_pages = math.ceil(total_users / size)
    response = httpx.get(f"{base_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()

    start = (page - 1) * size
    end = min(page * size, total_users)
    expected_items = end - start

    assert isinstance(data['items'], list)
    assert data['total'] == total_users
    assert data['page'] == page
    assert data['size'] == size
    assert data['pages'] == total_pages
    assert len(data['items']) == expected_items

@pytest.mark.usefixtures("fill_test_data")
@pytest.mark.parametrize("size", [5, 8, 3])
@allure.title("Проверка количества страниц в пагинации на каждой странице для size={size}")
def test_pagination_pages_count_all_pages(base_url: str, size: int, total_users: int):
    expected_pages = math.ceil(total_users / size)
    for page in range(1, expected_pages + 1):
        response = httpx.get(f"{base_url}/api/users/?page={page}&size={size}")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data['pages'] == expected_pages

@pytest.mark.usefixtures("fill_test_data")
@allure.title("Проверка возвращения  разных объектов на разных страницах")
def test_pagination_page_switch(base_url: str):
    response1 = httpx.get(f"{base_url}/api/users/?page=1&size=5")
    response2 = httpx.get(f"{base_url}/api/users/?page=2&size=5")
    assert response1.status_code == HTTPStatus.OK
    assert response2.status_code == HTTPStatus.OK
    items1 = response1.json()['items']
    items2 = response2.json()['items']
    assert items1 != items2
    ids1 = set(item['id'] for item in items1)
    ids2 = set(item['id'] for item in items2)
    assert ids1.isdisjoint(ids2)