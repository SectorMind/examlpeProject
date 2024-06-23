# app/routers/consumer_ticket_link.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app import crud, schemas
from app.database import get_async_session

router = APIRouter()


@router.post("/purchase_tickets/", response_model=List[schemas.ConsumerTicketLink])
async def purchase_tickets(
        payload: schemas.PurchasePayload,
        db: AsyncSession = Depends(get_async_session)
):
    # Check if consumer exists
    db_consumer = await crud.get_consumer_by_email(db=db, email=payload.consumer.email)
    if not db_consumer:
        # Create consumer if not exists
        db_consumer = await crud.create_consumer(db=db, consumer=payload.consumer)

    db_links = []
    for ticket_data in payload.tickets:
        # Check if the ticket exists
        db_ticket = await crud.get_ticket_by_details(db=db, event_name=ticket_data.event_name, row=ticket_data.row,
                                                     seat=ticket_data.seat)
        if not db_ticket:
            raise HTTPException(status_code=404,
                                detail=f"Ticket for event {ticket_data.event_name}, row {ticket_data.row}, seat {ticket_data.seat} does not exist")

        # Check if the ticket is available
        if not await crud.is_ticket_available(db=db, ticket_id=db_ticket.id):
            raise HTTPException(status_code=400,
                                detail=f"Ticket for event {ticket_data.event_name}, row {ticket_data.row}, seat {ticket_data.seat} is already purchased")

        # Link consumer to ticket
        db_link = await crud.create_link_ticket_to_consumer(db=db, consumer_id=db_consumer.id, ticket_id=db_ticket.id)
        db_links.append(db_link)

    return db_links


@router.get("/purchase_tickets/", response_model=List[schemas.Ticket])
async def get_purchase_tickets(db: AsyncSession = Depends(get_async_session)):
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


@router.get("/consumer_ticket_link/", response_model=List[schemas.ConsumerTicketLink])
async def get_all_consumer_ticket_links(
    db: AsyncSession = Depends(get_async_session)
):
    links = await crud.get_all_consumer_ticket_links(db=db)
    return links


@router.get("/consumer_ticket_link/{link_id}", response_model=schemas.ConsumerTicketLink)
async def get_consumer_ticket_link(
        link_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    db_link = await crud.get_consumer_ticket_link_by_id(db=db, link_id=link_id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    return db_link


@router.put("/consumer_ticket_link/{link_id}", response_model=schemas.ConsumerTicketLink)
async def update_consumer_ticket_link(
        link_id: int,
        update_data: schemas.ConsumerTicketLinkUpdate,
        db: AsyncSession = Depends(get_async_session)
):
    db_link = await crud.get_consumer_ticket_link_by_id(db=db, link_id=link_id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")

    if update_data.consumer_id:
        db_link.consumer_id = update_data.consumer_id
    if update_data.ticket_id:
        ticket_exists = await crud.is_ticket_exists(db=db, ticket_id=update_data.ticket_id)
        if not ticket_exists:
            raise HTTPException(status_code=400, detail="Ticket not found")
        db_link.ticket_id = update_data.ticket_id

    await db.commit()
    await db.refresh(db_link)
    return db_link


@router.delete("/consumer_ticket_link/{link_id}", response_model=schemas.ConsumerTicketLink)
async def delete_consumer_ticket_link(
        link_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    db_link = await crud.get_consumer_ticket_link_by_id(db=db, link_id=link_id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")

    await crud.delete_consumer_ticket_link(db=db, link_id=link_id)
    return db_link
