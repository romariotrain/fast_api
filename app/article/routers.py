from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional

from app.article.models import Article
from app.article.schema import ArticleCreate, ArticleInDb
from app.category.models import Category
from app.database import get_db
from fastapi_pagination import Page, paginate


router = APIRouter()


@router.post("/articles/", response_model=ArticleInDb)
async def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_categories = db.query(Category).filter(Category.id.in_(article.categories)).all()
    if len(db_categories) != len(article.categories):
        raise HTTPException(status_code=400, detail="One or more categories not found")
    new_article = Article(
        title=article.title,
        content=article.content,
        published_at=article.published_at or datetime.utcnow(),
        categories=db_categories
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@router.get("/articles/", response_model=Page[ArticleInDb])
async def get_articles(category_id: Optional[int] = Query(None),
                       search: Optional[str] = Query(None, max_length=50),
                       db: Session = Depends(get_db)):

    if search:
        results = db.query(Article).filter(
            or_(
                Article.content.ilike(f'%{search}%'),
                Article.title.ilike(f'%{search}%')
            )
        )
    else:
        results = db.query(Article)

    if category_id:
        results = results.join(Article.categories).filter(Category.id == category_id)
    return paginate(results.all())
