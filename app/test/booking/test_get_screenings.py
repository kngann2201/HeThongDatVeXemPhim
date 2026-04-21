from app.test.base_test import *
from app import dao
from datetime import datetime, timedelta



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
