from pydantic import BaseModel
from datetime import date
from typing import Optional


class CreateBook(BaseModel):
    title: str
    description: str
    publish_date: date
    author_id: int

    class ConfigDict:
        from_attributes = True


class CreateAuthor(BaseModel):
    name: str
    bio: str
    birth_date: date

    class ConfigDict:
        from_attributes = True


class UpdateAuthor(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[date] = None

    class ConfigDict:
        from_attributes = True


class UpdateBook(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    publish_date: Optional[date] = None

    class ConfigDict:
        from_attributes = True
