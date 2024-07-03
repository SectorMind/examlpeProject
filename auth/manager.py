# auth/manager.py
import os
from typing import Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, exceptions, models, schemas, UUIDIDMixin
from auth.models import User, UserRole
from app.utils import get_password_hash
from app.database import get_async_session

SECRET = os.getenv("SECRET_KEY", "default_secret")


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # Use logging instead of print for better practice
        import logging
        logging.info(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = get_password_hash(password)
        user_dict["role"] = UserRole.VIEWER  # or assign based on logic

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_async_session)):
    yield UserManager(user_db)
