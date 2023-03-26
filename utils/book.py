from enum import Enum
from typing import Dict

from pydantic import BaseModel


class BookTextKeyEnum(str, Enum):
    chapter = ("chapter",)
    page = "page"


class Book(BaseModel):
    title: str
    author: str
    key: BookTextKeyEnum
    text: Dict[str, str]
