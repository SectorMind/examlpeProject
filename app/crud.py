# app/crud.py
from typing import Type
import bcrypt

from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import update

from app.models import Consumer, Ticket, TicketCategory, TicketCategoryEnum, ConsumerTicketLink, TicketStatus, Event, \
    City, EventTicketCategory
from app.schemas import \
    Consumer as ConsumerSchema, \
    Ticket as TicketSchema, \
    TicketCategory as TicketCategorySchema, \
    ConsumerTicketLink as ConsumerTicketLinkSchema, \
    Event as EventSchema, \
    City as CitySchema, \
    EventTicketCategory as EventTicketCategorySchema, \
    EventTicketLink as EventTicketLinkSchema
from app.utils import get_password_hash

from uuid import uuid4, UUID
from datetime import datetime


async def create_link_ticket_to_consumer(db: AsyncSession, consumer_id: UUID, ticket_id: int):
    # Check if the ticket is already linked to a consumer
    if not await is_ticket_available(db, ticket_id):
        raise HTTPException(status_code=400, detail="Ticket is already purchased")

    db_link = ConsumerTicketLink(
        consumer_id=consumer_id,
        ticket_id=ticket_id,
        ticket_status=TicketStatus.RESERVE,
    )
    db.add(db_link)
    try:
        await db.commit()
        await db.refresh(db_link)
        return db_link
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to link ticket to consumer")


async def get_all_consumer_ticket_links(db: AsyncSession):
    result = await db.execute(
        select(
            ConsumerTicketLink.id,
            ConsumerTicketLink.consumer_id,
            ConsumerTicketLink.ticket_id,
            ConsumerTicketLink.ticket_status.label('status')
        )
    )
    return result.all()


async def get_consumer_ticket_link_by_id(db: AsyncSession, link_id: int):
    result = await db.execute(select(ConsumerTicketLink).where(ConsumerTicketLink.id == link_id))
    return result.scalars().first()


async def is_ticket_exists(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    return result.scalars().first() is not None


async def delete_consumer_ticket_link(db: AsyncSession, link_id: int):
    result = await db.execute(select(ConsumerTicketLink).where(ConsumerTicketLink.id == link_id))
    db_link = result.scalars().first()
    if db_link:
        await db.delete(db_link)
        await db.commit()
    return db_link


async def is_ticket_available(db: AsyncSession, ticket_id: int) -> bool:
    result = await db.execute(select(ConsumerTicketLink).filter(ConsumerTicketLink.ticket_id == ticket_id))
    link = result.scalars().first()
    return link is None


async def get_consumer_tickets(db: AsyncSession, consumer_id: UUID):
    result = await db.execute(
        select(Ticket).join(ConsumerTicketLink).filter(ConsumerTicketLink.consumer_id == consumer_id))
    tickets = result.scalars().all()
    return tickets


async def get_consumer_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Consumer).filter(Consumer.email == email))
    return result.scalars().first()


async def get_ticket_by_details(db: AsyncSession, event_name: str, row: str, seat: str):
    result = await db.execute(
        select(Ticket).filter(Ticket.event_name == event_name, Ticket.row == row, Ticket.seat == seat))
    return result.scalars().first()


# Consumer
async def create_consumer(db: AsyncSession, consumer: ConsumerSchema):
    db_consumer = Consumer(
        id=uuid4(),
        name=consumer.name,
        surname=consumer.surname,
        phone_number=consumer.phone_number,
        email=consumer.email,
    )
    db.add(db_consumer)
    await db.commit()
    await db.refresh(db_consumer)
    return db_consumer


async def get_consumers(db: AsyncSession):
    result = await db.execute(select(Consumer))
    consumers = result.scalars().all()
    return consumers


async def update_consumer(db: AsyncSession, consumer_id: UUID, consumer: ConsumerSchema):
    result = await db.execute(select(Consumer).filter(Consumer.id == consumer_id))
    db_consumer = result.scalars().first()
    if db_consumer:
        db_consumer.name = consumer.name
        db_consumer.surname = consumer.surname
        db_consumer.phone_number = consumer.phone_number
        db_consumer.email = consumer.email
        await db.commit()
        await db.refresh(db_consumer)
    return db_consumer


async def delete_consumer(db: AsyncSession, consumer_id: UUID):
    result = await db.execute(select(Consumer).filter(Consumer.id == consumer_id))
    db_consumer = result.scalars().first()
    if db_consumer:
        await db.delete(db_consumer)
        await db.commit()
    return db_consumer


# City
async def create_city(db: AsyncSession, city: CitySchema):
    db_city = City(
        name=city.name,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_cities(db: AsyncSession):
    result = await db.execute(select(City))
    cities = result.scalars().all()
    return cities


async def update_city(db: AsyncSession, city_id: UUID, city: CitySchema):
    result = await db.execute(select(City).filter(City.id == city_id))
    db_city = result.scalars().first()
    if db_city:
        db_city.name = city.name
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: UUID):
    result = await db.execute(select(City).filter(City.id == city_id))
    db_city = result.scalars().first()
    if db_city:
        await db.delete(db_city)
        await db.commit()
    return db_city


async def create_ticket_category(db: AsyncSession, category: TicketCategorySchema):
    db_category = TicketCategory(
        category=category.category
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def update_ticket_category(db: AsyncSession, category_id: int, category: TicketCategorySchema):
    query = await db.execute(select(TicketCategory).filter(TicketCategory.id == category_id))
    db_category = query.scalar_one_or_none()

    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.category = category.category

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def create_event_ticket_category(db: AsyncSession, category: EventTicketCategorySchema):
    db_category = EventTicketCategory(
        event_id=category.event_id,
        category_id=category.category_id,
        price=category.price
    )
    db.add(db_category)
    try:
        await db.commit()
        await db.refresh(db_category)
        return db_category
    except IntegrityError:
        await db.rollback()
        return None


async def get_event_ticket_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(EventTicketCategory).filter(EventTicketCategory.id == category_id))
    return result.scalars().first()


