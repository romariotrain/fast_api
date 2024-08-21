from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.category.models import Category
from app.category.schema import CategoryInDb
from fastapi_filter.contrib.sqlalchemy import Filter


class ArticleBase(BaseModel):
    title: str
    content: str
    published_at: Optional[datetime] = None

class ArticleCreate(ArticleBase):
    categories: List[int]

class ArticleInDb(ArticleBase):
    id: int
    categories: List[CategoryInDb]

    class Config:
        orm_mode = True


class UserFilter(Filter):
    name: Optional[str]