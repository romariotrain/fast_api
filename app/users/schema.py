import enum
from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel, EmailStr, constr, validator
import re


class Role(str, enum.Enum):
    company = "company"
    consumer = "consumer"


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str]
    # phone: constr(regex=r'^\+?[1-9]\d{1,14}$')
    phone: str


class UserCreate(UserBase):
    password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, confirm_password, values):
        password = values.get('password')
        if password != confirm_password:
            raise ValueError('Passwords do not match')
        return confirm_password


class UserUpdate(UserBase):
    password: Optional[str] = None
    photo: Optional[str]
    is_superuser: Optional[bool] = False


class UserInDBBase(UserBase):
    id: int
    photo: Optional[str] = None
    verified: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
    is_superuser: bool = False