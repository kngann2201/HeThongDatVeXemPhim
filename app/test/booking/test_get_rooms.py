from app.test.base_test import *
from app import dao



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

def test_get_booking_rooms(test_client, mocker):
    mock_rooms = mocker.patch('app.index.dao.get_room_by_type')
    room1 = mocker.Mock(id=1, number=101, image="room1_1.jpg", active=True)
    room2 = mocker.Mock(id=2, number=102, image="room1_2.jpg", active=True)
    mock_rooms.return_value = [room1, room2]
    response = test_client.get('/api/get-rooms/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert len(data['rooms']) == 2

def test_get_no_booking_rooms(test_client, mocker):
    mocker.patch('app.index.dao.get_room_by_type', return_value=[])
    response = test_client.get('/api/get-rooms/22')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert len(data['rooms']) == 0