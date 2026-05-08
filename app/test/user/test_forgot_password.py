from app.dao import add_user, send_reset_email, get_customer_by_email, update_password
from app.test.base_test import test_session, test_app, test_client
from datetime import datetime
from app import mail, db
import pytest
from app.models import Customer
import hashlib

def test_get_user_by_email_success(test_app):

    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    with test_app.app_context():
        add_user(username='a1' * 4, password='Abcd123@', full_name='admin',
                 phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)

    get_user=get_customer_by_email('admin123@gmail.com')
    assert get_user is not None

def test_get_user_by_email_fail(test_app):

    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    with test_app.app_context():
        add_user(username='a1' * 4, password='Abcd123@', full_name='admin',
                 phone='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)

    get_user=get_customer_by_email('admin123@gmail.co')
    assert get_user is None

def test_update_password_success(test_app):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    new_cust = Customer(id=1, username='a1' * 4, password='Abcd123@', full_name='admin',
                 phone_number='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)
    db.session.add(new_cust)
    db.session.commit()
    result = update_password(customer_id=1, new_password="Password123@")
    assert result is True

    updated_cust = Customer.query.get(1)
    assert updated_cust.password == hashlib.md5('Password123@'.encode('utf-8')).hexdigest()

@pytest.mark.parametrize('password', [
    '1' * 7, '1a' * 3 + 'A','@'*7,'Ab1'*2+'@',
    'A1' * 4, 'Aa' * 4, 'a1' * 4,'1@'*4,'a@'*4,'@A'*4,'Ha11'*4,'Aau@'*2,'@a1a'*2,'@AA1'*2,
    '1' * 8, 'a' * 8, 'A' * 8,'@'*8

])
def test_update_password_fail(test_app,password):
    birthday_obj = datetime.strptime('1/1/2008', '%d/%m/%Y').date()
    new_cust = Customer(id=1, username='a1' * 4, password='Abcd123@', full_name='admin',
                        phone_number='0323456789', birthday=birthday_obj, email='admin123@gmail.com', avatar=None)
    db.session.add(new_cust)
    db.session.commit()

    with pytest.raises(ValueError):
        update_password(customer_id=1, new_password=password)
    result_update = update_password(customer_id=999, new_password="ValidPassword123@")
    assert result_update is False

def test_send_reset_email_failure(test_app, monkeypatch):
    def mock_send_fail(msg):
        raise Exception("Connection error")

    monkeypatch.setattr(mail, "send", mock_send_fail)

    with test_app.app_context():
        result = send_reset_email("fail@example.com", "000000")
        assert result is False


def test_send_reset_email_success(test_app):
    from app import mail
    from app.dao import send_reset_email

    email = "ngan@example.com"
    otp = "123456"

    with test_app.app_context():
        with mail.record_messages() as outbox:
            result = send_reset_email(email, otp)

            assert result is True
            assert len(outbox) == 1
            assert outbox[0].subject == 'Mã xác nhận đặt lại mật khẩu'
            assert email in outbox[0].recipients