# populate_ticket_categories.py

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import TicketCategoryEnum, TicketCategory
from app.database import engine, Base


async def create_ticket_categories():
    async with AsyncSession(engine) as session:
        async with session.begin():
            for category in TicketCategoryEnum:
                db_category = TicketCategory(category=category)
                session.add(db_category)
        await session.commit()


async def main():
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await create_ticket_categories()


if __name__ == "__main__":
    asyncio.run(main())
