# auth/models.py
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, UUID_ID, GUID
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType, PhoneNumberType

from app.database import Base

import enum
from datetime import datetime
import uuid


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    VIEWER = "viewer"


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    id: Mapped[UUID_ID] = mapped_column(
        GUID, primary_key=True, default=uuid.uuid4
    )
    user_name: Mapped[str] = mapped_column(
        String(length=255), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    email: Mapped[str] = mapped_column(
        EmailType(), unique=True, index=True, nullable=False
    )
    phone_number: Mapped[PhoneNumberType] = mapped_column(
        PhoneNumberType(region="RU"), unique=True, nullable=True
    )
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole), default=UserRole.VIEWER
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
