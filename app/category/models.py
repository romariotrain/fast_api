from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.article.models import article_category
from app.database import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    articles = relationship('Article', secondary='article_category', back_populates='categories')