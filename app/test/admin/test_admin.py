from unittest.mock import MagicMock, patch

import pytest
from app.admin import CustomerView
from app.models import Customer
from app.test.base_test import test_app, test_session, test_client, sample_users
from app import app

def test_add_invalid_password(test_session):
    with app.test_request_context():
        view = CustomerView(Customer, test_session)
        form = MagicMock()
        form.username.data = "user3"
        form.email.data = "user@1233.com"
        form.phone_number.data = "0367822743"

        form.password.data = "pppass321"
        model = Customer()

        with pytest.raises(ValueError, match="Mật khẩu phải chứa kí tự in hoa và số!"):
            view.on_model_change(form, model, is_created=True)

def test_add_invalid_email(test_session):
    with app.test_request_context():
        view = CustomerView(Customer, test_session)
        form = MagicMock()
        form.username.data = "user3"
        form.phone_number.data = "0367822743"
        form.password.data = "Pass@123"

        form.email.data = "user.com"
        model = Customer()

        with pytest.raises(ValueError, match="Email không đúnng định dạng!"):
            view.on_model_change(form, model, is_created=True)

def test_add_invalid_phone(test_session):
    with app.test_request_context():
        view = CustomerView(Customer, test_session)
        form = MagicMock()
        form.username.data = "user3"
        form.email.data = "user@1233.com"
        form.password.data = "Pass@123"

        form.phone_number.data = "036782274"
        model = Customer()

        with pytest.raises(ValueError, match="Số điện thoại không hợp lệ!"):
            view.on_model_change(form, model, is_created=True)

# def test_add_existing_user(test_session, sample_users):
#     with app.test_request_context():
#         view = CustomerView(Customer, test_session)
#         form = MagicMock()
#         form.email.data = "user@1233.com"
#         form.phone_number.data = "0367822743"
#         form.password.data = "Pass@321"
#         form.avatar.data = None
#
#         form.username.data = "user1"
#         model = Customer()
#
#         with patch("app.admin.dao.is_username_exists", return_value=True):
#             with pytest.raises(ValueError, match="Username đã tồn tại!"):
#                 view.on_model_change(form, model, is_created=True)