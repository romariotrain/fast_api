from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

metadata = MetaData()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5431/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password_hash = Column(String)
#     is_active = Column(Boolean)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()