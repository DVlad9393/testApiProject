from http import HTTPStatus

import httpx
import allure
import pytest

@allure.title("Проверка количества объектов на странице")
def test_pagination_total_count(base_url: str):
    response = httpx.get(f"{base_url}/api/users/?page=1&size=20")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['total'] == 20
    assert len(data['items']) == 20

@allure.title("Проверка подсчета pages при разных значениях size")
@pytest.mark.parametrize("size,expected_pages", [(5, 4),(8, 3),(3, 7),])
def test_pagination_pages_count(base_url: str, size: int, expected_pages: int):
    response = httpx.get(f"{base_url}/api/users/?page=1&size={size}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['pages'] == expected_pages

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