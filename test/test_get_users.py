from http import HTTPStatus

import pytest
import requests

from app.models.User import ListUserPaginationModel


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK
    return ListUserPaginationModel.model_validate(response.json())

class TestGetUsers:


    def test_users(self, app_url) -> None:
        response = requests.get(f"{app_url}/api/users")
        assert response.status_code == HTTPStatus.OK
        users_data = ListUserPaginationModel.model_validate(response.json())

        assert isinstance(users_data.items, list)
        assert len(users_data.items) > 0


    def test_users_no_duplicates(self, users) -> None:
        users_ids = [user.id for user in users.items]
        assert len(users_ids) == len(set(users_ids))


    @pytest.mark.parametrize("size", [2, 4, 7])
    def test_pagination_size(self, app_url, size: int) -> None:
        response = requests.get(f"{app_url}/api/users?size={size}")
        assert response.status_code == HTTPStatus.OK

        data = ListUserPaginationModel.model_validate(response.json())
        assert len(data.items) == size


    @pytest.mark.parametrize("size", [1, 2, 3])
    def test_pagination_total_pages(self, app_url, users: ListUserPaginationModel, size: int) -> None:
        response = requests.get(f"{app_url}/api/users?size={size}")
        assert response.status_code == HTTPStatus.OK

        data = ListUserPaginationModel.model_validate(response.json())
        expected_pages = (users.total + size - 1) // size
        assert data.pages == expected_pages


    @pytest.mark.parametrize("page_one, page_two", [(1, 2)])
    @pytest.mark.parametrize("size", [5])
    def test_pagination_different_pages(self, app_url: str, page_one: int, page_two: int, size: int) -> None:

        response_page_1 = requests.get(f"{app_url}/api/users?page={page_one}&size={size}")
        response_page_2 = requests.get(f"{app_url}/api/users?page={page_two}&size={size}")

        assert response_page_1.status_code == HTTPStatus.OK
        assert response_page_2.status_code == HTTPStatus.OK

        data_page_1 = ListUserPaginationModel.model_validate(response_page_1.json())
        data_page_2 = ListUserPaginationModel.model_validate(response_page_2.json())

        ids_page_1 = {user.id for user in data_page_1.items}
        ids_page_2 = {user.id for user in data_page_2.items}

        assert ids_page_1, "Список пользователей на странице 1 пуст!"
        assert ids_page_2, "Список пользователей на странице 2 пуст!"
        assert ids_page_1.isdisjoint(ids_page_2), "Данные на страницах не должны пересекаться!"

        assert len(data_page_1.items) == size, f"Ожидалось {size} объектов на странице 1, получено {len(data_page_1.items)}"
        assert len(data_page_2.items) <= size, f"Ожидалось не более {size} объектов на странице 2, получено {len(data_page_2.items)}"


    @pytest.mark.parametrize("page, size", [(1, 2), (1, 5), (2, 3)])
    def test_pagination_correct_pages(self, app_url: str, page: int, size: int) -> None:
        response = requests.get(f"{app_url}/api/users?page={page}&size={size}")
        assert response.status_code == HTTPStatus.OK

        data = ListUserPaginationModel.model_validate(response.json())
        expected_pages = (data.total + size - 1) // size
        assert data.pages == expected_pages, f"Ожидалось {expected_pages} страниц, получено {data.pages}"


    @pytest.mark.parametrize("size", [3, 5, 10])
    def test_pagination_response_fields(self, app_url: str, size: int) -> None:
        response = requests.get(f"{app_url}/api/users?size={size}")
        assert response.status_code == HTTPStatus.OK

        data = ListUserPaginationModel.model_validate(response.json())
        assert isinstance(data.page, int)
        assert isinstance(data.size, int)
        assert isinstance(data.total, int)
        assert isinstance(data.pages, int)
        assert isinstance(data.items, list)
