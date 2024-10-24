# app/routers/consumer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app import crud, schemas
from app.database import get_async_session


router = APIRouter()


@router.post("/consumer/", response_model=schemas.Consumer)
async def create_consumer(consumer: schemas.Consumer, db: AsyncSession = Depends(get_async_session)):
    db_consumer = await crud.create_consumer(db=db, consumer=consumer)
    if db_consumer is None:
        raise HTTPException(status_code=400, detail="Consumer creation failed")
    return db_consumer


@router.get("/consumers/", response_model=List[schemas.Consumer])
async def get_consumers(db: AsyncSession = Depends(get_async_session)):
    consumers = await crud.get_consumers(db)
    return consumers


@router.put("/consumer/{consumer_id}", response_model=schemas.Consumer)
async def update_consumer(consumer_id: UUID, consumer: schemas.Consumer, db: AsyncSession = Depends(get_async_session)):
    db_consumer = await crud.update_consumer(db=db, consumer_id=consumer_id, consumer=consumer)
    if db_consumer is None:
        raise HTTPException(status_code=404, detail="Consumer not found")
    return db_consumer


@router.delete("/consumer/{consumer_id}", response_model=schemas.Consumer)
async def delete_consumer(consumer_id: UUID, db: AsyncSession = Depends(get_async_session)):
    db_consumer = await crud.delete_consumer(db=db, consumer_id=consumer_id)
    if db_consumer is None:
        raise HTTPException(status_code=404, detail="Consumer not found")
    return db_consumer