import hashlib
from sqlalchemy import cast, Date, extract
from app.models import Customer, Seat, RoomType, Movie, MovieTypeDetail, MovieType, MovieScreening, Room, ScreeningSeat, \
    Bill, Payment, UserRole
from app import db
import math
import re


def md5_hash(password: str):
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def add_user(username, password, full_name, phone, email):
    password = md5_hash(password)
    c = Customer(username=username, password=password, full_name=full_name, phone_number=phone, email=email)
    try:
        db.session.add(c)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        raise ex


def auth_user(username, password):
    password = md5_hash(password)
    return Customer.query.filter(Customer.username.__eq__(username), Customer.password.__eq__(password)).first()


def is_username_exists(username):
    return db.session.query(Customer).filter_by(username=username).first() is not None


def is_phone_exists(phone):
    return db.session.query(Customer).filter_by(phone_number=phone).first() is not None


def is_email_exists(email):
    return db.session.query(Customer).filter_by(email=email).first() is not None


def get_user_by_id(customer_id):
    return Customer.query.filter_by(id=customer_id, role=UserRole.CUSTOMER).first()

def get_admin_by_id(admin_id):
    return Customer.query.filter_by(id=admin_id, role=UserRole.ADMIN).first()

def auth_admin(username, password):
    password = md5_hash(password)
    return Customer.query.filter_by(username=username, password=password, role=UserRole.ADMIN).first()




# def get_movies(movie_type_id=None, release_year=None, age_limit=None):
#     query = db.session.query(Movie).all()
#
#     if movie_type_id is not None:
#         query = query(Movie).join(MovieTypeDetail).filter(MovieTypeDetail.movie_type_id == movie_type_id).all()
#     if release_year is not None:
#         query = query.filter(extract('year', Movie.release_date) == release_year).all()
#     if age_limit is not None:
#         query = query.filer(Movie.age_limit >= age_limit).all()
#
#     return query

def get_movie_by_id(movie_id):
    return db.session.query(Movie).filter_by(id=movie_id).first()

def get_movie_types(movie_id):
    return (db.session.query(MovieType)
            .join(MovieTypeDetail, MovieTypeDetail.type_id == MovieType.id)
            .join(Movie, MovieTypeDetail.movie_id == Movie.id)
            .filter(Movie.id == movie_id)
            .limit(3).all())

def get_room_by_type(room_type_id):
    return db.session.query(Room).filter_by(room_type_id=room_type_id).all()

def get_movie_screenings(movie_id, room_id, watch_date):
    return (db.session.query(MovieScreening)
        .join(Room, Room.id==MovieScreening.room_id)
        .join(Movie, Movie.id==MovieScreening.movie_id)
        .filter(MovieScreening.room_id == room_id,
                cast(MovieScreening.start_time, Date) == watch_date,
                MovieScreening.movie_id==movie_id)
        .order_by(MovieScreening.start_time.asc()).all())

def get_seats_by_screening(screening_id):
    return (db.session.query(Seat, ScreeningSeat.status)
        .join(ScreeningSeat, Seat.id == ScreeningSeat.seat_id)
        .join(MovieScreening, MovieScreening.id==ScreeningSeat.screening_id)
        .filter(ScreeningSeat.screening_id == screening_id)
        .order_by(Seat.row, Seat.number).all())

def get_room_types():
    return db.session.query(RoomType).all()

def get_bill(bill_id):
    return db.session.query(Bill).filter_by(id=bill_id).first()

def add_bill(customer_id):
    bill = Bill(customer_id=customer_id)
    db.session.add(bill)
    db.session.commit()

def add_payment(bill_id):
    payment = Payment(bill_id=bill_id)
    db.session.add(payment)
    db.session.commit()

def get_movies(page=1, page_size=8):
    start = (page - 1) * page_size
    # Trả về danh sách phim có phân trang
    return Movie.query.offset(start).limit(page_size).all()

def count_movies():
    return Movie.query.count()
