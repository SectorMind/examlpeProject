# app/init_admin.py

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models import AdminUser, Base
from app.utils import get_password_hash
from app.config import DATABASE_URL


async def init_admin():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            admin_user = AdminUser(
                username="string",
                email="string@gmail.com",
                is_active=True,
                role="admin",
                hashed_password=get_password_hash("string"),
                phone_number="string"
            )
            session.add(admin_user)

    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(init_admin())