async def get_event_ticket_categories(db: AsyncSession):
    result = await db.execute(select(EventTicketCategory))
    return result.scalars().all()


async def update_event_ticket_category(db: AsyncSession, category_id: int, category: EventTicketCategorySchema):
    result = await db.execute(select(EventTicketCategory).filter(EventTicketCategory.id == category_id))
    db_category = result.scalars().first()
    if db_category is None:
        return None

    db_category.event_id = category.event_id
    db_category.category_id = category.category_id
    db_category.price = category.price

    try:
        await db.commit()
        await db.refresh(db_category)
        return db_category
    except IntegrityError:
        await db.rollback()
        return None


async def delete_event_ticket_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(EventTicketCategory).filter(EventTicketCategory.id == category_id))
    db_category = result.scalars().first()
    if db_category is None:
        return None

    await db.delete(db_category)
    await db.commit()
    return db_category


async def create_ticket(db: AsyncSession, ticket: TicketSchema):
    result = await db.execute(select(TicketCategory).filter(TicketCategory.category == ticket.category.category))
    db_category = result.scalars().first()
    if not db_category:
        raise HTTPException(status_code=404, detail=f"Ticket category {ticket.category.category} does not exist")

    db_ticket = Ticket(
        event_name=ticket.event_name,
        row=ticket.row,
        seat=ticket.seat,
        category_id=db_category.id,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at
    )
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


async def update_ticket(db: AsyncSession, ticket_id: int, ticket: TicketSchema):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    db_ticket = result.scalars().first()
    if db_ticket:
        db_category = await db.execute(
            select(TicketCategory).filter(TicketCategory.category == ticket.category.category))
        db_category = db_category.scalars().first()
        if not db_category:
            raise HTTPException(status_code=404, detail=f"Ticket category {ticket.category.category} does not exist")

        db_ticket.event_name = ticket.event_name
        db_ticket.row = ticket.row
        db_ticket.seat = ticket.seat
        db_ticket.category_id = db_category.id
        db_ticket.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_ticket)
    return db_ticket


async def get_tickets(db: AsyncSession):
    result = await db.execute(select(Ticket))
    tickets = result.scalars().all()
    return tickets


async def get_purchased_tickets(db: AsyncSession):
    result = await db.execute(
        select(Ticket)
        .join(ConsumerTicketLink, Ticket.id == ConsumerTicketLink.ticket_id)
        .where(ConsumerTicketLink.ticket_status == TicketStatus.PURCHASED)
    )
    tickets = result.scalars().all()
    return tickets


async def get_reserve_tickets(db: AsyncSession):
    result = await db.execute(
        select(Ticket)
        .join(ConsumerTicketLink, Ticket.id == ConsumerTicketLink.ticket_id)
        .where(ConsumerTicketLink.ticket_status == TicketStatus.RESERVE)
    )
    tickets = result.scalars().all()
    return tickets


async def get_reserved_ticket_details(db: AsyncSession, consumer_id: UUID):
    result = await db.execute(
        select(
            Ticket.id,
            Ticket.event_id,
            Ticket.row,
            Ticket.seat,
            Ticket.price,
            TicketCategory.category,
            ConsumerTicketLink.ticket_status
        ).join(Ticket, ConsumerTicketLink.ticket_id == Ticket.id)
        .join(TicketCategory, Ticket.category_id == TicketCategory.id)
        .where(ConsumerTicketLink.consumer_id == consumer_id)
        .where(ConsumerTicketLink.ticket_status == TicketStatus.RESERVE)
    )
    tickets = result.all()
    return tickets


# async def purchase_ticket(db: AsyncSession, consumer_id: UUID, ticket_id: int):
#     # Create a link between the consumer and the ticket
#     db_link = ConsumerTicketLink(
#         consumer_id=consumer_id,
#         ticket_id=ticket_id,
#     )
#     try:
#         db.add(db_link)
#         await db.commit()
#         await db.refresh(db_link)
#         return db_link
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=400, detail="Ticket is already purchased")
async def confirm_ticket_purchase(db: AsyncSession, link_id: int):
    result = await db.execute(select(ConsumerTicketLink).where(ConsumerTicketLink.id == link_id))
    db_link = result.scalars().first()
    if db_link:
        stmt = (
            update(ConsumerTicketLink)
            .where(ConsumerTicketLink.id == link_id)
            .values(ticket_status=TicketStatus.PURCHASED)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(db_link)
        return db_link
    else:
        raise HTTPException(status_code=404, detail="Link not found")


async def update_ticket(db: AsyncSession, ticket_id: int, ticket: TicketSchema):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    db_ticket = result.scalars().first()
    if db_ticket:
        db_ticket.event_name = ticket.event_name
        db_ticket.row = ticket.row
        db_ticket.seat = ticket.seat
        db_ticket.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_ticket)
    return db_ticket


async def delete_ticket(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    db_ticket = result.scalars().first()
    if db_ticket:
        await db.delete(db_ticket)
        await db.commit()
    return db_ticket


def make_naive(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def create_event(db: AsyncSession, event: EventSchema):
    db_event = Event(
        event_name=event.event_name,
        date=make_naive(event.date),
        city_id=event.city_id
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def get_events(db: AsyncSession):
    result = await db.execute(select(Event))
    events = result.scalars().all()
    return events
