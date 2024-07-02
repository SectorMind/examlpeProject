# app/models.py
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, UUID_ID, GUID
from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey, UniqueConstraint, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as UUID_PG, ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import EmailType, PhoneNumberType

from app.database import Base

import enum
from datetime import datetime
import uuid
import bcrypt


class ConsumerTicketLink(Base):
    __tablename__ = "consumer_ticket_link"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    consumer_id: UUID = Column(UUID_PG(as_uuid=True), ForeignKey("consumer.id"))
    ticket_id: int = Column(Integer, ForeignKey("ticket.id"))
    consumer = relationship("Consumer", back_populates="tickets")
    ticket = relationship("Ticket", back_populates="consumers")

    __table_args__ = (UniqueConstraint('ticket_id', name='uq_ticket_id'),)


class Consumer(Base):
    __tablename__ = "consumer"

    id: UUID = Column(UUID_PG(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # TODO: bind to User table
    name: str = Column(String)
    surname: str = Column(String)
    phone_number: str = Column(String, unique=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    tickets = relationship("ConsumerTicketLink", back_populates="consumer")


class Ticket(Base):
    __tablename__ = "ticket"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # TODO: make seat identifier as separate class
    event_name: str = Column(String)
    row: str = Column(String)
    seat: str = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    consumers = relationship("ConsumerTicketLink", back_populates="ticket")


# class EventTicketLink(Base):
#     __tablename__ = "event_ticket_link"
#
#     id: int = Column(Integer, primary_key=True, autoincrement=True)
#     event_id: UUID = Column(UUID, ForeignKey("event.id"))
#     ticket_id: int = Column(Integer, ForeignKey("ticket.id"))
#     event = relationship("Event", back_populates="events")
#     ticket = relationship("Ticket", back_populates="consumers")


# class Event(Base):
#     __tablename__ = "event"
#
#     id: int = Column(Integer, primary_key=True, index=True)
#     event_name: str = Column(String)
#     date: datetime = Column(DateTime)
#     location: str = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     tickets = relationship("ConsumerTicketLink", back_populates="event")
#
#
# class Hall(Base):
#     __tablename__ = "hall"
#
#     id: int = Column(Integer, primary_key=True, index=True)
#     hall_name: str = Column(String)
#     row: str = Column(String)
#     seat: str = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     tickets = relationship("ConsumerTicketLink", back_populates="event")


if __name__ == '__main__':
    time_4 = datetime.utcnow()
    print(time_4)
