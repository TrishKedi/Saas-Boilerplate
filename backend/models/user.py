# models/user.py
from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

class Base(DeclarativeBase):
    __table_args__ = {'schema': 'public'}  # explicitly use public schema

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    __table_args__ = {'schema': 'public'}  # explicitly use public schema

    username = Column(String(length=50), nullable=True, unique=True)
    stripe_customer_id = Column(String, nullable=True)
