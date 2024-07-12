# app/schemas.py
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from decimal import Decimal
import uuid
from datetime import datetime

from app.models import TicketStatus


class TicketCategoryEnum(str, Enum):
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


class TicketCategory(BaseModel):
    id: int
    category: TicketCategoryEnum

    class Config:
        orm_mode = True

class ConsumerTicketLink(BaseModel):
    id: int
    consumer_id: UUID
    ticket_id: int
    status: TicketStatus
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class Consumer(BaseModel):
    id: UUID
    name: str
    surname: str
    phone_number: str
    email: str

    class Config:
        orm_mode = True

class Ticket(BaseModel):
    id: int
    event_id: int
    row: str
    seat: str
    category_id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class EventTicketLink(BaseModel):
    id: int
    Event_id: int
    ticket_id: int

    class Config:
        orm_mode = True

class Event(BaseModel):
    id: int
    event_name: str
    date: datetime
    city_id: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class EventTicketCategory(BaseModel):
    id: int
    event_id: int
    category_id: int
    price: Decimal



class ConsumerTicketLinkUpdate(BaseModel):
    consumer_id: Optional[UUID] = None
    ticket_id: Optional[int] = None
    status: Optional[Enum] = None


class PurchasePayload(BaseModel):
    consumer: Consumer
    tickets: List[Ticket]
    status: TicketStatus


class Discount(BaseModel):
    id: int
    discount_name: str
    discount_value: Decimal
    min_tickets: int
    start_date: datetime
    end_date: datetime

class PromoCode(BaseModel):
    id: int
    code: str
    discount_value: Decimal
    max_uses: int
    start_date: datetime
    end_date: datetime

class EventDiscount(BaseModel):
    id: int
    event_id: int
    discount_id: int
    is_cumulative: bool


class EventPromoCode(BaseModel):
    id: int
    event_id: int
    promo_code_id: int
    is_cumulative: bool


class City(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


if __name__ == '__main__':
    your_uuid = uuid.uuid4()
    print(str(your_uuid))
    from datetime import datetime

    timestamp = datetime(2024, 6, 26, 19, 18, 4, 288531)
    print(timestamp)
