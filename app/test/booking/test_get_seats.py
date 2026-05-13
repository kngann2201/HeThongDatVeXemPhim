from app.test.base_test import *
from app import dao

def test_get_seats_by_screening(test_session, sample_seats, sample_screening_seats):
    result = dao.get_seats_by_screening(screening_id=1)
    assert len(result) == 22
    for seat, status in result:
        assert seat is not None
        assert status is not None

def test_get_no_seats_by_screening(test_session, sample_seats, sample_screening_seats):
    result = dao.get_seats_by_screening(screening_id=22)
    assert len(result) == 0

def test_get_seats_success(test_session, test_client, sample_screening, sample_seats, sample_screening_seats):
    scr_id = sample_screening[0].id
    response = test_client.get(f'/api/get-seats/{scr_id}')
    data = response.get_json()
    assert data['success'] == True
    total_seats = sum(len(seats_in_row) for seats_in_row in data['seats'].values())
    assert total_seats == 22

def test_get_seats_fail(test_session, test_client, sample_screening, sample_seats, sample_screening_seats):
    response = test_client.get('/api/get-seats/99')
    data = response.get_json()
    assert data['success'] == False
    assert data['message'] == "Không tìm thấy ghế phù hợp!"
    assert data['seats'] == []
