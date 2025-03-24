from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi_users.db import SQLAlchemyUserDatabase
from dotenv import load_dotenv
import os
from models.user import User
from typing import AsyncGenerator

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

# Create async engine
engine = create_async_engine("postgresql+asyncpg://saas_user:1234@localhost/saas_boilerplate", echo=True)

# Create session
AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base model for SQLAlchemy
Base = declarative_base()

# ✅ Ensure `get_user_db()` returns a correct database session
async def get_user_db() -> AsyncGenerator[SQLAlchemyUserDatabase[User, str], None]:
    async with AsyncSessionLocal() as session:
        yield SQLAlchemyUserDatabase(session, User)
