from pydantic import BaseModel

from typing import List, Generic, TypeVar

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
