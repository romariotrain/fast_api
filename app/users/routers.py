import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from app.users import schema, models
from .models import User
from ..database import get_db
from ..utils import hash_password
from app.celery.tasks import send_confirmation_email

router = APIRouter()


@router.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}


@router.post("/register",  response_model=schema.UserBase)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):

    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_phone = db.query(models.User).filter(models.User.phone == user.phone).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="User with this phone is already registered")

    hashed_password = hash_password(user.password)

    user_data = user.dict()
    user_data.pop("confirm_password")
    user_data.pop("password")

    confirmation_token = str(uuid.uuid4())

    new_user = models.User(**user_data, password=hashed_password, confirmation_token=confirmation_token)


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_confirmation_email.delay(user.email, user.username, confirmation_token)

    return new_user


@router.get("/confirm")
def confirm_registration(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.confirmation_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    user.verified = True
    db.commit()
    db.refresh(user)

    return {"message": "Your account has been verified"}
