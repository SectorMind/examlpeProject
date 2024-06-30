# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from auth import crud
from auth.schemas import UserCreate, UserUpdate, UserRead as UserSchema
from app.dependencies import get_current_active_user
from app.utils import get_password_hash

from typing import List
from uuid import UUID

router = APIRouter()


@router.post("/users/", response_model=UserSchema, dependencies=[Depends(get_current_active_user)])
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    db_user = await crud.get_user_by_username(db, user_name=user.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user.hashed_password = get_password_hash(user.hashed_password)
    db_user = await crud.create_user(db=db, user=user)
    return db_user


@router.get("/users/{user_id}", response_model=UserSchema, dependencies=[Depends(get_current_active_user)])
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_async_session)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=List[UserSchema], dependencies=[Depends(get_current_active_user)])
async def read_all_users(db: AsyncSession = Depends(get_async_session)):
    db_users = await crud.get_all_users(db)
    return db_users


@router.put("/users/{user_id}", response_model=UserSchema, dependencies=[Depends(get_current_active_user)])
async def update_user(user_id: UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_async_session)):
    db_user = await crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=UserSchema, dependencies=[Depends(get_current_active_user)])
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_async_session)):
    db_user = await crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
