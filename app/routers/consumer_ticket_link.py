# app/routers/consumer_ticket_link.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app import crud, schemas
from app.database import get_async_session

router = APIRouter()


# TODO: Fix /purchase_tickets/ so that it does not create a new ticket, but finds and compares it with existing ones.
@router.post("/purchase_tickets/", response_model=List[schemas.ConsumerTicketLink])
async def purchase_tickets(
        payload: schemas.PurchasePayload,
        db: AsyncSession = Depends(get_async_session)
):
    # Create consumer
    consumer_data = payload.consumer
    db_consumer = await crud.create_consumer(db=db, consumer=consumer_data)

    # Process each ticket
    db_links = []
    for ticket_data in payload.tickets:
        if not await crud.is_ticket_available(db=db, ticket_id=ticket_data.id):
            raise HTTPException(status_code=400, detail=f"Ticket with ID {ticket_data.id} is already purchased")
        db_ticket = await crud.create_ticket(db=db, ticket=ticket_data)
        db_link = await crud.create_link_ticket_to_consumer(db=db, consumer_id=db_consumer.id, ticket_id=db_ticket.id)
        db_links.append(db_link)
    return db_links


@router.get("/purchase_tickets/", response_model=List[schemas.Ticket])
async def get_consumer_tickets(db: AsyncSession = Depends(get_async_session)):
    purchased_tickets = await crud.get_purchased_tickets(db=db)
    if not purchased_tickets:
        raise HTTPException(status_code=404, detail="No tickets found for the consumer")
    return purchased_tickets


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
