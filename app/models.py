from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime, Date, Enum
from enum import Enum as CustomEnum
from app import db, app

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Customer(Base, UserMixin):
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    # birthday = Column(Date, nullable=False)

class RoomType(Base):
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)

class Room(Base):
    type = Column(Integer, ForeignKey(RoomType.id), nullable=False)

class MovieType(Base):
    name = Column(String(100), nullable=False)

class Movie(Base):
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    age_limit = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)

class MovieTypeDetail(Base):
    type = Column(Integer, ForeignKey(MovieType.id), nullable=False)
    movie = Column(Integer, ForeignKey(Movie.id), nullable=False)

class MovieScreening(Base):
    start_time = Column(DateTime, nullable=False)
    room = Column(Integer, ForeignKey(Room.id), nullable=False)
    movie = Column(Integer, ForeignKey(Movie.id), nullable=False)

class Seat(Base):
    location = Column(String(100), nullable=False)
    room = Column(Integer, ForeignKey(Room.id), nullable=False)

class TicketStatus(CustomEnum):
    AVAILABLE = 0
    HOLDING = 1,
    PAID = 2,
    CANCELLED = 3,
    USED = 4

class Ticket(Base):
    price = Column(Integer, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.AVAILABLE)
    customer = Column(Integer, ForeignKey(Customer.id), nullable=False)
    seat = Column(Integer, ForeignKey(Seat.id), nullable=False)

class TicketBill(Base):
    pay_time = Column(DateTime, nullable=False)
    is_paid = Column(Boolean, nullable=False)
    ticket = Column(Integer, ForeignKey(Ticket.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        u = Customer(full_name="", email="", phone_number="0123456789", username="123", password="123")
        db.session.add(u)
        db.session.commit()






