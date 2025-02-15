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


class TestUpdatedUser:
    def test_successful_update(self, app_url, create_user):
        updated_first_name = {
            "first_name": "Hulio"
        }
        response_patch = requests.patch(f"{app_url}/api/users/{create_user}", json=updated_first_name)
        assert response_patch.status_code == HTTPStatus.OK
        user = User.model_validate(response_patch.json())
        response_get = requests.get(f"{app_url}/api/users/{user.id}")
        user_get = User.model_validate(response_get.json())
        assert user_get.first_name == "Hulio"

    def test_invalid_email(self, app_url):
        updated_email = {
            "email": "email"
        }
        user_id = create_user(app_url)
        response_patch = requests.patch(f"{app_url}/api/users/{user_id}", json=updated_email)
        assert response_patch.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_invalid_avatar(self, app_url):
        updated_avatar = {
            "avatar": "avatar"
        }
        user_id = create_user(app_url)
        response_patch = requests.patch(f"{app_url}/api/users/{user_id}", json=updated_avatar)
        assert response_patch.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
    def test_invalid_user_id(self, app_url, user_id):
        response_patch = requests.patch(f"{app_url}/api/users/{user_id}")
        assert response_patch.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

