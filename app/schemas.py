# app/schemas.py
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime

from fastapi_users.schemas import BaseUserCreate, BaseUser, BaseUserUpdate


class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    VIEWER = "viewer"

    class Config:
        use_enum_values = True
        orm_mode = True


class UserRead(BaseUser[UUID]):
    id: UUID
    user_name: str
    email: EmailStr
    phone_number: Optional[str]
    role: UserRole
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserCreate(BaseUserCreate):
    id: UUID
    user_name: str
    hashed_password: str
    email: EmailStr
    phone_number: Optional[str]
    role: UserRole
    created_at: datetime
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(BaseUserUpdate):
    user_name: Optional[str] = None
    hashed_password: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


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
    event_name: str
    row: str
    seat: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class ConsumerTicketLink(BaseModel):
    id: int
    consumer_id: UUID
    ticket_id: int

    class Config:
        orm_mode = True


class ConsumerTicketLinkUpdate(BaseModel):
    consumer_id: Optional[UUID] = None
    ticket_id: Optional[int] = None


class PurchasePayload(BaseModel):
    consumer: Consumer
    tickets: List[Ticket]


class Event(BaseModel):
    id: int
    event_name: str
    date: datetime
    location: str

    class Config:
        orm_mode = True


class EventTicketLink(BaseModel):
    id: int
    Event_id: int
    ticket_id: int

    class Config:
        orm_mode = True


class Hall(BaseModel):
    id: int
    hall_name: str
    row: str
    seat: str

    class Config:
        orm_mode = True


class EventHallLink(BaseModel):
    id: int
    event_id: int
    hall_id: int

    class Config:
        orm_mode = True


if __name__ == '__main__':
    your_uuid = uuid.uuid4()
    print(str(your_uuid))
    from datetime import datetime

    timestamp = datetime(2024, 6, 26, 19, 18, 4, 288531)
    print(timestamp)
