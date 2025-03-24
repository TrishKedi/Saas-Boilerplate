from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager, UUIDIDMixin
from fastapi_users.password import PasswordHelper
from fastapi_users.schemas import BaseUserCreate
from database import get_user_db
from models.user import User
from typing import AsyncGenerator
from fastapi import Request
from uuid import UUID

SECRET = "your_secret_key_here"

# ✅ JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# ✅ Authentication Backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)

class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
        self,
        user_create: BaseUserCreate,
        safe: bool = False,
        request: Request | None = None,
    ) -> User:
        user_dict = user_create.model_dump(exclude={"password"})
        hashed_password = self.password_helper.hash(user_create.password)

        user_dict["hashed_password"] = hashed_password

        return await self.user_db.create(user_dict)  # ✅ Corrected line

async def get_user_manager() -> AsyncGenerator[UserManager, None]:
    async for user_db in get_user_db():
        yield UserManager(user_db)


# ✅ Initialize FastAPIUsers
fastapi_users = FastAPIUsers[User, str](
    get_user_manager,
    [auth_backend]
)