from app.dao import add_user
from app.test.base_test import test_session, test_app, mock_cloudinary
import hashlib
import pytest
from app.models import Customer
from datetime import datetime

def test_success(test_app, test_session):
    date_string = '1/1/2008'
    birthday_obj = datetime.strptime(date_string, '%d/%m/%Y').date()
    username = 'a1' * 4
    password = 'Abcd123@'
    phone = '0323456789'

    with test_app.app_context():
        add_user(username=username, password=password, full_name='admin',
                 phone=phone, birthday=birthday_obj, email='admin123@gmail.com', avatar=None)

        u = Customer.query.filter(Customer.username == username).first()
        assert u is not None
        assert u.full_name == 'admin'
        assert u.password == hashlib.md5(password.encode('utf-8')).hexdigest()


@pytest.mark.parametrize('password', [
    '1a' * 3,
    '12',
    'aaaaaaa'
])
def test_invalid_password(test_app, password):
    date_string = '1/1/2008'
    birthday_obj = datetime.strptime(date_string, '%d/%m/%Y').date()

    with test_app.app_context():
        with pytest.raises(ValueError):
            add_user(username='a1' * 4, password=password, full_name='admin',
                     phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)

def test_exist_username(test_app, test_session, mock_cloudinary):
    date_string = '1/1/2008'
    birthday_obj = datetime.strptime(date_string, '%d/%m/%Y').date()
    username = 'unique_user_123'
    password = 'Abcd123@'
    phone1 = '0323456780'
    phone2 = '0323456781'
    email1 = 'test1@gmail.com'
    email2 = 'test2@gmail.com'

    with test_app.app_context():
        add_user(username=username, password=password, full_name='admin',
                 phone=phone1, birthday=birthday_obj, email=email1, avatar='abc')

        with pytest.raises(ValueError) as excinfo:
            add_user(username=username, password=password, full_name='admin',
                     phone=phone2, birthday=birthday_obj, email=email2, avatar='abc')

        assert "Tên đăng nhập đã tồn tại" in str(excinfo.value)