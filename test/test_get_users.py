from http import HTTPStatus

import pytest
import requests

from models.User import User


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    return response.json()


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK

    userss = response.json()["items"]
    for user in userss:
        User.model_validate(user)


def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


def test_pagination_size(app_url):
    size = 5
    response = requests.get(f"{app_url}/api/users?size={size}")

    assert response.status_code == 200
    assert "items" in response.json()
    assert len(response.json()["items"]) == size, f"Ожидалось {size} объектов, получено {len(response.json()['items'])}"


def test_pagination_total_pages(app_url, users):
    size = 10
    response = requests.get(f"{app_url}/api/users?size={size}")

    assert response.status_code == 200
    total_pages = (len(users["items"]) + size - 1) // size
    assert response.json()["pages"] == total_pages, f"Ожидалось {total_pages} страниц, получено {response.json()['pages']}"


def test_pagination_different_pages(app_url):
    page_size = 5

    response_page_1 = requests.get(f"{app_url}/api/users?page=1&size={page_size}")
    assert response_page_1.status_code == 200

    response_page_2 = requests.get(f"{app_url}/api/users?page=2&size={page_size}")
    assert response_page_2.status_code == 200

    data_page_1 = response_page_1.json()["items"]
    data_page_2 = response_page_2.json()["items"]

    assert data_page_1 != data_page_2, "Данные на страницах должны быть разными"
    assert len(data_page_1) == page_size, f"Ожидалось {page_size} объектов на странице 1, получено {len(data_page_1)}"
    if len(data_page_2) > 0:
        assert len (data_page_2) <= page_size, f"Ожидалось не более {page_size} объектов на странице 2, получено {len(data_page_2)}"