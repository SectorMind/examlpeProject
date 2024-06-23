# create_admin.py
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base, AdminUser
from config import DATABASE_URL


async def create_admin():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(bind=engine, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            # Ensure the admin user doesn't already exist
            result = await session.execute(select(AdminUser).filter_by(username="admin"))
            user = result.scalars().first()
            if user:
                print("Admin user already exists.")
                return

            # Create new admin user
            hashed_password = bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin_user = AdminUser(username="admin", password=hashed_password)
            session.add(admin_user)
            await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_admin())
