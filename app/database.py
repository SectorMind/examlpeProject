# app/database.py
import asyncio

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, decl_api, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URL

# Create SQLAlchemy engine
# TODO: add echo_pool for useful logging
# engine = create_engine(DATABASE_URL, echo=True)
# make async_engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# TODO: uncomment code for create async session later and use it in app
# Session = sessionmaker(bind=engine)
async_session_maker = sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   )

# Base class for declarative models
Base: decl_api.DeclarativeMeta = declarative_base()


# Function to get a new database session


async def get_async_session():
    async with async_session_maker() as session:
        yield session


if __name__ == '__main__':
    # from sqlalchemy import MetaData
    # metadata = MetaData()
    # metadata.reflect(bind=engine)
    # metadata.drop_all(bind=engine)
    #
    # metadata.create_all(bind=engine)

    # try to create ordinary session
    # Session = sessionmaker(bind=engine)
    # session = Session()
    async def create_tables():
        async with engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
                print("Tables created")
            except Exception as err:
                print(str(err))
                print("Database didn't created")
                raise err

    asyncio.run(create_tables())



