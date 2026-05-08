from app.dao import add_user
from app.test.base_test import test_session, test_app, mock_cloudinary
import hashlib
import pytest
from app.models import Customer
from datetime import datetime

def test_success(test_app, test_session):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()

    with test_app.app_context():
        add_user(username='a1' * 4, password='Abcd123@', full_name='admin',
                 phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)

        u = Customer.query.filter(Customer.username == 'a1' * 4).first()
        assert u is not None
        assert u.full_name == 'admin'
        assert u.password == hashlib.md5('Abcd123@'.encode('utf-8')).hexdigest()
        assert u.username == 'a1'*4
        assert u.phone_number == '0323456789'
        assert u.birthday == birthday_obj
        assert u.email == 'admin123@gmail.com'
        assert u.avatar=='https://res.cloudinary.com/dkzxdp1gi/image/upload/v1767843265/avatar-trang-nu-001_dym4n0.webp'


@pytest.mark.parametrize('password', [
    '1' * 7, '1a' * 3 + 'A','@'*7,'Ab1'*2+'@',
    'A1' * 4, 'Aa' * 4, 'a1' * 4,'1@'*4,'a@'*4,'@A'*4,'Ha11'*4,'Aau@'*2,'@a1a'*2,'@AA1'*2,
    '1' * 8, 'a' * 8, 'A' * 8,'@'*8
])
def test_invalid_password(test_app, password):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()

    with test_app.app_context():
        with pytest.raises(ValueError):
            add_user(username='a1' * 4, password=password, full_name='admin',
                     phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)


def test_exist_username(test_app, test_session, mock_cloudinary):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    username = 'unique_user_123'
    password = 'Abcd123@'
    phone1 = '0323456780'
    phone2 = '0323456781'
    email1 = 'test1@gmail.com'
    email2 = 'test2@gmail.com'

    with test_app.app_context():
        add_user(username=username, password=password, full_name='admin',
                 phone=phone1, birthday=birthday_obj, email=email1, avatar='abc')

        with pytest.raises(ValueError):
            add_user(username=username, password=password, full_name='admin',
                     phone=phone2, birthday=birthday_obj, email=email2, avatar='abc')


@pytest.mark.parametrize('username', [
    'a' * 5, '1' * 4
])
def test_invalid_username(test_app, username):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()

    with test_app.app_context():
        with pytest.raises(ValueError):
            add_user(username=username, password='Abc1234@', full_name='admin',
                     phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)


@pytest.mark.parametrize('email', [
    'user name@gmail.com', 'user@gmail', '@gmail.com'
])
def test_invalid_email(test_app, email):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()

    with test_app.app_context():
        with pytest.raises(ValueError):
            add_user(username='1' * 6, password='Abc1234@', full_name='admin',
                     phone='0323456789', birthday=birthday_obj, email=email, avatar=None)


def test_exist_email(test_app, test_session, mock_cloudinary):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    username = 'unique_user_12'
    password = 'Abcd123@'
    phone1 = '0323456780'
    phone2 = '0323456781'
    email1 = 'test1@gmail.com'
    email2 = 'test1@gmail.com'

    with test_app.app_context():
        add_user(username=username, password=password, full_name='admin',
                 phone=phone1, birthday=birthday_obj, email=email1, avatar='abc')

        with pytest.raises(ValueError):
            add_user(username=username, password=password, full_name='admin',
                     phone=phone2, birthday=birthday_obj, email=email2, avatar='abc')


@pytest.mark.parametrize('birthday', [
    '9/4/2014', '9/4/1925', ''
])
def test_invalid_birthday(test_app, birthday):
    with test_app.app_context():
        with pytest.raises(ValueError):
            birthday_obj = datetime.strptime(birthday, '%d/%m/%Y').date()
            add_user(username='a1' * 4, password='Abc1234@', full_name='admin',
                     phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)


def test_exist_phone(test_app, test_session, mock_cloudinary):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    username1 = 'unique_user_12'
    username2 = 'unique_user_1'
    password = 'Abcd123@'
    phone = '0323456780'
    email1 = 'test1@gmail.com'
    email2 = 'test2@gmail.com'

    with test_app.app_context():
        add_user(username=username1, password=password, full_name='admin',
                 phone=phone, birthday=birthday_obj, email=email1, avatar='abc')

        with pytest.raises(ValueError):
            add_user(username=username2, password=password, full_name='admin',
                     phone=phone, birthday=birthday_obj, email=email2, avatar='abc')

@pytest.mark.parametrize('phone', [
    '0123456789','012345678','01234567899','1234567890','034567890','03456789000'
])
def test_invalid_phone(test_app, phone):
    with test_app.app_context():
        with pytest.raises(ValueError):
            birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
            add_user(username='a1' * 4, password='Abc1234@', full_name='admin',
                     phone=phone, birthday=birthday_obj, email='admin123@gmail.com', avatar=None)

