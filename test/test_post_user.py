import copy
from http import HTTPStatus

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


class TestCreationUser:
    def test_successful_creation(self, app_url):
        response_post = requests.post(f"{app_url}/api/users", json=user_payload)
        assert response_post.status_code == HTTPStatus.CREATED
        user = User.model_validate(response_post.json())
        response_get = requests.get(f"{app_url}/api/users/{user.id}")
        assert response_post.status_code == HTTPStatus.OK
        get_user = User.model_validate(response_get.json())
        assert user.id == get_user.id

    def test_invalid_email(self, app_url):
        copy_data = copy.deepcopy(user_payload)
        copy_data["email"] = "email"
        response_post = requests.post(f"{app_url}/api/users", json=copy_data)
        assert response_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_invalid_avatar(self, app_url):
        copy_data = copy.deepcopy(user_payload)
        copy_data["avatar"] = "avatar"
        response_post = requests.post(f"{app_url}/api/users", json=copy_data)
        assert response_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_invalid_first_name(self, app_url):
        copy_data = copy.deepcopy(user_payload)
        copy_data["first_name"] = 12345
        response_post = requests.post(f"{app_url}/api/users", json=copy_data)
        assert response_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_without_last_name(self, app_url):
        copy_data = copy.deepcopy(user_payload)
        copy_data.pop("last_name")
        response_post = requests.post(f"{app_url}/api/users", json=copy_data)
        assert response_post.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
