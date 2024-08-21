import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

metadata = MetaData()
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5431/db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

# Создание асинхронного SessionLocal
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session