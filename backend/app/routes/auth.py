from fastapi import APIRouter
from auth import fastapi_users, auth_backend
from models.user import User
from fastapi_users.schemas import BaseUserCreate, BaseUser, BaseUserUpdate
from pydantic import BaseModel, EmailStr
from uuid import UUID

router = APIRouter()

# ✅ Define User Schemas with `stripe_customer_id`
class UserRead(BaseUser):
    id: UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    stripe_customer_id: str | None  # ✅ Add this field

    class Config:
        from_attributes = True  # ✅ Required for SQLAlchemy serialization in Pydantic v2

class UserCreate(BaseUserCreate):
    username: str
    stripe_customer_id: str | None = None  # ✅ Add `stripe_customer_id` (optional)

class UserUpdate(BaseUserUpdate):
    username: str | None = None  # ✅ Make it optional
    stripe_customer_id: str | None = None  # ✅ Allow updates to Stripe ID

# ✅ Authentication Routes
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

# ✅ Registration Routes
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

# ✅ User Management Routes (Fixed Missing Argument)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),  # ✅ Fix: Added `UserUpdate`
    prefix="/users",
    tags=["users"]
)
