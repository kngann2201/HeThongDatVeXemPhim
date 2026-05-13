from app import dao
from app.dao import auth_user, add_user
from app.models import Customer
from app.test.base_test import test_session, test_app, mock_cloudinary
from datetime import datetime
import pytest
import hashlib


@pytest.mark.parametrize('username, password', [
    ('a1' * 4, 'Abc1234'),
    ('a1a1a1', 'Abcd123@'),
    ('', ''),
    ('a1' * 4, ''),
    ('', 'Abcd123@')
])
def test_login_fail(test_app, username, password):

    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    with test_app.app_context():
        add_user(username='a1' * 4, password='Abcd123@', full_name='admin',
                 phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)

    test_login=auth_user(username=username, password=password)
    assert test_login is None


def test_login_success(test_app):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    with test_app.app_context():
        add_user(username='a1' * 4, password='Abcd123@', full_name='admin',
                 phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)

    test_login = auth_user(username='a1'*4, password='Abcd123@')

    assert test_login is not None
    assert test_login.username == 'a1'*4
    assert test_login.password == hashlib.md5('Abcd123@'.encode('utf-8')).hexdigest()


def test_add_user_database_error_login(test_app, mocker, test_session):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    mocker.patch("app.db.session.commit", side_effect=Exception("Database Down"))

    with pytest.raises(Exception):
        dao.add_user(username="abcccc", password="Hehe@123!", full_name='adminsss',
                     phone='0365872837', birthday=birthday_obj, email='adminsnfbah@gmail.com', avatar=None)

    login = dao.auth_user('abcccc', 'Hehe@123!')
    assert login is None


def test_add_user_success_login(test_app, test_session, mock_cloudinary):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    dao.add_user(username="abcccc", password="Hehe@123!", full_name='adminsss',
                 phone='0365872837', birthday=birthday_obj, email='adminsnfbah@gmail.com', avatar=None)

    user = test_session.query(Customer).filter_by(username='abcccc').first()
    assert user is not None
    assert user.full_name == 'adminsss'
    assert user.phone_number == '0365872837'
    assert user.birthday == birthday_obj
    assert user.email == 'adminsnfbah@gmail.com'
    assert user.password == hashlib.md5('Hehe@123!'.encode('utf-8')).hexdigest()
    assert user.avatar == 'https://res.cloudinary.com/dkzxdp1gi/image/upload/v1767843265/avatar-trang-nu-001_dym4n0.webp'

    login = dao.auth_user('abcccc', 'Hehe@123!')
    assert login is not None