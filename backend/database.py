from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi_users.db import SQLAlchemyUserDatabase
from dotenv import load_dotenv
import os
from models.user import User, Base  # Use your DeclarativeBase explicitly
from typing import AsyncGenerator

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

# Create async engine explicitly using DATABASE_URL from .env
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# ✅ Correct get_user_db() function
async def get_user_db() -> AsyncGenerator[SQLAlchemyUserDatabase[User, str], None]:
    async with AsyncSessionLocal() as session:
        yield SQLAlchemyUserDatabase(session, User)
