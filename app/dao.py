import hashlib
from datetime import datetime, timedelta

from flask import current_app
from pymysql import NULL
from sqlalchemy import cast, Date, or_
from app.models import (Customer, UserRole, Seat, RoomType, Movie, MovieTypeDetail, MovieType,
    MovieScreening, Room, ScreeningSeat, Bill, Payment, Ticket, TicketStatus, SeatStatus, PaymentStatus)
from app import db
import re
from datetime import date
from dateutil.relativedelta import relativedelta
import cloudinary.uploader
from sqlalchemy import and_
from flask_mail import Message
from app import mail

def md5_hash(password: str):
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def add_user(username, password, full_name, phone, email, birthday, avatar):
    if birthday and isinstance(birthday, str):
        birthday = date.fromisoformat(birthday)
    if birthday:
        today = date.today()
        age = relativedelta(today, birthday).years
        if age < 13:
            raise ValueError("Bạn phải từ 13 tuổi trở lên để đăng ký tài khoản")

        if age > 100:
            raise ValueError("Ngày sinh không hợp lệ")

    if not birthday:
        raise ValueError("Vui lòng chọn ngày sinh")

    if not re.match(r'^(0)(3|5|7|8|9)\d{8}$', phone):
        raise ValueError("Số điện thoại không hợp lệ")

    if is_phone_exists(phone):
        raise ValueError("Số điện thoại đã được sử dụng")

    if not re.search(r'^\S+@\S+\.\S+$', email) or is_email_exists(email):
        raise ValueError("Không đúng định dạng hoặc email đã tồn tại")

    if len(username) <6:
        raise ValueError("Username phải trên 6 kí tự")

    if is_username_exists(username):
        raise ValueError("Tên đăng nhập đã tồn tại")

    if len(password) < 8:
        raise ValueError("Mật khẩu phải có ít nhất 8 ký tự")

    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
        raise ValueError("Mật khẩu phải có chữ hoa, chữ thường và số")

    password = md5_hash(password)
    c = Customer(username=username, password=password, full_name=full_name, phone_number=phone, email=email, birthday=birthday, avatar=avatar)
    try:
        db.session.add(c)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        raise ex

def auth_user(username, password):
    password = md5_hash(password)
    return db.session.query(Customer).filter(Customer.username.__eq__(username), Customer.password.__eq__(password)).first()

def is_username_exists(username):
    return db.session.query(Customer).filter_by(username=username).first() is not None

def is_phone_exists(phone):
    return db.session.query(Customer).filter_by(phone_number=phone).first() is not None

def is_email_exists(email):
    return db.session.query(Customer).filter_by(email=email).first() is not None

def get_user_by_id(customer_id):
    return db.session.query(Customer).filter_by(id=customer_id, role=UserRole.CUSTOMER).first()

def get_admin_by_id(admin_id):
    return db.session.query(Customer).filter_by(id=admin_id, role=UserRole.ADMIN).first()

def auth_admin(username, password):
    password = md5_hash(password)
    return db.session.query(Customer).query.filter_by(username=username, password=password, role=UserRole.ADMIN).first()

def get_movie_by_id(movie_id):
    return db.session.query(Movie).filter_by(id=movie_id).first()

def get_movie_types(movie_id):
    return (db.session.query(MovieType)
            .join(MovieTypeDetail, MovieTypeDetail.type_id == MovieType.id)
            .filter(MovieTypeDetail.movie_id == movie_id)
            .all())

def get_room_types():
    return db.session.query(RoomType).all()

def get_room_by_type(room_type_id):
    return db.session.query(Room).filter_by(room_type_id=room_type_id).all()

def get_movie_screenings(movie_id, room_id, watch_date):
    start = datetime.combine(watch_date, datetime.min.time())
    end = start + timedelta(days=1)
    return (db.session.query(MovieScreening)
        .filter(MovieScreening.room_id == room_id,
                MovieScreening.movie_id == movie_id,
                MovieScreening.start_time >= start,
                MovieScreening.start_time < end,
                MovieScreening.start_time >= datetime.now())
        .order_by(MovieScreening.start_time.asc()).all())

def get_seats_by_screening(screening_id):
    return (db.session.query(Seat, ScreeningSeat.status)
        .join(ScreeningSeat, Seat.id == ScreeningSeat.seat_id)
        .filter(ScreeningSeat.screening_id == screening_id)
        .order_by(Seat.row, Seat.number)
        .all())

