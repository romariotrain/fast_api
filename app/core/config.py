import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:5431/db")

settings = Settings()