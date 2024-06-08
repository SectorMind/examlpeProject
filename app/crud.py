# app/crud.py
from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import uuid4
from app.models import Consumer, Ticket
from app.schemas import Consumer as ConsumerSchema, Ticket as TicketSchema
from uuid import uuid4
from datetime import datetime


# Create Consumer
async def create_consumer(db: AsyncSession, consumer: ConsumerSchema):
    db_consumer = Consumer(
        id=consumer.id,
        name=consumer.name,
        surname=consumer.surname,
        phone_number=consumer.phone_number,
        email=consumer.email,
    )
    db.add(db_consumer)
    await db.commit()
    await db.refresh(db_consumer)
    return db_consumer


# Create Ticket
def create_ticket(db: Session, ticket: TicketSchema):
    db_consumer = Consumer(
        id=ticket.id,
        event_name=ticket.event_name,
        row=ticket.row,
        seat=ticket.seat,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_consumer)
    db.commit()
    db.refresh(db_consumer)
    return db_consumer
