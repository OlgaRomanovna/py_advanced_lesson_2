from http import HTTPStatus

import pytest
import requests
from app.models.User import User


class TestGetUserById:

    def test_user(self, app_url):
        response_users = requests.get(f"{app_url}/api/users")
        user = User.model_validate(response_users.json())
        response = requests.get(f"{app_url}/api/users/{user.id}")
        assert response.status_code == HTTPStatus.OK

        User.model_validate(response.json())

    @pytest.mark.parametrize("user_id", [35])
    def test_user_nonexistent_values(self, app_url, user_id):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
    def test_user_invalid_values(self, app_url, user_id):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("user_id", [35])
    def test_method_not_allowed(self, app_url, user_id):
        response = requests.post(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
