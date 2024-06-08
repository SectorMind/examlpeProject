# app/crud.py
from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session
from uuid import uuid4
from app.models import Consumer, Ticket
from app.schemas import Consumer as ConsumerSchema, Ticket as TicketSchema

# Create Consumer
def create_consumer(db: Session, consumer: ConsumerSchema, user_id: int):
    db_consumer = Consumer(
        id=uuid4(),
        user_id=user_id,
        username=consumer.username,
        full_name=consumer.full_name,
        email=consumer.email,
        phone=consumer.phone,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_consumer)
    db.commit()
    db.refresh(db_consumer)
    return db_consumer
