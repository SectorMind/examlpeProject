# app/routers/event.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/event/", response_model=schemas.Event)
async def create_event(event: schemas.Event, db: AsyncSession = Depends(get_async_session)):
    db_event = await crud.create_event(db=db, event=event)
    if db_event is None:
        raise HTTPException(status_code=400, detail="Event creation failed")
    return db_event


@router.get("/events/", response_model=List[schemas.Event])
async def get_events(db: AsyncSession = Depends(get_async_session)):
    events = await crud.get_events(db)
    return events
