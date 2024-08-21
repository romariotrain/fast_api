import enum
import uuid

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, DateTime, Enum
from app.database import Base
from sqlalchemy.orm import relationship
from fastapi_users.manager import BaseUserManager


class Sname(Base):
    __tablename__ = "short_names"

    name = Column(String, primary_key=True, index=True)
    status = Column(Integer, unique=False, nullable=False)

class Lname(Base):
    __tablename__ = "full_names"

    name = Column(String, primary_key=True, index=True)
    status = Column(Integer, unique=False, nullable=True)
