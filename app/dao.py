import hashlib
from datetime import datetime, timedelta

from flask import current_app
from sqlalchemy import cast, Date, or_, func
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
    return db.session.query(Customer).filter_by(username=username, password=password, role=UserRole.ADMIN).first()

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
    watch_date = datetime.strptime(str(watch_date), "%Y-%m-%d").date()
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

def get_screening_by_id(screening_id):
    return db.session.query(MovieScreening).filter_by(screening_id=screening_id).first()

def get_bill_by_id(bill_id):
    return db.session.query(Bill).filter_by(id=bill_id).first()

def get_payment_by_bill_id(bill_id):
    return db.session.query(Payment).filter_by(bill_id=bill_id).first()

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

def get_movies(keyword=None):
    query = db.session.query(Movie)
    if keyword:
        query = query.filter(Movie.title.contains(keyword))
    movies = query.order_by(Movie.id.desc()).all()

    results = []
    for m in movies:
        genres_list = [detail.type.name for detail in m.movie_type_details]

        results.append({
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'poster': m.poster,
            'genres': ", ".join(genres_list) if genres_list else "Đang cập nhật"
        })

    return results

def count_movies():
    return db.session.query(Movie).count()

def ticket_count_by_movie_id(movie_id):
    ticket_count = (
        db.session.query(func.count(Ticket.id))
        .join(ScreeningSeat, Ticket.screening_seat_id == ScreeningSeat.id)
        .join(MovieScreening, ScreeningSeat.screening_id == MovieScreening.id)
        .filter(MovieScreening.movie_id == movie_id, Ticket.status != TicketStatus.CANCELLED)
    ).scalar()
    return ticket_count

def pay_fail(payment, bill):
    payment.status = PaymentStatus.FAILED
    db.session.commit()

def pay_success(payment, bill):
    payment.status = PaymentStatus.SUCCESS
    bill.status = PaymentStatus.SUCCESS
    bill.pay_time = datetime.now()

    for ticket in bill.tickets:
        ticket.status = TicketStatus.PAID
        ticket.screening_seat.status = SeatStatus.BOOKED

    db.session.commit()

def get_info_movie(customer_id, status_enum):
    target_statuses = [status_enum]
    if status_enum == TicketStatus.PAID:
        target_statuses.append(TicketStatus.CANCELLED)

    results = db.session.query(
        Ticket.id, Movie.title, MovieScreening.start_time,
        Room.number, Seat.row, Seat.number,
        Ticket.price, Ticket.status
    ).join(ScreeningSeat, Ticket.screening_seat_id == ScreeningSeat.id)\
     .join(Seat, ScreeningSeat.seat_id == Seat.id)\
     .join(Room, Seat.room_id == Room.id)\
     .join(MovieScreening, ScreeningSeat.screening_id == MovieScreening.id)\
     .join(Movie, MovieScreening.movie_id == Movie.id)\
     .join(Bill, Ticket.bill_id == Bill.id)\
     .filter(
         Bill.customer_id == customer_id,
         Ticket.status.in_(target_statuses)
     ).all()

    ticket_list = []
    for r in results:
        ticket_list.append({
            'id': r[0],
            'movie_name': r[1],
            'show_time': r[2].strftime('%H:%M - %d/%m/%Y'),
            'room_number': r[3],
            'seat_number': f"{r[4]}{r[5]}",
            'price': r[6],
            'status': r[7].name
        })
    return ticket_list

def get_all_info_movie(customer_id):
    results = db.session.query(Ticket.id,Movie.title,MovieScreening.start_time,Room.number,Seat.row,Seat.number,
        Ticket.price,Ticket.status, Bill.id
    ).join(ScreeningSeat, Ticket.screening_seat_id == ScreeningSeat.id)\
     .join(Seat, ScreeningSeat.seat_id == Seat.id)\
     .join(Room, Seat.room_id == Room.id)\
     .join(MovieScreening, ScreeningSeat.screening_id == MovieScreening.id)\
     .join(Movie, MovieScreening.movie_id == Movie.id)\
     .join(Bill, Ticket.bill_id == Bill.id)\
     .filter(Bill.customer_id == customer_id).all()

    watched_list = []
    for r in results:
        watched_list.append({
            'id': r[0],
            'movie_name': r[1],
            'show_time': r[2].strftime('%H:%M - %d/%m/%Y'),
            'room_number': r[3],
            'seat_number': f"{r[4]}{r[5]}",
            'price': r[6],
            'status': r[7],
            'bill_id': r[8]
        })
    return watched_list

def get_customer_by_email(email):
    return db.session.query(Customer).filter(Customer.email == email.strip()).first()


# app/dao.py
def send_reset_email(user_email, otp_code):
    from flask_mail import Message
    from app import mail

    msg = Message(
        subject='Mã xác nhận đặt lại mật khẩu',
        recipients=[user_email]
    )
    msg.body = f"Mã OTP của bạn là: {otp_code}."

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Lỗi gửi mail: {e}")
        return False

def update_password(customer_id, new_password):
    customer = db.session.get(Customer, customer_id)
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

def cancel_ticket(ticket_id, customer_id):
    ticket = Ticket.query.join(Bill).filter(
        Ticket.id == ticket_id,
        Bill.customer_id == customer_id
    ).first()

    if not ticket:
        raise ValueError("Không tìm thấy vé hoặc bạn không có quyền hủy vé này!")

    if ticket.status == TicketStatus.USED:
        raise ValueError("Vé đã check-in và sử dụng, không thể hủy!")

    if ticket.status == TicketStatus.CANCELLED:
        raise ValueError("Vé đã hủy!")

    screening = ticket.screening_seat.screening
    now = datetime.now()

    if screening.start_time - now < timedelta(hours=2):
        raise ValueError("Quá hạn hủy vé! Chỉ được hủy trước suất chiếu ít nhất 2 tiếng.")

    try:
        ticket.status = TicketStatus.CANCELLED

        s_seat = ticket.screening_seat
        s_seat.status = SeatStatus.AVAILABLE
        s_seat.holding_user_id = None
        s_seat.hold_expired_at = None

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Lỗi hệ thống khi hủy vé: {str(e)}")