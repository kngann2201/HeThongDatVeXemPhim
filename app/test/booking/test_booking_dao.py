from datetime import datetime, date, timedelta

import pytest

from app.test.base_test import (
    test_app, test_session,
    sample_movie, sample_movie_type, sample_room_type, sample_movie_type_detail,
    sample_room, sample_screening, sample_seats, sample_screening_seats
)
from app import dao

def test_get_movie_exist(test_session, sample_movie):
    result = dao.get_movie_by_id(movie_id=1)
    assert result is not None
    assert result.id == 1

def test_get_movie_not_exist(test_session, sample_movie):
    result = dao.get_movie_by_id(movie_id=22)
    assert result is None

def test_get_movie_no_type(test_session, sample_movie_type):
    result = dao.get_movie_types(movie_id=4)
    assert len(result) == 0

def test_get_movie_types(test_session, sample_movie_type, sample_movie_type_detail):
    t1 = sample_movie_type[0]
    t2 = sample_movie_type[1]
    result = dao.get_movie_types(movie_id=1)
    assert len(result) == 2
    assert result[0].id == t1.id
    assert result[1].id == t2.id

def test_get_movie_type_movie_not_exist(test_session, sample_movie_type):
    result = dao.get_movie_types(movie_id=22)
    assert len(result) == 0

def test_get_all_room_types(test_session, sample_room_type):
    result = dao.get_room_types()
    assert len(result) == 3

def test_get_rooms(test_session, sample_room):
    result = dao.get_room_by_type(room_type_id=1)
    assert len(result) == 2
    assert all(r.room_type_id == 1 for r in result)

def test_get_no_rooms(test_session,sample_room):
    result = dao.get_room_by_type(room_type_id=3)
    assert len(result) == 0

def test_get_rooms_room_type_not_exist(test_session, sample_room):
    result = dao.get_room_by_type(room_type_id=22)
    assert len(result) == 0

def test_get_movie_screenings_in_past(test_session, sample_screening):
    watch_date = datetime.now().date() - timedelta(days=1)
    result = dao.get_movie_screenings(movie_id=1, room_id=1, watch_date=watch_date)
    assert len(result) == 0

def test_get_movie_screenings_in_time(test_session, sample_screening):
    watch_date = datetime.now().date()
    result = dao.get_movie_screenings(movie_id=1, room_id=1, watch_date=watch_date)
    assert len(result) == 1
    assert all(r.movie_id == 1 for r in result)
    assert all(r.room_id == 1 for r in result)
    assert all(r.start_time.date() == watch_date for r in result)

def test_get_movie_screenings_in_future(test_session, sample_screening):
    watch_date = datetime.now().date() + timedelta(days=1)
    result = dao.get_movie_screenings(movie_id=1, room_id=1, watch_date=watch_date)
    assert len(result) == 1
    assert all(r.movie_id == 1 for r in result)
    assert all(r.room_id == 1 for r in result)
    assert all(r.start_time.date() == watch_date for r in result)

def test_get_seats_by_screening(test_session, sample_seats, sample_screening_seats):
    result = dao.get_seats_by_screening(screening_id=1)
    assert len(result) == 16
    for seat, status in result:
        assert seat is not None
        assert status is not None

def test_get_no_seats_by_screening(test_session, sample_seats, sample_screening_seats):
    result = dao.get_seats_by_screening(screening_id=22)
    assert len(result) == 0

def test_hold_one_seat(test_session, sample_screening_seats):
    seat_ids = ['1']
    result = dao.hold_seats(seat_ids=seat_ids, screening_id=1)
    assert len(result) == 1
    assert result[0].screening_id == 1
    assert result[0].seat_id == 1

def test_hold_no_seat(test_session, sample_screening_seats):
    seat_ids = []
    with pytest.raises(Exception, match="Số lượng ghế không hợp lệ!"):
        dao.hold_seats(seat_ids=seat_ids, screening_id=1)

def test_hold_max_seats(test_app, test_session, sample_screening_seats):
    seat_ids = ['1', '2', '3', '4', '5', '6', '7', '8']
    result = dao.hold_seats(seat_ids=seat_ids, screening_id=1)
    assert len(result) == 8
    assert all(r.screening_id == 1 for r in result)

def test_hold_over_seats(test_session, sample_screening_seats):
    seat_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    with pytest.raises(Exception, match="Số lượng ghế không hợp lệ!"):
        dao.hold_seats(seat_ids=seat_ids, screening_id=1)

def test_hold_invalid_screening(test_session, sample_screening_seats):
    seat_ids = ['1', '2', '3', '4', '5', '6', '7']
    result = dao.hold_seats(seat_ids=seat_ids, screening_id=22)
    assert len(result) == 0