
from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UsersResponse(BaseModel):
    page: int
    size: int
    total: int
    pages: int
    items: list[User]
