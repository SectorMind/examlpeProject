# app/schemas.py
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    VIEWER = "viewer"


class AdminUserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    role: UserRole = UserRole.VIEWER


class AdminUserCreate(AdminUserBase):
    hashed_password: str
    phone_number: Optional[str] = None


class AdminUserUpdate(AdminUserBase):
    hashed_password: Optional[str] = None
    phone_number: Optional[str] = None


class AdminUser(AdminUserBase):
    id: UUID
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class AdminUserListResponse(BaseModel):
    admins: List[AdminUser]


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    full_name: str


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
