from tkinter.constants import CASCADE

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
    room_type_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)
    number = Column(Integer, nullable=False, unique=True)
    image = Column(String(200), nullable=False)

class SeatStatus(CustomEnum):
    AVAILABLE = 0
    HOLDING = 1
    BOOKED = 2

class Seat(Base):
    row = Column(String(5), nullable=False)
    number = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('room_id', 'row', 'number', name='unique_seat_room'),
    )

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

class MovieTypeDetail(Base):
    type_id = Column(Integer, ForeignKey(MovieType.id), nullable=False)
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('type_id', 'movie_id', name='unique_movie_type'),
    )

class MovieScreening(Base):
    start_time = Column(DateTime, nullable=False)
    base_price = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('room_id', 'start_time', name='unique_room_time'),
    )

class ScreeningSeat(Base):
    seat_id = Column(Integer, ForeignKey(Seat.id), nullable=False, index=True)
    screening_id = Column(Integer, ForeignKey(MovieScreening.id), nullable=False, index=True)
    status = Column(Enum(SeatStatus), default=SeatStatus.AVAILABLE, index=True)
    hold_expired_at = Column(DateTime, index=True)

    seat = relationship("Seat", backref="screening_seat",lazy=True)
    screening = relationship("MovieScreening", backref="screening_seat",lazy=True)

    __table_args__ = (
        UniqueConstraint('seat_id', 'screening_id', name='unique_seat_screening'),
    )

class PaymentStatus(CustomEnum):
    PENDING = 1
    SUCCESS = 2
    FAILED = 2

class Bill(Base):
    pay_time = Column(DateTime, nullable=True)
    total_amount = Column(Integer, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False, index=True)

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

class Payment(Base):
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_id = Column(String(100), nullable=False, unique=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("DB created successfully!")

        # 1. Tạo Thể loại phim
        t1 = MovieType(name="Hành động")
        t2 = MovieType(name="Tình cảm")
        t3 = MovieType(name="Khoa học viễn tưởng")
        # db.session.add_all([t1, t2, t3])
        # db.session.commit()

        # 2. Tạo Phim
        from datetime import datetime, date, timedelta
        m1 = Movie(
            title="Dune: Hành Tinh Cát",
            description="Câu chuyện về Paul Atreides trong cuộc chiến giành quyền lực.",
            age_limit=13,
            duration=155,
            poster="https://image.tmdb.org/t/p/original/d5NXSklZfs7Z1o2m9gH9D8M6S3p.jpg",
            release_date=date(2024, 3, 1)
        )
        # db.session.add(m1)
        # db.session.commit()

        # Gán thể loại cho phim
        # db.session.add(MovieTypeDetail(type_id=t1.id, movie_id=m1.id))
        # db.session.add(MovieTypeDetail(type_id=t3.id, movie_id=m1.id))

        # 3. Tạo Loại phòng và Phòng
        rt_standard = RoomType(name="Standard")
        rt_imax = RoomType(name="IMAX")
        # db.session.add_all([rt_standard, rt_imax])
        # db.session.commit()

        r1 = Room(room_type_id=rt_imax.id, number=101, image="room1.jpg")
        # db.session.add(r1)
        # db.session.commit()

        # # 4. Tạo Ghế cho Phòng 1 (Vẽ sơ đồ 5 hàng x 5 cột)
        rows = ['A', 'B', 'C', 'D', 'E']
        seats = []
        for r in rows:
            for n in range(1, 6):
                s = Seat(row=r, number=n, room_id=1)
                seats.append(s)
        # db.session.add_all(seats)
        # db.session.commit()

        # # 5. Tạo Suất chiếu (MovieScreening)
        # Suất chiếu vào 19:00 tối nay
        screening_time = datetime.now().replace(hour=19, minute=0, second=0, microsecond=0)
        ms1 = MovieScreening(
            start_time=screening_time,
            base_price=95000,
            room_id=1,
            movie_id=1
        )
        # db.session.add(ms1)
        # db.session.commit()

        # # 6. Tạo ScreeningSeat (Quan trọng nhất để hiện sơ đồ ghế khi đặt vé)
        all_seats = Seat.query.filter_by(room_id=r1.id).all()
        for seat in all_seats:
            ss = ScreeningSeat(
                seat_id=seat.id,
                screening_id=ms1.id,
                status=SeatStatus.AVAILABLE
            )
            # Giả lập 2 ghế đã có người đặt (BOOKED)
            if seat.row == 'C' and seat.number in [3, 4]:
                ss.status = SeatStatus.BOOKED
        #     db.session.add(ss)
        # db.session.commit()

        seats = Seat.query.filter(Seat.room_id.in_([1, 2])).all()
        for seat in seats:
            ss = ScreeningSeat(
                seat_id=seat.id,
                screening_id=5
            )
        #     db.session.add(ss)
        #
        # db.session.commit()

        print("Data was imported successfully!")




