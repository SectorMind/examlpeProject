# app/crud.py
from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Consumer, Ticket#, Event
from app.schemas import Consumer as ConsumerSchema, Ticket as TicketSchema
from uuid import uuid4
from datetime import datetime


# Create Consumer
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


# Create Ticket
async def create_ticket(db: AsyncSession, ticket: TicketSchema):
    db_ticket = Ticket(
        id=ticket.id,
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


# async def create_event(db: AsyncSession, event: Event):
#     db_event = Event(
#         id=uuid4(),
#         name=event.name,
#         date=event.date,
#         location=event.location,
#     )
#     db.add(db_event)
#     await db.commit()
#     await db.refresh(db_event)
#     return db_event
#
#
# async def get_events(db: AsyncSession):
#     result = await db.execute(select(Event))
#     events = result.scalars().all()
#     return events
