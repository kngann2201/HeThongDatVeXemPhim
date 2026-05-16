from app.test.base_test import *
from app import dao
from datetime import datetime, timedelta



def test_get_movie_screenings_in_time(test_session, sample_screening, sample_room_type, sample_room):
    watch_date = datetime.now().date()
    result = dao.get_movie_screenings(movie_id=1, room_type_id=1, watch_date=watch_date)
    assert len(result) == 2
    assert all(r.movie_id == 1 for r in result)
    assert all(r.room_id == 1 for r in result)
    assert all(r.start_time.date() == watch_date for r in result)

def test_get_movie_screenings_in_future(test_session, sample_screening, sample_room_type, sample_room):
    watch_date = datetime.now().date() + timedelta(days=1)
    result = dao.get_movie_screenings(movie_id=1, room_type_id=1, watch_date=watch_date)
    assert len(result) == 1
    assert all(r.movie_id == 1 for r in result)
    assert all(r.room_id == 1 for r in result)
    assert all(r.start_time.date() == watch_date for r in result)

def test_get_screening_success(test_session, test_client, sample_screening, sample_room_type, sample_movie):
    response = test_client.get(
        '/api/get-screenings',
        query_string={
            'watch_date': datetime.now().date().strftime("%Y-%m-%d"),
            'room_type_id': 1,
            'movie_id': 1
        }
    )
    data = response.get_json()
    assert data['success'] == True
    assert len(data['screenings']) == 1

def test_get_screening_missing_info(test_session, test_client, sample_screening, sample_room_type, sample_movie):
    response = test_client.get(
        '/api/get-screenings',
        query_string={
            'watch_date': datetime.now().date().strftime("%Y-%m-%d"),
            'room_type_id': 1
        }
    )
    data = response.get_json()
    assert data['success'] == False
    assert data['message'] == "Thiếu thông tin để tìm suất chiếu!"
    assert len(data['screenings']) == 0



