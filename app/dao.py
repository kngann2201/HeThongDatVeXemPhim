import hashlib
from models import Customer
from app import db

def md5_hash(password: str):
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def add_user(username, password, avatar, full_name, phone, email=None):
    password = md5_hash(password)
    u = Customer(username=username, password=password, avatar=avatar)
    c = Customer(full_name=full_name, phone=phone, email=email, user=u)
    try:
        db.session.add(u)
        db.session.add(c)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        raise ex

def auth_user(username,password):
    password = md5_hash(password)
    return Customer.query.filter(Customer.username.__eq__(username), Customer.password.__eq__(password)).first()

def is_username_exists(username):
    return db.session.query(Customer).filter_by(username=username).first() is not None

def is_phone_exists(phone):
    return db.session.query(Customer).filter_by(phone=phone).first() is not None