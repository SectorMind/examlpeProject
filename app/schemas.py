import enum
from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime


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
