# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.authentication import CookieTransport
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_async_session
from auth import crud, schemas
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import verify_password

router = APIRouter()

cookie_transport = CookieTransport(cookie_name='ticket', cookie_max_age=3600)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token", response_model=schemas.Token)  # Ensure correct response model
async def login_for_access_token(db: AsyncSession = Depends(get_async_session),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_username(user_name=form_data.username, db=db)  # Fix argument order
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name, "role": user.role.value}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}