from http import HTTPStatus

import pytest
import requests
from models.User import User


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/user/{user_id}")
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("user_id", [35])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/user/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/user/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
