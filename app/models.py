from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


# for create tables to database
# from sqlalchemy.orm import declarative_base
# Base = declarative_base()

# class User(SQLAlchemyBaseUserTableUUID, Base):
#     __tablename__ = "user"
#
#     id: Mapped[UUID_ID] = mapped_column(
#         GUID, primary_key=True, default=uuid.uuid4
#     )
#     user_name: Mapped[str] = mapped_column(
#         String(length=255), unique=True, nullable=False
#     )
#     email: Mapped[str] = mapped_column(
#         EmailType(), unique=True, index=True, nullable=False
#     )
#     phone_number: Mapped[str] = mapped_column(
#         PhoneNumberType(region="RU"), unique=True, nullable=True,
#     )
#     hashed_password: Mapped[str] = mapped_column(
#         String(length=1024), nullable=False
#     )
#     is_active: Mapped[bool] = mapped_column(
#         Boolean, default=True, nullable=False
#     )
#     is_superuser: Mapped[bool] = mapped_column(
#         Boolean, default=False, nullable=False
#     )
#     is_verified: Mapped[bool] = mapped_column(
#         Boolean, default=False, nullable=False
#     )
class ConsumerTicketLink(Base):
    __tablename__ = "consumer_ticket_link"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    consumer_id: UUID = Column(UUID, ForeignKey("consumer.id"))
    ticket_id: int = Column(Integer, ForeignKey("ticket.id"))
    consumer = relationship("Consumer", back_populates="tickets")
    ticket = relationship("Ticket", back_populates="consumers")


class Consumer(Base):
    __tablename__ = "consumer"

    id: UUID = Column(UUID, primary_key=True, index=True)
    # TODO: bind to User table
    name: str = Column(String)
    surname: str = Column(String)
    phone_number: str = Column(String, unique=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    tickets = relationship("ConsumerTicketLink", back_populates="consumer")
    # tickets = relationship("Ticket", secondary="consumer_ticket_link", back_populates=Ticket.consumers) # wrong sintax


class Ticket(Base):
    __tablename__ = "ticket"

    id: int = Column(Integer, primary_key=True, index=True)
    # TODO: make seat identifier as separate class
    event_name: str = Column(String)
    row: str = Column(String)
    seat: str = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    consumers = relationship("ConsumerTicketLink", back_populates="ticket")


if __name__ == '__main__':
    pass
