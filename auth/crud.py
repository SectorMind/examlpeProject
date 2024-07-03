# auth/crud.py
from uuid import uuid4, UUID
from datetime import datetime

from fastapi import HTTPException, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth.models import User
from auth.schemas import UserCreate, UserUpdate
from app.utils import get_password_hash
from app.database import get_async_session
from auth.manager import UserManager
from auth.init_user import auth_backend


async def get_user_manager(user_db=Depends(get_async_session)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager, [auth_backend]
)


async def get_user_by_username(user_name: str, db: AsyncSession = Depends(get_async_session)) -> User:
    result = await db.execute(select(User).where(User.user_name == user_name))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    if not user.phone_number:
        raise HTTPException(status_code=400, detail="Phone number is required for admin user creation")

    hashed_password = get_password_hash(user.hashed_password)
    db_user = User(
        id=uuid4(),
        user_name=user.user_name,
        hashed_password=hashed_password,
        email=user.email,
        phone_number=user.phone_number,
        role=user.role,
        created_at=datetime.utcnow(),
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_verified=user.is_verified
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: UUID, user_update: UserUpdate) -> User:
    db_user = await get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.hashed_password:
        user_update.hashed_password = get_password_hash(user_update.hashed_password)
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: UUID) -> User:
    db_user = await get_user(db=db, user_id=user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
