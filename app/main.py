
from fastapi import FastAPI
# from app.database import Base, engine
from app.routers import consumer


import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log to a file
    filemode='a'  # Append mode
)

app = FastAPI()

# TODO: combine it in the separate function
# Create database tables
# Base.metadata.create_all(bind=engine)

# Mount routers
app.include_router(consumer.router, prefix="/api/v1")

