# app/routers/consumer_ticket_link.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app import crud, schemas
from app.database import get_async_session

router = APIRouter()


# TODO:Make it impossible to purchase an already purchased ticket.
@router.post("/link_ticket_to_consumer/", response_model=schemas.ConsumerTicketLink)
async def link_ticket_to_consumer(consumer_id: UUID, ticket_id: int, db: AsyncSession = Depends(get_async_session)):
    db_ticket = await crud.create_link_ticket_to_consumer(db=db, consumer_id=consumer_id, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=400, detail="Linking ticket to consumer failed")
    return db_ticket


@router.get("/consumer_tickets/{consumer_id}", response_model=List[schemas.Ticket])
async def get_consumer_tickets(consumer_id: UUID, db: AsyncSession = Depends(get_async_session)):
    purchased_tickets = await crud.get_consumer_tickets(db=db, consumer_id=consumer_id)
    if not purchased_tickets:
        raise HTTPException(status_code=404, detail="No tickets found for the consumer")
    return purchased_tickets
