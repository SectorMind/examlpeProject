# app/models.py
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, UUID_ID, GUID
from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey, DECIMAL, UniqueConstraint, Boolean, \
    Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as UUID_PG, ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import EmailType, PhoneNumberType

from app.database import Base

import enum
from datetime import datetime, timedelta
import uuid


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
    tickets = relationship("Ticket", back_populates="category")
    events = relationship("EventTicketCategory", back_populates="category")


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
    event_id: int = Column(Integer, ForeignKey("event.id"))
    row: str = Column(String)
    seat: str = Column(String)
    category_id: int = Column(Integer, ForeignKey("ticket_category.id"), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    consumer = relationship("ConsumerTicketLink", back_populates="ticket")
    events = relationship("EventTicketLink", back_populates="ticket")
    category = relationship("TicketCategory", back_populates="tickets")


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
    city_id = Column(Integer, ForeignKey("city.id"))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tickets = relationship("EventTicketLink", back_populates="event")
    categories = relationship("EventTicketCategory", back_populates="event")
    discounts = relationship("EventDiscount", back_populates="event")
    promo_codes = relationship("EventPromoCode", back_populates="event")
    city = relationship("City", back_populates="events")


class EventTicketCategory(Base):
    __tablename__ = "event_ticket_category"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    event_id: int = Column(Integer, ForeignKey("event.id"))
    category_id: int = Column(Integer, ForeignKey("ticket_category.id"))
    price: DECIMAL = Column(DECIMAL(10, 2), nullable=False)
    event = relationship("Event", back_populates="categories")
    category = relationship("TicketCategory", back_populates="events")

    __table_args__ = (UniqueConstraint('event_id', 'category_id', name='uq_event_category'),)


class DiscountTypeEnum(str, enum.Enum):
    PERCENTAGE = "percentage"
    AMOUNT = "amount"


class Discount(Base):
    __tablename__ = "discount"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    discount_name: str = Column(String, unique=True, nullable=False)
    discount_type = Column(SQLEnum(DiscountTypeEnum), default=DiscountTypeEnum.PERCENTAGE, nullable=False)
    discount_value: DECIMAL = Column(DECIMAL(10, 2), nullable=False)  # Example: 10.00 means 10% discount
    min_tickets: int = Column(Integer, nullable=True)  # Minimum tickets required to apply discount
    start_date: datetime = Column(DateTime, default=datetime.utcnow, nullable=True)
    end_date: datetime = Column(DateTime, default=datetime.utcnow() + timedelta(days=365*100), nullable=True)
    event_discounts = relationship("EventDiscount", back_populates="discount")


class PromoCode(Base):
    __tablename__ = "promo_code"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code: str = Column(String, unique=True, nullable=False)
    discount_type = Column(SQLEnum(DiscountTypeEnum), default=DiscountTypeEnum.PERCENTAGE, nullable=False)
    discount_value: DECIMAL = Column(DECIMAL(10, 2), nullable=False)  # Example: 10.00 means 10% discount
    max_uses: int = Column(Integer, nullable=True)  # Maximum times this promo code can be used
    start_date: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date: datetime = Column(DateTime, default=datetime.utcnow() + timedelta(days=365*100), nullable=False)
    event_promo_codes = relationship("EventPromoCode", back_populates="promo_code")


class EventDiscount(Base):
    __tablename__ = "event_discount"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    event_id: int = Column(Integer, ForeignKey("event.id"))
    discount_id: int = Column(Integer, ForeignKey("discount.id"))
    is_cumulative: bool = Column(Boolean, default=False)  # Whether the discount is cumulative with promo codes
    event = relationship("Event", back_populates="discounts")
    discount = relationship("Discount", back_populates="event_discounts")

    __table_args__ = (UniqueConstraint('event_id', 'discount_id', name='uq_event_discount'),)


class EventPromoCode(Base):
    __tablename__ = "event_promo_code"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    event_id: int = Column(Integer, ForeignKey("event.id"))
    promo_code_id: int = Column(Integer, ForeignKey("promo_code.id"))
    is_cumulative: bool = Column(Boolean, default=False)  # Whether the promo code is cumulative with discounts
    event = relationship("Event", back_populates="promo_codes")
    promo_code = relationship("PromoCode", back_populates="event_promo_codes")

    __table_args__ = (UniqueConstraint('event_id', 'promo_code_id', name='uq_event_promo_code'),)


class City(Base):
    __tablename__ = "city"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String, unique=True, nullable=False)
    events = relationship("Event", back_populates="city")


if __name__ == '__main__':
    time_4 = datetime.utcnow()
    print(time_4)
