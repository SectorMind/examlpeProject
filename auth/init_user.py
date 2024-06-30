# app/init_user.py
# https://fastapi-users.github.io/fastapi-users/10.1/configuration/databases/sqlalchemy/
# https://github.com/artemonsh/fastapi_course/blob/main/Lesson_05/auth/auth.py
# https://www.youtube.com/watch?v=nfueh3ei8HU&t=59s


import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from auth.models import User, Base, UserRole
from app.utils import get_password_hash
from app.config import DATABASE_URL, TOKEN

from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

SECRET = TOKEN

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


async def init_user():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            user = User(
                id=uuid.uuid4(),  # Ensures the user ID is properly initialized
                user_name="string",
                email="string@gmail.com",
                is_active=True,
                role=UserRole.ADMIN,  # Assign the correct enum value for the role
                hashed_password=get_password_hash("string"),
                phone_number="string",
                is_superuser=True,  # Assuming the first user should be a superuser/admin
                is_verified=True  # Assuming the first user should be verified
            )
            session.add(user)

    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(init_user())
