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
        return f"{self.full_name}"

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
    type_id = Column(Integer, ForeignKey(MovieType.id), nullable=False)
    movie_id = Column(Integer, ForeignKey(Movie.id), nullable=False)

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
        db.drop_all()
        db.create_all()
        print("DB created successfully!")

        #Tạo admin

        import hashlib
        admin = Customer(
            full_name = "Admin",
            username='admin',
            password=hashlib.md5("123".encode("utf-8")).hexdigest(),
            email='admin@gmail.com',
            phone_number='0357899304',
            role=UserRole.ADMIN
        )
        db.session.add(admin)
        db.session.commit()

        # 1. Tạo Thể loại phim
        t1 = MovieType(name="Hành động")
        t2 = MovieType(name="Tình cảm")
        t3 = MovieType(name="Khoa học viễn tưởng")
        db.session.add_all([t1, t2, t3])
        db.session.commit()

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
        db.session.add(m1)
        db.session.commit()

        # ===== 3. Movie =====
        movies = [
            # --- PHIM VIỆT NAM ---
            {
                "title": "Mai",
                "description": "Phim tâm lý tình cảm của Trấn Thành, xoay quanh cuộc đời của người phụ nữ tên Mai.",
                "age_limit": 18,
                "duration": 131,
                "poster": "https://upload.wikimedia.org/wikipedia/vi/3/36/Mai_2024_poster.jpg",
                "release_date": "2019-04-26"
            },
            {
                "title": "Mai 2",
                "description": "Phim tâm lý tình cảm của Trấn Thành, xoay quanh cuộc đời của người phụ nữ tên Mai.",
                "age_limit": 18,
                "duration": 131,
               "poster": "https://upload.wikimedia.org/wikipedia/vi/3/36/Mai_2024_poster.jpg",
                "release_date": "2019-04-26"

            },
            {
                "title": "Mai 3",
                "description": "Phim tâm lý tình cảm của Trấn Thành, xoay quanh cuộc đời của người phụ nữ tên Mai.",
                "age_limit": 18,
                "duration": 131,
               "poster": "https://upload.wikimedia.org/wikipedia/vi/3/36/Mai_2024_poster.jpg",
                "release_date": "2019-04-26"
            },
            {
                "title": "Mai 4",
                "description": "Phim tâm lý tình cảm của Trấn Thành, xoay quanh cuộc đời của người phụ nữ tên Mai.",
                "age_limit": 18,
                "duration": 131,
               "poster": "https://upload.wikimedia.org/wikipedia/vi/3/36/Mai_2024_poster.jpg",
                "release_date": "2019-04-26"
            },
            {
                "title": "Mai 5",
                "description": "Phim tâm lý tình cảm của Trấn Thành, xoay quanh cuộc đời của người phụ nữ tên Mai.",
                "age_limit": 18,
                "duration": 131,
               "poster": "https://upload.wikimedia.org/wikipedia/vi/3/36/Mai_2024_poster.jpg",
                "release_date": "2019-04-26"
            },
            {
                "title": "Mai 6",
                "description": "Phim tâm lý tình cảm của Trấn Thành, xoay quanh cuộc đời của người phụ nữ tên Mai.",
                "age_limit": 18,
                "duration": 131,
               "poster": "https://upload.wikimedia.org/wikipedia/vi/3/36/Mai_2024_poster.jpg",
                "release_date": "2019-04-26"
            },
            {
                "title": "Mai 7",
                "description": "Phim tâm lý tình cảm của Trấn Thành, xoay quanh cuộc đời của người phụ nữ tên Mai.",
                "age_limit": 18,
                "duration": 131,
              "poster": "https://upload.wikimedia.org/wikipedia/vi/3/36/Mai_2024_poster.jpg",
                "release_date": "2019-04-26"
            }

        ]
        for m in movies:
            movie = Movie(**m)
            db.session.add(movie)

        db.session.commit()

        # Gán thể loại cho phim
        db.session.add(MovieTypeDetail(type_id=1, movie_id=1))
        db.session.add(MovieTypeDetail(type_id=3, movie_id=1))
        db.session.add(MovieTypeDetail(type_id=2, movie_id=2))
        db.session.add(MovieTypeDetail(type_id=3, movie_id=2))
        # 3. Tạo Loại phòng và Phòng
        rt_standard = RoomType(name="Standard")
        rt_imax = RoomType(name="IMAX")
        db.session.add_all([rt_standard, rt_imax])
        db.session.commit()

        r1 = Room(room_type_id=1, number=101, image="room1.jpg")
        db.session.add(r1)
        db.session.commit()

        # # 4. Tạo Ghế cho Phòng 1 (Vẽ sơ đồ 5 hàng x 5 cột)
        rows = ['A', 'B', 'C', 'D', 'E']
        seats = []
        for r in rows:
            for n in range(1, 6):
                s = Seat(row=r, number=n, room_id=1)
                seats.append(s)
        db.session.add_all(seats)
        db.session.commit()

        # # 5. Tạo Suất chiếu (MovieScreening)
        # Suất chiếu vào 19:00 tối nay
        screening_time = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
        ms1 = MovieScreening(
            start_time=screening_time,
            base_price=95000,
            room_id=1,
            movie_id=1
        )
        db.session.add(ms1)
        db.session.commit()

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
            db.session.add(ss)
        db.session.commit()

        # seats = Seat.query.filter(Seat.room_id.in_([1, 2])).all()
        # for seat in seats:
        #     ss = ScreeningSeat(
        #         seat_id=seat.id,
        #         screening_id=1
        #     )
        #     db.session.add(ss)
        #
        # db.session.commit()
        # 8. HISTORY_TICKET
        user_test = Customer.query.filter_by(username='khach_test').first()
        if not user_test:
            user_test = Customer(
                full_name="Nguyễn Văn T",
                email="test_all@gmail.com",
                phone_number="0944555666",
                username="khach_test",
                password=hashlib.md5("123".encode("utf-8")).hexdigest(),
                role=UserRole.CUSTOMER
            )
            db.session.add(user_test)
            db.session.commit()

        bill_test = Bill(
            total_amount=190000,
            status=PaymentStatus.SUCCESS,
            customer_id=user_test.id,
            pay_time=datetime.now()
        )
        db.session.add(bill_test)
        db.session.commit()
        seats_to_book = ScreeningSeat.query.filter_by(
            screening_id=ms1.id,
            status=SeatStatus.AVAILABLE
        ).limit(2).all()

        if len(seats_to_book) >= 2:
            seats_to_book[0].status = SeatStatus.BOOKED
            ticket_paid = Ticket(
                price=95000,
                status=TicketStatus.PAID,
                screening_seat_id=seats_to_book[0].id,
                bill_id=bill_test.id
            )
            db.session.add(ticket_paid)
            seats_to_book[1].status = SeatStatus.BOOKED
            ticket_used = Ticket(
                price=95000,
                status=TicketStatus.USED,
                screening_seat_id=seats_to_book[1].id,
                bill_id=bill_test.id
            )
            db.session.add(ticket_used)
            db.session.commit()

        print("Data was imported successfully!")
