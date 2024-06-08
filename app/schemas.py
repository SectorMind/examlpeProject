import enum
from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional


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

    class Config:
        orm_mode = True


class ConsumerTicketLink(BaseModel):
    id: int
    consumer_id: UUID
    ticket_id: str

    class Config:
        orm_mode = True
