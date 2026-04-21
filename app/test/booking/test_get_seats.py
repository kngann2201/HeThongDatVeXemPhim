from app.test.base_test import *
from app import dao

def test_get_seats_by_screening(test_session, sample_seats, sample_screening_seats):
    result = dao.get_seats_by_screening(screening_id=1)
    assert len(result) == 16
    for seat, status in result:
        assert seat is not None
        assert status is not None

def test_get_no_seats_by_screening(test_session, sample_seats, sample_screening_seats):
    result = dao.get_seats_by_screening(screening_id=22)
    assert len(result) == 0