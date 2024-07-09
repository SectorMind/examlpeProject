# app/models.py
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, UUID_ID, GUID
from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey, DECIMAL, UniqueConstraint, Boolean, \
    Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as UUID_PG, ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import EmailType, PhoneNumberType

from app.database import Base

import enum
from datetime import datetime
import uuid
from decimal import Decimal
import bcrypt


class TicketStatus(str, enum.Enum):
    PURCHASED = "purchased"
    RESERVE = "reserve"
    # FREE = "free"  # default if Ticket only


class TicketCategoryEnum(str, enum.Enum):
    PREMIUM = "premium"
    PREMIUM1 = "premium-1"
    PREMIUM2 = "premium-2"
    BUSINESS = "business"
    BUSINESS1 = "business-1"
    BUSINESS2 = "business-2"
    VIP = "vip"
    VIP1 = "vip-1"
    VIP2 = "vip-2"
    STANDARD = "standard"
    STANDARD1 = "standard-1"
    STANDARD2 = "standard-2"


class TicketCategory(Base):
    __tablename__ = "ticket_category"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(SQLEnum(TicketCategoryEnum), unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False, default=10000.00)  # Precision 10, scale 2


class ConsumerTicketLink(Base):
    __tablename__ = "consumer_ticket_link"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    consumer_id: UUID = Column(UUID_PG(as_uuid=True), ForeignKey("consumer.id"))
    ticket_id: int = Column(Integer, ForeignKey("ticket.id"))
    ticket_status: SQLEnum = Column(SQLEnum(TicketStatus), default=TicketStatus.RESERVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
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
    price: DECIMAL = Column(DECIMAL(10, 2), nullable=False)  # Precision 10, scale 2
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    consumers = relationship("ConsumerTicketLink", back_populates="ticket")
    events = relationship("EventTicketLink", back_populates="ticket")
    category = relationship("TicketCategory", back_populates="tickets")
    TicketCategory.tickets = relationship("Ticket", back_populates="category")



class EventTicketLink(Base):
    __tablename__ = "event_ticket_link"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    event_id: int = Column(Integer, ForeignKey("event.id"))
    ticket_id: int = Column(Integer, ForeignKey("ticket.id"))
    event = relationship("Event", back_populates="tickets")
    ticket = relationship("Ticket", back_populates="events")


class Event(Base):
    __tablename__ = "event"

    id: int = Column(Integer, primary_key=True, index=True)
    event_name: str = Column(String)
    date: datetime = Column(DateTime)
    location: str = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tickets = relationship("EventTicketLink", back_populates="event")


if __name__ == '__main__':
    time_4 = datetime.utcnow()
    print(time_4)
