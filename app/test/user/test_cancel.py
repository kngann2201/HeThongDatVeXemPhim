from app.models import TicketStatus, SeatStatus
from app.dao import cancel_ticket
from app.test.base_test import (test_app, test_session, sample_movie, sample_room,sample_seats, sample_screening, sample_screening_seats_v2,
                                sample_screening_seats, sample_bill, sample_tickets)
import pytest

@pytest.mark.parametrize('ticket_index', [1, 2, 3])
def test_cancel_ticket_fail(test_app,test_session, sample_tickets, mocker, ticket_index):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    ticket = sample_tickets[ticket_index]
    with pytest.raises(ValueError):
        cancel_ticket(ticket_id=ticket.id, customer_id=user.id)



def test_cancel_ticket_success(test_app, test_session, sample_tickets, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)
    ticket = sample_tickets[0]
    cancel_ticket(ticket_id=ticket.id, customer_id=user.id)
    test_session.refresh(ticket)
    assert ticket.status == TicketStatus.CANCELLED
    assert ticket.screening_seat.status == SeatStatus.AVAILABLE
