from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime, Date, Enum, UniqueConstraint
from enum import Enum as CustomEnum

from sqlalchemy.orm import relationship

from app import db, app
from datetime import datetime


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.now)

class UserRole(CustomEnum):
    CUSTOMER = 0
    ADMIN = 1

class Customer(Base, UserMixin):
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone_number = Column(String(100), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=True)
    avatar = Column(String(200), nullable=True, default="https://res.cloudinary.com/dkzxdp1gi/image/upload/v1767843265/avatar-trang-nu-001_dym4n0.webp")
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    def __str__(self):
        return self.full_name

class RoomType(Base):
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name

class Room(Base):
    room_type_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)
    number = Column(Integer, nullable=False, unique=True)
    image = Column(String(200), nullable=False)

    room_type = relationship(RoomType, backref="rooms")

    def __str__(self):
        return f"Phòng {self.number} ({self.room_type.name})"

class SeatStatus(CustomEnum):
    AVAILABLE = 0
    HOLDING = 1
    BOOKED = 2

class Seat(Base):
    row = Column(String(5), nullable=False)
    number = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)

    room = relationship(Room, backref="seats")

    __table_args__ = (
        UniqueConstraint('room_id', 'row', 'number', name='unique_seat_room'),
    )

    def __str__(self):
        return f"{self.room}, Ghế {self.row}{self.number}"

class MovieType(Base):
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name

class Movie(Base):
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    age_limit = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    poster = Column(String(200), nullable=False)
    release_date = Column(Date, nullable=False)

    def __str__(self):
        return self.title

class MovieTypeDetail(Base):
    type_id = Column(Integer, ForeignKey(MovieType.id, ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey(Movie.id, ondelete="CASCADE"), nullable=False)

    type = relationship("MovieType", backref="movie_type_details")
    movie = relationship("Movie", backref="movie_type_details")

    __table_args__ = (
        UniqueConstraint('type_id', 'movie_id', name='unique_movie_type'),
    )

class MovieScreening(Base):
    start_time = Column(DateTime, nullable=False)
    base_price = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)

    room = relationship("Room", backref="movie_screenings")
    movie = relationship("Movie", backref="movie_screenings")

    __table_args__ = (
        UniqueConstraint('room_id', 'start_time', name='unique_room_time'),
    )

    def __str__(self):
        return f"{self.start_time}"

class ScreeningSeat(Base):
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False, index=True)
    screening_id = Column(Integer, ForeignKey(MovieScreening.id), nullable=False, index=True)
    status = Column(Enum(SeatStatus), default=SeatStatus.AVAILABLE, index=True)
    hold_expired_at = Column(DateTime, index=True)
    holding_user_id = Column(Integer, ForeignKey(Customer.id), nullable=True)

    seat = relationship("Seat", backref="screening_seats",lazy=True)
    screening = relationship("MovieScreening", backref="screening_seats",lazy=True)
    holding_user = relationship("Customer", backref="holding_seats", lazy=True)

    __table_args__ = (
        UniqueConstraint('seat_id', 'screening_id', name='unique_seat_screening'),
    )

    def __str__(self):
        return f"{self.seat}  - Suất chiếu: {self.screening}"

class PaymentStatus(CustomEnum):
    PENDING = 0
    SUCCESS = 1
    FAILED = 2

class Bill(Base):
    total_amount = Column(Integer, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False, index=True)

    customer = relationship("Customer", backref="bills")

class TicketStatus(CustomEnum):
    HOLDING = 0
    PAID = 1
    CANCELLED = 2
    USED = 3

class Ticket(Base):
    price = Column(Integer, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.HOLDING, index=True)
    screening_seat_id = Column(Integer, ForeignKey(ScreeningSeat.id), nullable=False, index=True)
    bill_id = Column(Integer, ForeignKey(Bill.id, ondelete="CASCADE"), nullable=True, index=True)

    bill = relationship("Bill", backref="tickets")
    screening_seat = relationship("ScreeningSeat", backref="tickets")

class Payment(Base):
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    txn_ref = Column(String(100))
    vnp_transaction_id = Column(String(100))

    bill = relationship("Bill", backref="payments")

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        print("Tạo DB thành công!")
        #
        # import hashlib
        # admin = Customer(
        #     full_name = "Admin",
        #     username='admin',
        #     password=hashlib.md5("123".encode("utf-8")).hexdigest(),
        #     email='admin@gmail.com',
        #     phone_number='0357899304',
        #     role=UserRole.ADMIN
        # )
        # db.session.add(admin)
        # db.session.commit()

        # import string
        # def create_seats(room_id, num_rows, num_cols):
        #     rows = list(string.ascii_uppercase)[:num_rows]
        #
        #     for r in rows:
        #         for c in range(1, num_cols + 1):
        #             seat = Seat(
        #                 row=r,
        #                 number=c,
        #                 room_id=room_id
        #             )
        #             db.session.add(seat)
        #
        # for i in range(1, 12):
        #     create_seats(room_id=i, num_rows=10, num_cols=10)
        # db.session.commit()
        print("thêm ghế thành công!")


