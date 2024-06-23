# app/routers/admin_user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.database import get_async_session

router = APIRouter()


# @router.post("/register", response_model=User)
# async def register_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
#     hashed_password = get_password_hash(user.password)
#     db_user = UserInDB(username=user.username, email=user.email, full_name=user.full_name,
#                        hashed_password=hashed_password)
#     db.add(db_user)
#     await db.commit()
#     await db.refresh(db_user)
#     return db_user
#
#
# @router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
#                                  db: AsyncSession = Depends(get_async_session)):
#     user = await authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @router.post("/admin_user/", response_model=dict)
# async def create_admin_user(username: str, password: str, db: AsyncSession = Depends(get_async_session)):
#     db_admin_user = await crud.create_admin_user(db=db, username=username, password=password)
#     if db_admin_user is None:
#         raise HTTPException(status_code=400, detail="Admin user creation failed")
#     return {"username": db_admin_user.username}
#
#
# @router.post("/admin_user/login/", response_model=dict)
# async def login_admin_user(username: str, password: str, db: AsyncSession = Depends(get_async_session)):
#     db_admin_user = await crud.authenticate_admin_user(db=db, username=username, password=password)
#     if db_admin_user is None:
#         raise HTTPException(status_code=400, detail="Invalid username or password")
#     return {"message": "Login successful"}
