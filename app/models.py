from sqlalchemy import Column, String, Integer, Time, Boolean, Text, ForeignKey, DateTime, Date, Enum, text,func
from enum import Enum as CustomEnum

from app import db, app


class Customer(db.Model):
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    # birthday = Column(Date, nullable=False)

class RoomType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)

class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, ForeignKey(RoomType.id), nullable=False)

class MovieType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

class Movie(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    age_limit = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    type = Column(Integer, ForeignKey(MovieType.id), nullable=False)

class MovieScreening(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(DateTime, nullable=False)
    room = Column(Integer, ForeignKey(Room.id), nullable=False)
    movie = Column(Integer, ForeignKey(Movie.id), nullable=False)

class Seat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(100), nullable=False)
    room = Column(Integer, ForeignKey(Room.id), nullable=False)

class TicketStatus(CustomEnum):
    AVAILABLE = 0
    HOLDING = 1,
    PAID = 2,
    CANCELLED = 3,
    USED = 4

class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.AVAILABLE)
    customer = Column(Integer, ForeignKey(Customer.id), nullable=False)
    seat = Column(Integer, ForeignKey(Seat.id), nullable=False)

class TicketBill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pay_time = Column(DateTime, nullable=False)
    is_paid = Column(Boolean, nullable=False)
    ticket = Column(Integer, ForeignKey(Ticket.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        u = Customer(full_name="", email="", phone_number="0123456789", username="123", password="123")
        db.session.add(u)
        db.session.commit()






