from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.category.models import Category
from app.category.schema import CategoryCreate, CategoryInDb
from app.database import get_db

router = APIRouter()


@router.post("/categories/", response_model=CategoryInDb)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/categories/", response_model=List[CategoryInDb])
async def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()