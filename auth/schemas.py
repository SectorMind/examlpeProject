# auth/schemas.py
from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from fastapi_users.schemas import BaseUserCreate, BaseUser, BaseUserUpdate
from pydantic import EmailStr, BaseModel
from enum import Enum


# class UserRole(str, Enum):
#     ADMIN = "admin"
#     MODERATOR = "moderator"
#     VIEWER = "viewer"
#
#     class Config:
#         use_enum_values = True
#         orm_mode = True
#
#
# class UserRead(BaseUser[UUID]):
#     id: UUID
#     user_name: str  # Updated to match the User model
#     email: EmailStr
#     phone_number: Optional[str]  # Made optional to match the User model
#     role: UserRole  # Corrected Enum type
#     is_active: bool
#     is_superuser: bool
#     is_verified: bool
#
#     class Config:
#         orm_mode = True
#
#
# class UserCreate(BaseUserCreate):
#     id: UUID
#     user_name: str  # Updated to match the User model
#     hashed_password: str
#     email: EmailStr
#     phone_number: Optional[str]  # Made optional to match the User model
#     role: UserRole  # Corrected Enum type
#     created_at: datetime
#     is_active: Optional[bool] = True
#     is_superuser: Optional[bool] = False
#     is_verified: Optional[bool] = False
#
#
# class UserUpdate(BaseUserUpdate):
#     user_name: Optional[str] = None  # Added to match the User model
#     hashed_password: Optional[str] = None
#     email: Optional[EmailStr] = None
#     phone_number: Optional[str] = None  # Made optional to match the User model
#     role: Optional[UserRole] = None  # Added to allow role updates
#     is_active: Optional[bool] = None
#     is_superuser: Optional[bool] = None
#     is_verified: Optional[bool] = None
