# app/routers/ticket.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_active_user, get_current_active_moderator_user, get_current_active_admin_user

router = APIRouter()


@router.post("/ticket/", response_model=schemas.Ticket)
async def create_ticket(ticket: schemas.Ticket, db: AsyncSession = Depends(get_async_session)):
    db_ticket = await crud.create_ticket(db=db, ticket=ticket)
    if db_ticket is None:
        raise HTTPException(status_code=400, detail="Ticket creation failed")
    return db_ticket


@router.get("/tickets/", response_model=List[schemas.Ticket])
async def get_tickets(db: AsyncSession = Depends(get_async_session)):
    tickets = await crud.get_tickets(db)
    return tickets


@router.put("/ticket/{ticket_id}", response_model=schemas.Ticket)
async def update_ticket(ticket_id: int, ticket: schemas.Ticket, db: AsyncSession = Depends(get_async_session)):
    db_ticket = await crud.update_ticket(db=db, ticket_id=ticket_id, ticket=ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.delete("/ticket/{ticket_id}", response_model=schemas.Ticket)
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_async_session)):
    db_ticket = await crud.delete_ticket(db=db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
