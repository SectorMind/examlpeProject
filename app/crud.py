# app/crud.py
from typing import Type
import bcrypt

from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from app.models import Consumer, Ticket, ConsumerTicketLink, Event
from app.schemas import Consumer as ConsumerSchema, Ticket as TicketSchema, \
    ConsumerTicketLink as ConsumerTicketLinkSchema, Event as EventSchema
from app.utils import get_password_hash

from uuid import uuid4, UUID
from datetime import datetime


async def create_link_ticket_to_consumer(db: AsyncSession, consumer_id: UUID, ticket_id: int):
    # Check if the ticket is already linked to a consumer
    if not await is_ticket_available(db, ticket_id):
        raise HTTPException(status_code=400, detail="Ticket is already purchased")

    db_link = ConsumerTicketLink(
        consumer_id=consumer_id,
        ticket_id=ticket_id,
    )
    db.add(db_link)
    try:
        await db.commit()
        await db.refresh(db_link)
        return db_link
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to link ticket to consumer")


async def get_all_consumer_ticket_links(db: AsyncSession):
    result = await db.execute(
        select(ConsumerTicketLink.id, ConsumerTicketLink.consumer_id, ConsumerTicketLink.ticket_id))
    return result.all()


async def get_consumer_ticket_link_by_id(db: AsyncSession, link_id: int):
    result = await db.execute(select(ConsumerTicketLink).where(ConsumerTicketLink.id == link_id))
    return result.scalars().first()


async def is_ticket_exists(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    return result.scalars().first() is not None


async def delete_consumer_ticket_link(db: AsyncSession, link_id: int):
    result = await db.execute(select(ConsumerTicketLink).where(ConsumerTicketLink.id == link_id))
    db_link = result.scalars().first()
    if db_link:
        await db.delete(db_link)
        await db.commit()
    return db_link


async def is_ticket_available(db: AsyncSession, ticket_id: int) -> bool:
    result = await db.execute(select(ConsumerTicketLink).filter(ConsumerTicketLink.ticket_id == ticket_id))
    link = result.scalars().first()
    return link is None


async def get_consumer_tickets(db: AsyncSession, consumer_id: UUID):
    result = await db.execute(
        select(Ticket).join(ConsumerTicketLink).filter(ConsumerTicketLink.consumer_id == consumer_id))
    tickets = result.scalars().all()
    return tickets


async def get_consumer_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Consumer).filter(Consumer.email == email))
    return result.scalars().first()


async def get_ticket_by_details(db: AsyncSession, event_name: str, row: str, seat: str):
    result = await db.execute(
        select(Ticket).filter(Ticket.event_name == event_name, Ticket.row == row, Ticket.seat == seat))
    return result.scalars().first()


# Consumer
async def create_consumer(db: AsyncSession, consumer: ConsumerSchema):
    db_consumer = Consumer(
        id=uuid4(),
        name=consumer.name,
        surname=consumer.surname,
        phone_number=consumer.phone_number,
        email=consumer.email,
    )
    db.add(db_consumer)
    await db.commit()
    await db.refresh(db_consumer)
    return db_consumer


async def get_consumers(db: AsyncSession):
    result = await db.execute(select(Consumer))
    consumers = result.scalars().all()
    return consumers


async def update_consumer(db: AsyncSession, consumer_id: UUID, consumer: ConsumerSchema):
    result = await db.execute(select(Consumer).filter(Consumer.id == consumer_id))
    db_consumer = result.scalars().first()
    if db_consumer:
        db_consumer.name = consumer.name
        db_consumer.surname = consumer.surname
        db_consumer.phone_number = consumer.phone_number
        db_consumer.email = consumer.email
        await db.commit()
        await db.refresh(db_consumer)
    return db_consumer


async def delete_consumer(db: AsyncSession, consumer_id: UUID):
    result = await db.execute(select(Consumer).filter(Consumer.id == consumer_id))
    db_consumer = result.scalars().first()
    if db_consumer:
        await db.delete(db_consumer)
        await db.commit()
    return db_consumer


# Create Ticket
async def create_ticket(db: AsyncSession, ticket: TicketSchema):
    db_ticket = Ticket(
        # id=ticket.id,
        event_name=ticket.event_name,
        row=ticket.row,
        seat=ticket.seat,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at
    )
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


async def get_tickets(db: AsyncSession):
    result = await db.execute(select(Ticket))
    tickets = result.scalars().all()
    return tickets


async def get_purchased_tickets(db: AsyncSession):
    result = await db.execute(select(Ticket).join(ConsumerTicketLink))
    tickets = result.scalars().all()
    return tickets


async def purchase_ticket(db: AsyncSession, consumer_id: UUID, ticket_id: int):
    # Create a link between the consumer and the ticket
    db_link = ConsumerTicketLink(
        consumer_id=consumer_id,
        ticket_id=ticket_id,
    )
    try:
        db.add(db_link)
        await db.commit()
        await db.refresh(db_link)
        return db_link
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Ticket is already purchased")


async def update_ticket(db: AsyncSession, ticket_id: int, ticket: TicketSchema):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    db_ticket = result.scalars().first()
    if db_ticket:
        db_ticket.event_name = ticket.event_name
        db_ticket.row = ticket.row
        db_ticket.seat = ticket.seat
        db_ticket.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_ticket)
    return db_ticket


async def delete_ticket(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    db_ticket = result.scalars().first()
    if db_ticket:
        await db.delete(db_ticket)
        await db.commit()
    return db_ticket


def make_naive(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def create_event(db: AsyncSession, event: EventSchema):
    db_event = Event(
        event_name=event.event_name,
        date=make_naive(event.date),
        location=event.location
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def get_events(db: AsyncSession):
    result = await db.execute(select(Event))
    events = result.scalars().all()
    return events
