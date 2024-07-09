from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import TicketCategory as TicketCategorySchema
from app.database import get_async_session
import app.crud as crud

router = APIRouter()


@router.post("/ticket_category/", response_model=TicketCategorySchema)
async def create_ticket_category(
        category: TicketCategorySchema,
        db: AsyncSession = Depends(get_async_session)
):
    return await crud.create_ticket_category(db=db, category=category)


@router.put("/ticket_category/{category_id}", response_model=TicketCategorySchema)
async def update_ticket_category(
        category_id: int,
        category: TicketCategorySchema,
        db: AsyncSession = Depends(get_async_session)
):
    return await crud.update_ticket_category(db=db, category_id=category_id, category=category)