def hold_seats(seat_ids, screening_id):
    if (len(seat_ids) <= 0 or len(seat_ids) > 8):
        raise Exception("Số lượng ghế không hợp lệ!")

    return db.session.query(ScreeningSeat).filter(
        ScreeningSeat.seat_id.in_(seat_ids),
        ScreeningSeat.screening_id == screening_id
    ).with_for_update().all()

def total_seat_per_screening(screening_id, user_id):
    return db.session.query(ScreeningSeat).filter(
        ScreeningSeat.screening_id == screening_id,
        ScreeningSeat.holding_user_id == user_id,
        or_(
            ScreeningSeat.status == SeatStatus.BOOKED,
            and_(ScreeningSeat.status == SeatStatus.HOLDING, ScreeningSeat.hold_expired_at > datetime.now())
        )
    ).count()

def get_bill_by_id(bill_id):
    return db.session.query(Bill).filter_by(id=bill_id).first()

def add_bill(customer_id, total=0):
    bill = Bill(customer_id=customer_id, total_amount=total)
    db.session.add(bill)
    db.session.flush()
    return bill

def add_ticket(bill_id, ss_id, price):
    ticket = Ticket(bill_id=bill_id, screening_seat_id=ss_id, price=price)
    db.session.add(ticket)
    db.session.commit()

def add_payment(bill_id, amount, txn_ref):
    payment = Payment(bill_id=bill_id, amount=amount, txn_ref=txn_ref)
    db.session.add(payment)
    db.session.commit()
    return payment

def get_movies(page=1, page_size=8):
    start = (page - 1) * page_size
    return db.session.query(Movie).offset(start).limit(page_size).all()

def count_movies():
    return db.session.query(Movie).count()

def pay_fail(payment, bill):
    payment.status = PaymentStatus.FAILED
    bill.status = PaymentStatus.FAILED
    bill.pay_time = datetime.now()

    for ticket in bill.tickets:
        ticket.status = TicketStatus.CANCELLED
        ticket.screening_seat.status = SeatStatus.AVAILABLE
        ticket.screening_seat.holding_user = NULL
        ticket.screening_seat.hold_expired_at = NULL

    db.session.commit()

def pay_success(payment, bill):
    payment.status = PaymentStatus.SUCCESS
    bill.status = PaymentStatus.SUCCESS
    bill.pay_time = datetime.now()

    for ticket in bill.tickets:
        ticket.status = TicketStatus.PAID
        ticket.screening_seat.status = SeatStatus.BOOKED

    db.session.commit()


def get_info_movie(customer_id):
    results = db.session.query(Ticket.id,Movie.title,MovieScreening.start_time,Room.number,Seat.row,Seat.number,
        Ticket.price,Ticket.status
    ).join(ScreeningSeat, Ticket.screening_seat_id == ScreeningSeat.id)\
     .join(Seat, ScreeningSeat.seat_id == Seat.id)\
     .join(Room, Seat.room_id == Room.id)\
     .join(MovieScreening, ScreeningSeat.screening_id == MovieScreening.id)\
     .join(Movie, MovieScreening.movie_id == Movie.id)\
     .join(Bill, Ticket.bill_id == Bill.id)\
     .filter(Bill.customer_id == customer_id,
             Ticket.status == TicketStatus.USED).all()

    watched_list = []
    for r in results:
        watched_list.append({
            'id': r[0],
            'movie_name': r[1],
            'show_time': r[2].strftime('%H:%M - %d/%m/%Y'),
            'room_number': r[3],
            'seat_number': f"{r[4]}{r[5]}",
            'price': r[6],
            'status': r[7]
        })
    return watched_list
def get_customer_by_email(email):
    return db.session.query(Customer).filter(Customer.email == email.strip()).first()

def send_reset_email(user_email, otp_code):
    msg = Message(
        subject='Mã xác nhận đặt lại mật khẩu',
        recipients=[user_email]
    )
    msg.body = f"Mã OTP của bạn là: {otp_code}. Vui lòng không chia sẻ mã này cho bất kỳ ai."

    try:
        with current_app.app_context():
            mail.send(msg)
        return True
    except Exception as e:
        print(f"Lỗi gửi mail: {e}")
        return False


def update_password(customer_id, new_password):
    customer = db.session.query(Customer).get(customer_id)
    if len(new_password) < 8:
        raise ValueError("Mật khẩu phải có ít nhất 8 ký tự")
    if not re.search(r'[A-Z]', new_password) or not re.search(r'\d', new_password):
        raise ValueError("Mật khẩu phải có chữ hoa và số")
    if customer:
        password_hashed = md5_hash(new_password)
        customer.password = password_hashed
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    return False
