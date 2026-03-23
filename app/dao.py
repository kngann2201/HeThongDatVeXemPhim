import hashlib
from models import Customer
from app import db
import re

def md5_hash(password: str):
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def add_user(username, password, full_name, phone, email):
    password = md5_hash(password)
    c = Customer(username=username, password=password,full_name=full_name, phone_number=phone, email=email)
    try:
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
    return db.session.query(Customer).filter_by(phone_number=phone).first() is not None

def is_email_exists(email):
    return db.session.query(Customer).filter_by(email=email).first() is not None

def get_user_by_id(customer_id):
    return Customer.query.get(customer_id)