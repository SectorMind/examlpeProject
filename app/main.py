# app/main.py

from fastapi import FastAPI
# from app.database import Base, engine
from app.routers import consumer, event, ticket, consumer_ticket_link  # user, auth
# from app.admin import app as admin_app


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

# Mount admin panel
# app.mount("/admin", admin_app)

# Mount routers
app.include_router(consumer.router, prefix="/api/v1")
app.include_router(consumer_ticket_link.router, prefix="/api/v1")
# app.include_router(event.router, prefix="/api/v1")
app.include_router(ticket.router, prefix="/api/v1")
# app.include_router(user.router, prefix="/api/v1")
# app.include_router(auth.router, prefix="/api/v1")
