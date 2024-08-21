import enum
import uuid

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, DateTime, Enum
from app.database import Base
from sqlalchemy.orm import relationship
from fastapi_users.manager import BaseUserManager


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    password = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    verified = Column(Boolean, nullable=False, server_default='False')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    is_superuser = Column(Boolean, nullable=False, server_default='False')
    confirmation_token = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False, unique=True, index=True)
    reset_password_token = Column(String, nullable=True)
    reset_password_expires_at = Column(DateTime, nullable=True)

class UserManager(BaseUserManager[User, uuid.UUID]):
    user_db_model = User


