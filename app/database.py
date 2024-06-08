import asyncio

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

from models import ConsumerTicketLink, Consumer, Ticket, Base

# Create SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session factory
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession)

# Base class for declarative models
# Base = declarative_base()


# Function to get a new database session
async def get_async_session():
    async with async_session_maker() as session:
        yield session


# Function to create tables
async def create_tables():
    async with engine.begin() as conn:
        try:
            print("Dropping all tables...")
            await conn.run_sync(Base.metadata.drop_all)
            print("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully")
        except SQLAlchemyError as err:
            print(f"SQLAlchemyError occurred: {err}")
            raise err
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e


if __name__ == '__main__':
    asyncio.run(create_tables())
