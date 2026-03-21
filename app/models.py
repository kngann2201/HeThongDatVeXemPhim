from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime, Date, Enum, UniqueConstraint
from enum import Enum as CustomEnum
from app import db, app
from datetime import datetime


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.now)

class Customer(Base):
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone_number = Column(String(100), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=False)
    avatar = Column(String(200), nullable=True, default="https://res.cloudinary.com/dkzxdp1gi/image/upload/v1767843265/avatar-trang-nu-001_dym4n0.webp")

class RoomType(Base):
    name = Column(String(100), nullable=False)

class Room(Base):
    room_type = Column(Integer, ForeignKey(RoomType.id), nullable=False)
    image = Column(String(200), nullable=False)

class MovieType(Base):
    name = Column(String(100), nullable=False)

class Movie(Base):
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    age_limit = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    poster = Column(String(200), nullable=False)

class MovieTypeDetail(Base):
    type = Column(Integer, ForeignKey(MovieType.id), nullable=False)
    movie = Column(Integer, ForeignKey(Movie.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('type', 'movie', name='unique_movie_type'),
    )

class MovieScreening(Base):
    start_time = Column(DateTime, nullable=False)
    room = Column(Integer, ForeignKey(Room.id), nullable=False)
    movie = Column(Integer, ForeignKey(Movie.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('room', 'start_time', name='unique_room_time'),
    )

class Seat(Base):
    row = Column(String(5), nullable=False)
    number = Column(Integer, nullable=False)
    room = Column(Integer, ForeignKey(Room.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('room', 'row', 'number', name='unique_seat_room'),
    )

class TicketStatus(CustomEnum):
    AVAILABLE = 0
    HOLDING = 1
    PAID = 2
    CANCELLED = 3
    USED = 4

class BillStatus(CustomEnum):
    PENDING = 0
    PAID = 1
    CANCELLED = 2

class Bill(Base):
    pay_time = Column(DateTime, nullable=True)
    total_amount = Column(Integer, nullable=False)
    status = Column(Enum(BillStatus), nullable=False, default=BillStatus.PENDING)
    customer = Column(Integer, ForeignKey(Customer.id), nullable=False, index=True)

class Ticket(Base):
    price = Column(Integer, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False, default=TicketStatus.AVAILABLE, index=True)
    hold_expired_at = Column(DateTime, index=True)
    customer = Column(Integer, ForeignKey(Customer.id), nullable=True, index=True)
    seat = Column(Integer, ForeignKey(Seat.id), nullable=False, index=True)
    screening = Column(Integer, ForeignKey(MovieScreening.id), nullable=False, index=True)
    bill = Column(Integer, ForeignKey(Bill.id), nullable=True)

    __table_args__ = (
        UniqueConstraint('seat', 'screening', name='unique_seat_screening'),
    )

class PaymentStatus(CustomEnum):
    PENDING = 0
    SUCCESS = 1
    FAILED = 2

class Payment(Base):
    bill = Column(Integer, ForeignKey(Bill.id), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_id = Column(String(100), nullable=False, unique=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from datetime import date, datetime

        # ===== 1. Customer =====
        u = Customer(full_name="", email="", phone_number="0123456789", username="123", password="123", birthday=date(2000, 5, 20))
        db.session.add(u)
        db.session.commit()

        # ===== 2. Room + RoomType =====
        room_type = RoomType(name="2D")
        db.session.add(room_type)
        db.session.commit()

        room = Room(room_type=room_type.id, image="room.jpg")
        db.session.add(room)
        db.session.commit()

        # ===== 3. Movie =====
        movie = Movie(
            title="Avengers",
            description="Marvel movie",
            age_limit=13,
            duration=120,
            poster="poster.jpg"
        )
        db.session.add(movie)
        db.session.commit()

        # ===== 4. Screening =====
        from datetime import timedelta
        screening = MovieScreening(
            start_time=datetime.now() + timedelta(hours=2),
            room=room.id,
            movie=movie.id
        )
        db.session.add(screening)
        db.session.commit()

        # ===== 5. Seats =====
        seats = []
        for i in range(1, 6):
            seat = Seat(row="A", number=i, room=room.id)
            seats.append(seat)

        db.session.add_all(seats)
        db.session.commit()

        # ===== 6. HOLD ghế (user chọn ghế) =====
        # ticket1 = Ticket(
        #     price=50000,
        #     status=TicketStatus.HOLDING,
        #     hold_expired_at=datetime.now() + timedelta(minutes=10),
        #     customer=u.id,
        #     seat=seats[0].id,
        #     screening=screening.id
        # )
        #
        # ticket2 = Ticket(
        #     price=50000,
        #     status=TicketStatus.HOLDING,
        #     hold_expired_at=datetime.now() + timedelta(minutes=10),
        #     customer=u.id,
        #     seat=seats[1].id,
        #     screening=screening.id
        # )
        #
        # db.session.add_all([ticket1, ticket2])
        # db.session.commit()

        # ===== 7. Tạo Bill =====
        # bill = Bill(
        #     total_amount=100000,
        #     status=BillStatus.PENDING,
        #     customer=u.id
        # )
        # db.session.add(bill)
        # db.session.commit()

        # ===== 8. Gán ticket vào bill =====
        # ticket1.bill = bill.id
        # ticket2.bill = bill.id
        # db.session.commit()

        # ===== 9. Thanh toán =====
        # payment = Payment(
        #     bill=bill.id,
        #     amount=100000,
        #     transaction_id="TRANS001",
        #     status=PaymentStatus.SUCCESS
        # )
        # db.session.add(payment)

        # update trạng thái
        # bill.status = BillStatus.PAID
        # bill.pay_time = datetime.now()
        #
        # ticket1.status = TicketStatus.PAID
        # ticket2.status = TicketStatus.PAID
        #
        # db.session.commit()

        print("Data created successfully!")




