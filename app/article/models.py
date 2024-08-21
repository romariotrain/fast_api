from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

article_category = Table('article_category', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    published_at = Column(DateTime)
    categories = relationship('Category', secondary='article_category', back_populates='articles')

