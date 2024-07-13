# app/routers/event_ticket_category.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import EventTicketCategory as EventTicketCategorySchema
from app.database import get_async_session
import app.crud as crud

from typing import List

router = APIRouter()


@router.post("/event_ticket_category/", response_model=EventTicketCategorySchema)
async def create_event_ticket_category(
        category: EventTicketCategorySchema,
        db: AsyncSession = Depends(get_async_session)
):
    return await crud.create_event_ticket_category(db=db, category=category)


@router.get("/event_ticket_category/{category_id}", response_model=EventTicketCategorySchema)
async def get_event_ticket_category(
        category_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    db_category = await crud.get_event_ticket_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="EventTicketCategory not found")
    return db_category


@router.get("/event_ticket_categories/", response_model=List[EventTicketCategorySchema])
async def get_event_ticket_categories(
        db: AsyncSession = Depends(get_async_session)
):
    return await crud.get_event_ticket_categories(db=db)


@router.put("/event_ticket_category/{category_id}", response_model=EventTicketCategorySchema)
async def update_event_ticket_category(
        category_id: int,
        category: EventTicketCategorySchema,
        db: AsyncSession = Depends(get_async_session)
):
    return await crud.update_event_ticket_category(db=db, category_id=category_id, category=category)


@router.delete("/event_ticket_category/{category_id}", response_model=EventTicketCategorySchema)
async def delete_event_ticket_category(
        category_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    db_category = await crud.delete_event_ticket_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="EventTicketCategory not found")
    return db_category
