from app.test.base_test import (test_app, test_session, sample_room,
        sample_movie, sample_movie_type, sample_movie_type_detail)
from app import dao

def test_get_movie_type(test_session, sample_movie, sample_movie_type, sample_movie_type_detail):
    result = dao.get_movie_types(movie_id=1)
    assert len(result) == 2

def test_get_rooms(test_session, sample_room, sample_movie_type):
    result = dao.get_room_by_type(room_type_id=1)
    assert len(result) == 2
    assert all(r.room_type_id == 1 for r in result)
