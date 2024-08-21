import uuid
from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
import bcrypt

from app.users import schema, models
from .auth import create_access_token
from .models import User
from .views import authenticate_user, get_user_by_email
from ..arq_worker import get_redis_pool
from ..core.config import settings
from ..database import get_db
from ..utils import hash_password

router = APIRouter()

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


@router.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}


@router.post("/register",  response_model=schema.UserBase)
async def register(user: schema.UserCreate, db: Session = Depends(get_db)):

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


    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)

    redis = await get_redis_pool()
    await redis.enqueue_job('send_confirmation_email', user.email, user.name, confirmation_token)
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


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password/")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(hours=1)

    user.reset_password_token = token
    user.reset_password_expires_at = expires_at
    db.commit()
    redis = await get_redis_pool()
    await redis.enqueue_job('send_reset_password_email', user.email, user.name, token)
    return {"msg": "Password reset email sent"}


@router.post("/reset-password/")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_password_token == request.token).first()
    if not user or user.reset_password_expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.password = hash_password(request.new_password)
    user.reset_password_token = None
    user.reset_password_expires_at = None
    db.commit()

    return {"msg": "Password has been reset"}



