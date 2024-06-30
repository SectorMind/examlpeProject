# drop_all_tables.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base  # Import your SQLAlchemy Base from your app
from app.config import DATABASE_URL
import asyncio
from alembic import context
from alembic import command


async def drop_all_tables():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def main():
    await drop_all_tables()

    # Run Alembic migrations
    alembic_cfg = config().Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


if __name__ == '__main__':
    asyncio.run(main())
