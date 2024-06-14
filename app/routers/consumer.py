# app/routers/consumer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


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

# @router.get("/{consumer_id}", response_model=schemas.Consumer)
# def read_consumer(consumer_id: int, db: Session = Depends(get_db)):
#     db_consumer = crud.get_consumer(db, consumer_id=consumer_id)
#     if db_consumer is None:
#         raise HTTPException(status_code=404, detail="Consumer not found")
#     return db_consumer
#
#
# @router.put("/{consumer_id}", response_model=schemas.Consumer)
# def update_consumer(consumer_id: int, consumer: schemas.Consumer, db: Session = Depends(get_db)):
#     db_consumer = crud.get_consumer(db, consumer_id=consumer_id)
#     if db_consumer is None:
#         raise HTTPException(status_code=404, detail="Consumer not found")
#     return crud.update_consumer(db=db, consumer_id=consumer_id, consumer=consumer)
#
#
# @router.delete("/{consumer_id}", response_model=schemas.Consumer)
# def delete_consumer(consumer_id: int, db: Session = Depends(get_db)):
#     db_consumer = crud.get_consumer(db, consumer_id=consumer_id)
#     if db_consumer is None:
#         raise HTTPException(status_code=404, detail="Consumer not found")
#     return crud.delete_consumer(db=db, consumer_id=consumer_id)
#
#
# @router.get("/", response_model=List[schemas.Consumer])
# def read_consumers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     consumers = crud.get_consumers(db, skip=skip, limit=limit)
#     return consumers
