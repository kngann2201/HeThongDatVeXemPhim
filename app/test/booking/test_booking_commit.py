import pytest
from app.test.base_test import *
from app import dao



def test_hold_one_seat(test_session, sample_screening_seats):
    seat_ids = ['1']
    result = dao.hold_seats(seat_ids=seat_ids, screening_id=1)
    assert len(result) == 1
    assert result[0].screening_id == 1
    assert result[0].seat_id == 1

def test_hold_max_seats(test_app, test_session, sample_screening_seats):
    seat_ids = ['1', '2', '3', '4', '5', '6', '7', '8']
    result = dao.hold_seats(seat_ids=seat_ids, screening_id=1)
    assert len(result) == 8
    assert all(r.screening_id == 1 for r in result)

def test_hold_invalid_screening(test_session, sample_screening_seats):
    seat_ids = ['1', '2', '3', '4', '5', '6', '7']
    result = dao.hold_seats(seat_ids=seat_ids, screening_id=22)
    assert len(result) == 0

def test_total_seat_per_screening(test_session, sample_screening_seats):
    result = dao.total_seat_per_screening(screening_id=1, user_id=1)
    assert result == 1

def test_total_seat_per_invalid_screening(test_session, sample_screening_seats):
    result = dao.total_seat_per_screening(screening_id=11, user_id=1)
    assert result == 0

def test_total_seat_per_screening_invalid_user(test_session, sample_screening_seats):
    result = dao.total_seat_per_screening(screening_id=1, user_id=11)
    assert result == 0