import json
from http import HTTPStatus


import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from models.AppStatus import AppStatus
from models.User import User
from utils.generate_users import generate_users

app = FastAPI()
add_pagination(app)


# Загрузка пользователей из файла
def load_users_from_file(filename: str) -> list[User]:
    with open(filename, 'r') as file:
        users_data = json.load(file)
        return [User(**user) for user in users_data]


# Чтение пользователей при запуске
users = load_users_from_file('users.json')


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/api/user/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.get("/api/users", response_model=Page[User])
def get_users() -> Page[User]:
    if not users:
        raise HTTPException(status_code=404, detail="No found users")
    return paginate(users)


if __name__ == "__main__":
    generate_users(20)
    uvicorn.run(app, host="localhost", port=8002)
