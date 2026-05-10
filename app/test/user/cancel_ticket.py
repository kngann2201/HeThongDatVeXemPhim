import pytest
from datetime import datetime, timedelta
from app.models import TicketStatus, SeatStatus, PaymentStatus
from app.dao import cancel_ticket
from app.test.base_test import *

class FakeUser:
    def __init__(self, user_id=1):
        self.id = user_id
        self.is_authenticated = True


@pytest.fixture
def mock_user(mocker):
    user = FakeUser(user_id=1)  # ID = 1 khớp với sample_users của bạn
    mocker.patch('flask_login.utils._get_user', return_value=user)
    return user


def test_cancel_ticket_success(test_app, test_session, sample_tickets, mock_user):
    ticket = sample_tickets[1]
    bill = ticket.bill
    initial_total = bill.total_amount
    ticket_price = ticket.price

    result = cancel_ticket(ticket_id=ticket.id, customer_id=mock_user.id)

    assert result is True
    assert ticket.status == TicketStatus.CANCELLED
    assert ticket.screening_seat.status == SeatStatus.AVAILABLE
    assert ticket.screening_seat.holding_user_id is None
    assert bill.total_amount == initial_total - ticket_price


def test_cancel_last_ticket_sets_bill_cancelled(test_app, test_session, sample_tickets, mock_user):
    ticket = sample_tickets[0]
    bill = ticket.bill
    bill.tickets = [ticket]
    test_session.commit()

    cancel_ticket(ticket_id=ticket.id, customer_id=mock_user.id)

    assert bill.status == PaymentStatus.CANCELLED
    assert bill.total_amount == 0


def test_cancel_ticket_wrong_user(test_app, test_session, sample_tickets):
    ticket = sample_tickets[0]
    wrong_user_id = 999

    with pytest.raises(ValueError):
        cancel_ticket(ticket_id=ticket.id, customer_id=wrong_user_id)


def test_cancel_ticket_before_2_hours_watching(test_app, test_session, sample_tickets, mock_user):
    ticket = sample_tickets[0]
    ticket.screening_seat.screening.start_time = datetime.now() + timedelta(hours=1)
    test_session.commit()

    with pytest.raises(ValueError):
        cancel_ticket(ticket_id=ticket.id, customer_id=mock_user.id)


def test_cancel_ticket_used(test_app, test_session, sample_tickets, mock_user):
    ticket = sample_tickets[2]

    with pytest.raises(ValueError):
        cancel_ticket(ticket_id=ticket.id, customer_id=mock_user.id)


def test_cancel_ticket_cancelled(test_app, test_session, sample_tickets, mock_user):
    ticket = sample_tickets[3]

    with pytest.raises(ValueError, match="Vé này đã được hủy trước đó"):
        cancel_ticket(ticket_id=ticket.id, customer_id=mock_user.id)

def test_cancel_ticket_exception(test_app, test_session, sample_tickets, mock_user, mocker):
    ticket = sample_tickets[0]
    original_status = ticket.status

    mocker.patch('app.db.session.commit', side_effect=Exception("Database down"))

    with pytest.raises(Exception):
        cancel_ticket(ticket_id=ticket.id, customer_id=mock_user.id)
    test_session.refresh(ticket)
    assert ticket.status == original_status