# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
# from app.database import Base, engine
from app.routers import consumer, event, city, ticket, ticket_category, consumer_ticket_link, user, auth, \
    event_ticket_category
# from app.admin import app as admin_app

import logging
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log to a file
    filemode='a'  # Append mode
)
# gunicorn_error_logger = logging.getLogger("gunicorn.error")
# gunicorn_logger = logging.getLogger("gunicorn")
# uvicorn_access_logger = logging.getLogger("uvicorn.access")
#
# uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
# fastapi_logger = logging.getLogger("fastapi")
# fastapi_logger.handlers = gunicorn_error_logger.handlers
#
# fastapi_logger.setLevel(logging.DEBUG)
# logger = logging.getLogger("uvicorn.access")

app = FastAPI()

# Middleware to log requests and responses
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger.info(f"Start request path={request.url.path} method={request.method}")
#
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#
#     logger.info(
#         f"Completed request path={request.url.path} method={request.method} "
#         f"status_code={response.status_code} process_time={process_time:.2f}s"
#     )
#     return response

# TODO: combine it in the separate function
# Create database tables
# Base.metadata.create_all(bind=engine)

# Mount admin panel
# app.mount("/admin", admin_app)

# Mount routers
app.include_router(consumer.router, prefix="/api/v1")
app.include_router(consumer_ticket_link.router, prefix="/api/v1")
app.include_router(event.router, prefix="/api/v1")
app.include_router(city.router, prefix="/api/v1")
app.include_router(ticket.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(ticket_category.router, prefix="/api/v1")
app.include_router(event_ticket_category.router, prefix="/api/v1")
