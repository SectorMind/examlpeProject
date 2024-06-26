# app/routers/admin_user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app import crud
from app.schemas import AdminUserCreate, AdminUserUpdate, AdminUser as AdminUserSchema
from app.dependencies import get_current_active_admin_user, get_current_active_user
from app.utils import get_password_hash

from typing import List
from uuid import UUID

router = APIRouter()


@router.post("/admin_users/", response_model=AdminUserSchema, dependencies=[Depends(get_current_active_admin_user)])
async def create_admin_user(admin_user: AdminUserCreate, db: AsyncSession = Depends(get_async_session)):
    db_admin_user = await crud.get_admin_user_by_username(db, username=admin_user.username)
    if db_admin_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    admin_user.hashed_password = get_password_hash(admin_user.hashed_password)
    db_admin_user = await crud.create_admin_user(db=db, admin_user=admin_user)
    return db_admin_user


@router.get("/admin_users/{user_id}", response_model=AdminUserSchema, dependencies=[Depends(get_current_active_user)])
async def read_admin_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    db_admin_user = await crud.get_admin_user(db, user_id=user_id)
    if db_admin_user is None:
        raise HTTPException(status_code=404, detail="Admin user not found")
    return db_admin_user


@router.get("/admin_users/", response_model=List[AdminUserSchema],
            dependencies=[Depends(get_current_active_admin_user)])
async def read_all_admin_users(db: AsyncSession = Depends(get_async_session)):
    db_admin_users = await crud.get_all_admin_users(db)
    return db_admin_users


@router.put("/admin_users/{user_id}", response_model=AdminUserSchema,
            dependencies=[Depends(get_current_active_admin_user)])
async def update_admin_user(user_id: UUID, admin_user: AdminUserUpdate, db: AsyncSession = Depends(get_async_session)):
    db_admin_user = await crud.update_admin_user(db, user_id=user_id, **admin_user.dict(exclude_unset=True))
    if db_admin_user is None:
        raise HTTPException(status_code=404, detail="Admin user not found")
    return db_admin_user


@router.delete("/admin_users/{user_id}", response_model=AdminUserSchema,
               dependencies=[Depends(get_current_active_admin_user)])
async def delete_admin_user(user_id: UUID, db: AsyncSession = Depends(get_async_session)):
    db_admin_user = await crud.delete_admin_user(db, user_id=user_id)
    if db_admin_user is None:
        raise HTTPException(status_code=404, detail="Admin user not found")
    return db_admin_user
