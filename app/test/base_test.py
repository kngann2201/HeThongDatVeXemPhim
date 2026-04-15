import os
from flask import Flask
from app import db, dao, app, mail, login
import pytest
import hashlib
from datetime import datetime, timedelta
from app.models import Movie, MovieType, RoomType, Room, MovieTypeDetail, Customer, UserRole, Seat, MovieScreening, \
    ScreeningSeat, SeatStatus, Bill, PaymentStatus, Ticket, TicketStatus, Payment
from datetime import date
from flask_mail import Mail
from app import mail as flask_mail 


def create_app():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.abspath(os.path.join(test_dir, '..', '..'))

    app = Flask(
        __name__,
        root_path=os.path.join(app_dir, 'app'),
        template_folder=os.path.join(app_dir, 'app', 'templates'),
        static_folder=os.path.join(app_dir, 'app', 'static')
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'

    app.config["TESTING"] = True
    app.secret_key = 'sjkfksgfghsvhvagjdhaldg'
    db.init_app(app)
    flask_mail.init_app(app)
    from flask_login import LoginManager
    login.init_app(app)


    from app.index import register_app
    register_app(app)

    return app


@pytest.fixture
def test_app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_mail_object():
    return flask_mail

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()

@pytest.fixture
def sample_movie(test_session):
    m1 = Movie(
        title="Dune: Hành Tinh Cát",
        description="Câu chuyện về Paul Atreides trong cuộc chiến giành quyền lực.",
        age_limit=13,
        duration=155,
        poster="image.png",
        release_date=date(2024, 3, 1)
    )
    m2 = Movie(
        title="Inception",
        description="Dom Cobb là một kẻ chuyên đánh cắp bí mật từ tiềm thức của người khác khi họ đang ngủ. Anh được trao cơ hội chuộc lại quá khứ bằng cách thực hiện một nhiệm vụ gần như bất khả thi. Thay vì đánh cắp ý tưởng, lần này anh phải cấy một ý tưởng vào tâm trí mục tiêu. Kế hoạch trở nên phức tạp khi các tầng giấc mơ chồng chéo lên nhau. Mọi thứ dần vượt khỏi tầm kiểm soát khi quá khứ của Cobb quay lại ám ảnh anh.",
        age_limit=13,
        duration=148,
        poster="inception.png",
        release_date=date(2010, 7, 16)
    )
    m3 = Movie(
        title="The Dark Knight",
        description="Batman tiếp tục cuộc chiến chống lại tội phạm tại Gotham cùng với cảnh sát và công tố viên Harvey Dent. Một kẻ thù mới xuất hiện, Joker, mang đến sự hỗn loạn chưa từng có. Hắn không chỉ gây rối mà còn thách thức các nguyên tắc đạo đức của Batman. Thành phố dần rơi vào trạng thái hỗn loạn khi Joker thực hiện những kế hoạch tàn bạo. Batman buộc phải đối mặt với những lựa chọn khó khăn để bảo vệ Gotham.",
        age_limit=16,
        duration=152,
        poster="the_dark_knight.png",
        release_date=date(2008, 7, 18)
    )
    test_session.add_all([m1, m2, m3])
    test_session.commit()
    return [m1, m2, m3]

@pytest.fixture
def sample_movie_type(test_session):
    t1 = MovieType(name="Hành động")
    t2 = MovieType(name="Tình cảm")
    t3 = MovieType(name="Khoa học viễn tưởng")
    test_session.add_all([t1, t2, t3])
    test_session.commit()
    return [t1, t2, t3]

@pytest.fixture
def sample_movie_type_detail(test_session):
    td1 = MovieTypeDetail(movie_id=1, type_id=1)
    td2 = MovieTypeDetail(movie_id=1, type_id=2)
    td3 = MovieTypeDetail(movie_id=3, type_id=2)
    test_session.add_all([td1, td2, td3])
    test_session.commit()
    return [td1, td2, td3]

@pytest.fixture
def sample_room_type(test_session):
    rt1 = RoomType(name="Standard")
    rt2 = RoomType(name="IMAX")
    rt3 = RoomType(name="VIP")
    test_session.add_all([rt1, rt2, rt3])
    test_session.commit()
    return [rt1, rt2, rt3]

@pytest.fixture
def sample_room(test_session):
    r1 = Room(room_type_id=1, number=101, image="room1_1.jpg")
    r2 = Room(room_type_id=1, number=102, image="room1_2.jpg")
    r3 = Room(room_type_id=2, number=201, image="room2_1.jpg")
    test_session.add_all([r1, r2, r3])
    test_session.commit()
    return [r1, r2, r3]

@pytest.fixture
def mock_cloudinary(monkeypatch):
    def fake_upload(file):
        return {'secure_url': 'https://fake-avartar.png'}

    monkeypatch.setattr('cloudinary.uploader.upload',fake_upload)

@pytest.fixture
def sample_users(test_session):
    u1 = Customer(
        full_name="User 1",
        username="user1",
        password=hashlib.md5("Pass@123".encode()).hexdigest(),
        email="user1@gmail.com",
        phone_number="0123456789",
        role=UserRole.CUSTOMER
    )

    admin = Customer(
        full_name="Admin",
        username="admin",
        password=hashlib.md5("123".encode()).hexdigest(),
        email="admin@gmail.com",
        phone_number="0999999999",
        role=UserRole.ADMIN
    )

    test_session.add_all([u1, admin])
    test_session.commit()
    return [u1, admin]

@pytest.fixture
def sample_seats(test_session, sample_room):
    seats = []
    rows = ['A', 'B']

    for r in rows:
        for n in range(1, 9):
            s = Seat(row=r, number=n, room_id=sample_room[0].id)
            seats.append(s)

    test_session.add_all(seats)
    test_session.commit()
    return seats

@pytest.fixture
def sample_screening(test_session, sample_movie, sample_room):
    scr1 = MovieScreening(
        start_time=datetime.now() + timedelta(days=1),
        base_price=100000,
        room_id=1,
        movie_id=1
    )
    scr2 = MovieScreening(
        start_time=datetime.now() - timedelta(days=1),
        base_price=100000,
        room_id=1,
        movie_id=1
    )
    scr3 = MovieScreening(
        start_time=datetime.now() + timedelta(minutes=2),
        base_price=100000,
        room_id=1,
        movie_id=1
    )
    scr4 = MovieScreening(
        start_time=datetime.now() - timedelta(minutes=1),
        base_price=100000,
        room_id=1,
        movie_id=1
    )

    test_session.add_all([scr1, scr2, scr3, scr4])
    test_session.commit()
    return [scr1, scr2, scr3, scr4]

@pytest.fixture
def sample_screening_seats(test_session, sample_seats, sample_screening):
    ss_list = []

    for i, seat in enumerate(sample_seats):
        is_first = (i == 0)
        ss = ScreeningSeat(
            seat_id=seat.id,
            screening_id=sample_screening[0].id,
            status=SeatStatus.BOOKED if is_first else SeatStatus.AVAILABLE,
            holding_user_id=1 if is_first else None
        )
        ss_list.append(ss)

    test_session.add_all(ss_list)
    test_session.commit()
    return ss_list

@pytest.fixture
def sample_bill(test_session):
    bill = Bill(
        total_amount=100000,
        status=PaymentStatus.PENDING,
        customer_id=1
    )

    test_session.add(bill)
    test_session.commit()
    return bill

@pytest.fixture
def sample_tickets(test_session, sample_screening_seats, sample_bill):
    t = Ticket(
        price=100000,
        status=TicketStatus.PAID,
        screening_seat_id=1,
        bill_id=sample_bill[0].id
    )

    test_session.add(t)
    test_session.commit()
    return [t]

@pytest.fixture
def sample_payment(test_session, sample_bill):
    payment = Payment(
        bill_id=sample_bill.id,
        amount=100000,
        status=PaymentStatus.PENDING,
        txn_ref="TEST123"
    )

    test_session.add(payment)
    test_session.commit()
    return payment
