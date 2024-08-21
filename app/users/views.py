import uuid

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.arq_worker import get_redis_pool
# from app.celery.tasks import send_confirmation_email

from app.core.security import verify_password, get_password_hash
from app.database import get_db
from app.users.auth import verify_token
from app.users.models import User, UserManager
from app.users.schema import UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.name == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


async def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = str(uuid.uuid4())

    redis = await get_redis_pool()
    await redis.enqueue_job('send_confirmation_email', user.email, user.name, token)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = verify_token(token, credentials_exception)
    user = get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_db)):
    yield UserManager(user_db)


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)

