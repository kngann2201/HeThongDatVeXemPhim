from datetime import date
from app.test.base_test import test_app, test_session, test_client


def test_access_booking_page(test_client, mocker):
    mock_movie = mocker.patch('app.index.dao.get_movie_by_id')
    mock_types = mocker.patch('app.index.dao.get_movie_types')
    mock_room_types = mocker.patch('app.index.dao.get_room_types')

    response = test_client.get('/booking/1')
    mock_movie.return_value = {
        'id': 1,
        'title': "The Dark Knight",
        'description':"Batman tiếp tục cuộc chiến chống lại tội phạm tại Gotham cùng với cảnh sát và công tố viên Harvey Dent. Một kẻ thù mới xuất hiện, Joker, mang đến sự hỗn loạn chưa từng có. Hắn không chỉ gây rối mà còn thách thức các nguyên tắc đạo đức của Batman. Thành phố dần rơi vào trạng thái hỗn loạn khi Joker thực hiện những kế hoạch tàn bạo. Batman buộc phải đối mặt với những lựa chọn khó khăn để bảo vệ Gotham.",
        'age_limit': 16,
        'duration': 152,
        'poster': "the_dark_knight.png",
        'release_date': date(2008, 7, 18)
    }
    mock_types.return_value = [
        {'id': 1, 'name': 'Hài kịch'},
        {'id': 2, 'name': 'Hành động'}
    ]
    mock_room_types.return_value = [
        {'id': 1, 'name': 'VIP'}
    ]
    assert response.status_code == 200

def test_access_booking_page_fail(test_client, mocker):
    mocker.patch('app.index.dao.get_movie_by_id', return_value=None)
    response = test_client.get('/booking/22')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

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







