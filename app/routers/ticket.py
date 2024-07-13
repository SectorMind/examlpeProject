# app/routers/ticket.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_active_user, get_current_active_moderator_user, get_current_active_admin_user
from app.models import Ticket, EventTicketCategory, TicketCategory, PromoCode, DiscountTypeEnum

router = APIRouter()


@router.post("/ticket/", response_model=schemas.Ticket)
async def create_ticket(ticket: schemas.Ticket, db: AsyncSession = Depends(get_async_session)):
    db_ticket = await crud.create_ticket(db=db, ticket=ticket)
    if db_ticket is None:
        raise HTTPException(status_code=400, detail="Ticket creation failed")
    return db_ticket


@router.post("/tickets/", response_model=List[schemas.Ticket])
async def create_tickets(tickets: schemas.TicketCreateList, db: AsyncSession = Depends(get_async_session)):
    db_tickets = []
    for ticket_data in tickets.tickets:
        db_ticket = await crud.create_ticket(db=db, ticket=ticket_data)
        if db_ticket is None:
            raise HTTPException(status_code=400, detail="Some tickets creation failed")
        db_tickets.append(db_ticket)
    return db_tickets


@router.get("/tickets/", response_model=List[schemas.Ticket])
async def get_tickets(db: AsyncSession = Depends(get_async_session)):
    tickets = await crud.get_tickets(db)
    return tickets


@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, db: Depends(get_async_session)):
    # Fetch the ticket
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Fetch the event ticket category
    event_ticket_category = db.query(EventTicketCategory).filter(
        EventTicketCategory.id == ticket.event_category_id).first()
    if not event_ticket_category:
        raise HTTPException(status_code=404, detail="Event Ticket Category not found")

    # Fetch the ticket category
    ticket_category = db.query(TicketCategory).filter(TicketCategory.id == event_ticket_category.category_id).first()
    if not ticket_category:
        raise HTTPException(status_code=404, detail="Ticket Category not found")

    return {
        "ticket_id": ticket.id,
        "row": ticket.row,
        "seat": ticket.seat,
        "category": ticket_category.category.value,
        "price": event_ticket_category.price
    }


@router.post("/tickets/{ticket_id}/apply_promo_code")
def apply_promo_code(ticket_id: int, promo_code: str, db: Depends(get_async_session)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    event_ticket_category = db.query(EventTicketCategory).filter(
        EventTicketCategory.id == ticket.event_category_id).first()
    if not event_ticket_category:
        raise HTTPException(status_code=404, detail="Event Ticket Category not found")

    promo = db.query(PromoCode).filter(PromoCode.code == promo_code).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")

    # Apply promo code to the price
    if promo.discount_type == DiscountTypeEnum.PERCENTAGE:
        discount_value = event_ticket_category.price * (promo.discount_value / 100)
    else:
        discount_value = promo.discount_value

    new_price = event_ticket_category.price - discount_value
    if new_price < 0:
        new_price = 0

    return {
        "ticket_id": ticket.id,
        "original_price": event_ticket_category.price,
        "discount_value": discount_value,
        "new_price": new_price
    }


@router.put("/ticket/{ticket_id}", response_model=schemas.Ticket)
async def update_ticket(ticket_id: int, ticket: schemas.Ticket, db: AsyncSession = Depends(get_async_session)):
    db_ticket = await crud.update_ticket(db=db, ticket_id=ticket_id, ticket=ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.delete("/ticket/{ticket_id}", response_model=schemas.Ticket)
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_async_session)):
    db_ticket = await crud.delete_ticket(db=db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
