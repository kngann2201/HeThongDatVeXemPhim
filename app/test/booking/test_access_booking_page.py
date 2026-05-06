from app.test.base_test import *
from app import dao



def test_get_movie_exist(test_session, sample_movie):
    result = dao.get_movie_by_id(movie_id=1)
    assert result is not None
    assert result.id == 1

def test_get_movie_not_exist(test_session, sample_movie):
    result = dao.get_movie_by_id(movie_id=22)
    assert result is None

def test_get_movie_no_type(test_session, sample_movie_type, sample_movie_type_detail):
    result = dao.get_movie_types(movie_id=4)
    assert len(result) == 0

def test_get_movie_types(test_session, sample_movie_type, sample_movie_type_detail):
    result = dao.get_movie_types(movie_id=1)
    assert len(result) == 2

def test_get_movie_type_movie_not_exist(test_session, sample_movie_type, sample_movie_type_detail):
    result = dao.get_movie_types(movie_id=22)
    assert len(result) == 0

def test_get_all_room_types(test_session, sample_room_type):
    result = dao.get_room_types()
    assert len(result) == 3

def test_get_movie_view(test_session, sample_movie, sample_screening, sample_screening_seats, sample_bill, sample_tickets):
    result = dao.ticket_count_by_movie_id(movie_id=1)
    assert result == 3

def test_get_movie_no_view(test_session, sample_movie, sample_screening, sample_screening_seats, sample_bill, sample_tickets):
    result = dao.ticket_count_by_movie_id(movie_id=3)
    assert result == 0

def test_access_booking_page(test_client, mocker):
    mock_movie = mocker.patch('app.index.dao.get_movie_by_id')
    mock_types = mocker.patch('app.index.dao.get_movie_types')
    mock_room_types = mocker.patch('app.index.dao.get_room_types')
    mock_views = mocker.patch('app.index.dao.ticket_count_by_movie_id')

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
    mock_views.return_value = 0

    assert response.status_code == 200

def test_access_booking_page_fail(test_client, mocker):
    mocker.patch('app.index.dao.get_movie_by_id', return_value=None)
    response = test_client.get('/booking/22')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'