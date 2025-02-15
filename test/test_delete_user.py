from http import HTTPStatus

import pytest
import requests
from faker import Faker

from app.models.User import User

fake = Faker()

user_payload = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "avatar": fake.image_url()
}

@pytest.fixture(scope="function")
def create_user(app_url):
    response_post = requests.post(f"{app_url}/api/users", json=user_payload)
    user = User.model_validate(response_post.json())
    return user.id


class TestDeletionUser:

    def test_successful_removal(self, app_url, create_user):
        response_delete = requests.delete(f"{app_url}/api/users/{create_user}")
        assert response_delete.status_code == HTTPStatus.OK
        response_get = requests.get(f"{app_url}/api/users/{create_user}")
        assert response_get.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
    def test_invalid_user_id(self, app_url, user_id):
        response_delete = requests.delete(f"{app_url}/api/users/{user_id}")
        assert response_delete.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_double_removal(self, app_url):
        user_id = create_user(app_url)
        response_delete = requests.delete(f"{app_url}/api/users/{user_id}")
        assert response_delete.status_code == HTTPStatus.OK
        response_delete_2 = requests.delete(f"{app_url}/api/users/{user_id}")
        assert response_delete_2.status_code == HTTPStatus.NOT_FOUND

