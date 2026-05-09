import os
import platform
import threading
import time

from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from app import db
import pytest
import hashlib
from datetime import datetime, timedelta
from app.models import *
from datetime import date
from app import mail as flask_mail


def create_app(db_uri=None):
    test_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.abspath(os.path.join(test_dir, '..', '..'))

    app = Flask(
        __name__,
        root_path=os.path.join(app_dir, 'app'),
        template_folder=os.path.join(app_dir, 'app', 'templates'),
        static_folder=os.path.join(app_dir, 'app', 'static')
    )

    if db_uri is None:
        db_uri = "sqlite:///:memory:"

    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=True,
        MAIL_SUPPRESS_SEND=True,
        MAIL_DEFAULT_SENDER='test@example.com',
        SECRET_KEY='sjkfksgfghsvhvagjdhaldg',
        WTF_CSRF_ENABLED=False
    )

    from app import db, mail, login
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
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
def sample_screening(test_session):
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
def sample_screening_seats(test_session, sample_seats):
    ss_list = []

    for i, seat in enumerate(sample_seats):
        is_first = (i == 0)
        ss = ScreeningSeat(
            seat_id=seat.id,
            screening_id=1,
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
    return [bill]

@pytest.fixture
def sample_tickets(test_session, sample_screening_seats, sample_bill):
    t1 = Ticket(
        price=100000,
        status=TicketStatus.PAID,
        screening_seat_id=sample_screening_seats[0].id,
        bill_id=sample_bill[0].id
    )

    t2 = Ticket(
        price=100000,
        status=TicketStatus.PAID,
        screening_seat_id=sample_screening_seats[1].id,
        bill_id=sample_bill[0].id
    )

    t3 = Ticket(
        price=100000,
        status=TicketStatus.USED,
        screening_seat_id=sample_screening_seats[2].id,
        bill_id=sample_bill[0].id
    )

    t4 = Ticket(
        price=100000,
        status=TicketStatus.CANCELLED,
        screening_seat_id=sample_screening_seats[3].id,
        bill_id=sample_bill[0].id
    )
    test_session.add_all([t1,t2, t3,t4])
    test_session.commit()
    return [t1,t2, t3,t4]

@pytest.fixture
def sample_payment(test_session, sample_bill):
    payment = Payment(
        bill_id=sample_bill[0].id,
        amount=100000,
        status=PaymentStatus.PENDING,
        txn_ref="TEST123"
    )

    test_session.add(payment)
    test_session.commit()
    return payment

@pytest.fixture(scope="session")
def sel_app():
    if os.getenv('GITHUB_ACTIONS'):
        uri = "mysql+pymysql://root:root@127.0.0.1:3306/cinemadb"
    else:
        uri = "sqlite:///selenium_test.db"

    app = create_app(db_uri=uri)

    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()

    def run_app():
        app.run(host='0.0.0.0', port=5005, debug=False, use_reloader=False)

    server_thread = threading.Thread(target=run_app, daemon=True)
    server_thread.start()
    time.sleep(5)

    yield app
    if not os.getenv('GITHUB_ACTIONS') and os.path.exists("selenium_test.db"):
        os.remove("selenium_test.db")

@pytest.fixture()
def driver(sel_app):
    options = Options()

    if os.getenv('GITHUB_ACTIONS'):
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    options.add_argument("--disable-features=SafeBrowsingPasswordCheck")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "autofill.profile_enabled": False,
        "password_manager_leak_detection": False,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
