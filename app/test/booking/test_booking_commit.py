import pytest
from app.test.base_test import *
from app import dao


def test_get_exist_screening_by_id(test_session, sample_screening):
    result = dao.get_screening_by_id(screening_id=1)
    assert result is not None
    assert result.id == 1

def test_get_not_exist_screening_by_id(test_session, sample_screening):
    result = dao.get_screening_by_id(screening_id=22)
    assert result is None

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

def test_user_total_seat_per_screening(test_session, sample_seats, sample_screening_seats):
    result = dao.total_seat_per_screening(screening_id=1, user_id=1)
    assert result == 1

def test_booking_missing_info(test_session, test_client, sample_screening, sample_screening_seats, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    seat_ids = [
        sample_screening_seats[1].id,
        sample_screening_seats[2].id
    ]

    response = test_client.post(
        '/booking/submit',
        data={
            'seat': ",".join(map(str, seat_ids))
        },
        follow_redirects=True
    )

    html = response.get_data(as_text=True)
    assert 'Hệ thống đang có lỗi, vui lòng thử lại sau ít phút!' in html

    bill = Bill.query.filter_by(customer_id=user.id).first()
    assert bill is None

def test_booking_screening_already_start(test_session, test_client, sample_screening, sample_screening_seats, mocker, sample_movie):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    response = test_client.post(
        '/booking/submit',
        data={
            'seat': sample_screening_seats[1].id,
            'screening': sample_screening[1].id
        },
        follow_redirects=True
    )

    html = response.get_data(as_text=True)
    assert 'Suất chiếu đã bắt đầu, không thể đặt vé!' in html

    bill = Bill.query.filter_by(customer_id=user.id).first()
    assert bill is None

def test_booking_before_start_10m(test_session, test_client, sample_screening, sample_screening_seats, mocker, sample_movie):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    response = test_client.post(
        '/booking/submit',
        data={
            'seat': sample_screening_seats[1].id,
            'screening': sample_screening[2].id
        },
        follow_redirects=True
    )

    html = response.get_data(as_text=True)
    assert 'Không thể đặt vé trong 10 phút trước giờ chiếu!' in html

    bill = Bill.query.filter_by(customer_id=user.id).first()
    assert bill is None

def test_booking_over_limit_seat(test_session, test_client, sample_screening, sample_screening_seats, mocker, sample_movie):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    seat_ids = []
    for i in range(1, 10):
        seat_ids.append(sample_screening_seats[i].id)

    response = test_client.post(
        '/booking/submit',
        data={
            'seat': ",".join(map(str, seat_ids)),
            'screening': sample_screening[0].id
        },
        follow_redirects=True
    )

    html = response.get_data(as_text=True)
    assert 'Vượt quá số ghế được đặt mỗi suất chiếu!' in html

    bill = Bill.query.filter_by(customer_id=user.id).first()
    assert bill is None

def test_booking_not_found_seat(test_session, test_client, sample_screening, sample_screening_seats, mocker, sample_movie):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    seat_ids = [
        sample_screening_seats[1].id,
        sample_screening_seats[2].id,
        25, 27
    ]

    response = test_client.post(
        '/booking/submit',
        data={
            'seat': ",".join(map(str, seat_ids)),
            'screening': sample_screening[0].id
        },
        follow_redirects=True
    )

    html = response.get_data(as_text=True)
    assert 'Một số ghế không tồn tại trong suất chiếu này!' in html

    bill = Bill.query.filter_by(customer_id=user.id).first()
    assert bill is None

def test_booking_booked_seat(test_session, test_client, sample_screening, sample_screening_seats, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    booked_seat = sample_screening_seats[0]

    response = test_client.post(
        '/booking/submit',
        data={
            'seat': booked_seat.id,
            'screening': sample_screening[0].id
        },
        follow_redirects=True
    )

    html = response.get_data(as_text=True)
    assert 'Ghế đã được đặt!' in html

    bill = Bill.query.filter_by(customer_id=user.id).first()
    assert bill is None

def test_booking_commit_success(test_session, test_client, sample_screening, sample_screening_seats, mocker):
    class FakeUser:
        is_authenticated = True
        id = 5

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    seat_ids = [
        sample_screening_seats[1].id,
        sample_screening_seats[2].id
    ]

    response = test_client.post(
        '/booking/submit',
        data={
            'seat': ",".join(map(str, seat_ids)),
            'screening': sample_screening[0].id
        }
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'Chuyển hướng thanh toán' in html

    bill = Bill.query.filter_by(customer_id=user.id).first()
    assert bill is not None
    assert bill.total_amount == 200000
    tickets = Ticket.query.filter_by(bill_id=bill.id).all()
    assert len(tickets) == 2
    for seat_id in seat_ids:
        ss = ScreeningSeat.query.get(seat_id)
        assert ss.status == SeatStatus.HOLDING

def test_booking_commit_exception(test_session, test_client, sample_screening, sample_screening_seats, mocker):
    class FakeUser:
        is_authenticated = True
        id = 5

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    seat_ids = [
        sample_screening_seats[1].id,
        sample_screening_seats[2].id
    ]
    mocker.patch("app.db.session.commit", side_effect=Exception("Database Down"))
    response = test_client.post(
        '/booking/submit',
        data={
            'seat': ",".join(map(str, seat_ids)),
            'screening': sample_screening[0].id
        },
        follow_redirects = True
    )
    html = response.get_data(as_text=True)
    assert 'Hệ thống đang có lỗi, vui lòng thử lại sau ít phút!' in html



