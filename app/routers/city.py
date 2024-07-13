# app/routers/city.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app import crud, schemas
from app.database import get_async_session

router = APIRouter()


@router.post("/city/", response_model=schemas.City)
async def create_city(city: schemas.City, db: AsyncSession = Depends(get_async_session)):
    db_city = await crud.create_city(db=db, city=city)
    if db_city is None:
        raise HTTPException(status_code=400, detail="Consumer creation failed")
    return db_city


@router.get("/cities/", response_model=List[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_async_session)):
    cities = await crud.get_cities(db)
    return cities


@router.put("/city/{city_id}", response_model=schemas.City)
async def update_city(city_id: UUID, city: schemas.City, db: AsyncSession = Depends(get_async_session)):
    db_city = await crud.update_city(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="Consumer not found")
    return db_city


@router.delete("/city/{city_id}", response_model=schemas.City)
async def delete_city(city_id: UUID, db: AsyncSession = Depends(get_async_session)):
    db_city = await crud.delete_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="Consumer not found")
    return db_city
