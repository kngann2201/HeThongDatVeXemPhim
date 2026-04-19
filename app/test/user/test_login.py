from app.dao import auth_user, add_user
from app.test.base_test import test_session, test_app
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