from urllib.parse import unquote_plus
from app.test.base_test import *
from app import dao
from app.models import PaymentStatus, TicketStatus, SeatStatus



def test_get_bill_by_id(test_session, sample_bill):
    r = dao.get_bill_by_id(bill_id=1)
    assert r is not None
    assert r.id == 1

def test_get_not_exist_bill_by_id(test_session, sample_bill):
    r = dao.get_bill_by_id(bill_id=99)
    assert r is None

def test_add_bill(test_session):
    r = dao.add_bill(customer_id=1, total=100000)
    assert r is not None
    assert r.id == 1
    assert r.total_amount == 100000

def test_add_bill_no_total(test_session):
    r = dao.add_bill(customer_id=1)
    assert r is not None
    assert r.id == 1
    assert r.total_amount == 0

def test_add_bill_null_customer(test_session):
    with pytest.raises(ValueError):
        dao.add_bill(customer_id=None, total=100000)

def test_add_ticket(test_session):
    r = dao.add_ticket(bill_id=1, ss_id=1, price=100000)
    assert r is not None
    assert r.bill_id == 1
    assert r.screening_seat_id == 1
    assert r.price == 100000

def test_add_ticket_null_bill_id(test_session):
    with pytest.raises(ValueError):
        dao.add_ticket(bill_id=None, ss_id=1, price=100000)

def test_add_ticket_null_ss_id(test_session):
    with pytest.raises(ValueError):
        dao.add_ticket(bill_id=1, ss_id=None, price=100000)

def test_add_ticket_null_price(test_session):
    with pytest.raises(ValueError):
        dao.add_ticket(bill_id=1, ss_id=1, price=None)

def test_add_payment(test_session):
    r = dao.add_payment(bill_id=1, txn_ref='1', amount=100000)
    assert r is not None
    assert r.bill_id == 1
    assert r.txn_ref == '1'
    assert r.amount == 100000

def test_add_payment_null_bill_id(test_session):
    with pytest.raises(ValueError):
        dao.add_payment(bill_id=None, txn_ref=1, amount=100000)

def test_add_payment_null_txn_ref(test_session):
    with pytest.raises(ValueError):
        dao.add_payment(bill_id=1, txn_ref=None, amount=100000)

def test_add_payment_null_amount(test_session):
    with pytest.raises(ValueError):
        dao.add_payment(bill_id=1, txn_ref=1, amount=None)

def test_pay_fail(test_session):
    bill = Bill(customer_id=1, total_amount=1000)
    payment = Payment(bill_id=1, txn_ref="abc123", amount=1000)

    test_session.add_all([bill, payment])
    test_session.commit()
    dao.pay_fail(payment, bill)
    assert payment.status == PaymentStatus.FAILED

def test_pay_success(test_session):
    bill = Bill(customer_id=1, total_amount=1000)
    payment = Payment(bill_id=1, txn_ref="abc123", amount=1000)

    test_session.add_all([bill, payment])
    test_session.commit()
    dao.pay_success(payment, bill)
    tickets = bill.tickets
    assert payment.status == PaymentStatus.SUCCESS
    assert bill.status == PaymentStatus.SUCCESS
    assert all(t.status == TicketStatus.PAID for t in tickets)
    assert all(t.screening_seat.status == SeatStatus.BOOKED for t in tickets)

def test_payment_bill_not_found(test_client, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)
    res = test_client.get("/payment/999999", follow_redirects=True)
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'Hoá đơn không tồn tại!' in html

def test_payment_success_redirect(test_client, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)
    bill = Bill(customer_id=user.id, total_amount=1000)
    db.session.add(bill)
    db.session.commit()

    res = test_client.get(f"/payment/{bill.id}")
    assert res.status_code == 302
    assert bill.payments is not None

def test_vnpay_no_response_code(test_client, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    res = test_client.get("/vnpay_return")
    assert res.status_code == 302
    decoded_url = unquote_plus(res.location)
    assert "Không có mã trả về từ vnpay!" in decoded_url

def test_vnpay_payment_not_found(test_client, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    res = test_client.get("/vnpay_return?vnp_TxnRef=abcd&vnp_ResponseCode=99")
    decoded_url = unquote_plus(res.location)
    assert "Không tìm thấy thông tin thanh toán!" in decoded_url
    assert res.status_code == 302

def test_vnpay_fail_response_code(test_client, test_session, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    bill = Bill(customer_id=1, total_amount=1000)
    payment = Payment(bill=bill, txn_ref="abc", amount=1000)
    test_session.add_all([bill, payment])
    test_session.commit()

    res = test_client.get("/vnpay_return?vnp_TxnRef=abc&vnp_ResponseCode=51")
    decoded = unquote_plus(res.location)
    assert "Thanh toán thất bại!" in decoded

def test_vnpay_seat_not_holding(test_client, test_session, sample_payment, sample_tickets ,sample_screening_seats, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    payment = sample_payment
    bill = payment.bill
    for ticket in bill.tickets:
        ticket.screening_seat.status = SeatStatus.AVAILABLE
    test_session.commit()

    res = test_client.get(f"/vnpay_return?vnp_TxnRef={payment.txn_ref}&vnp_ResponseCode=00")
    decoded = unquote_plus(res.location)
    assert "Ghế đã bị huỷ trong khi thanh toán!" in decoded

def test_vnpay_success(test_client, test_session, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    bill = Bill(customer_id=1, total_amount=1000)
    payment = Payment(bill=bill, txn_ref=1, amount=1000)
    test_session.add_all([bill, payment])
    test_session.commit()
    res = test_client.get("/vnpay_return?vnp_ResponseCode=00&vnp_TxnRef=1")
    decoded = unquote_plus(res.location)
    assert "Thanh toán thành công" in decoded
    assert payment.status == PaymentStatus.SUCCESS
    updated_bill = test_session.query(Bill).filter_by(id=bill.id).first()
    assert updated_bill.status == PaymentStatus.SUCCESS
    tickets = bill.tickets
    for t in tickets:
        assert t.status == TicketStatus.USED

def test_vnpay_duplicate_bill(test_client, test_session, sample_payment, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    payment = sample_payment
    bill = payment.bill

    dao.pay_success(payment, bill)
    test_session.commit()
    res = test_client.get(f"/vnpay_return?vnp_ResponseCode=00&vnp_TxnRef={payment.txn_ref}")
    decoded = unquote_plus(res.location)
    assert bill.status == PaymentStatus.SUCCESS
    assert payment.status == PaymentStatus.SUCCESS
    assert "Hoá đơn đã được thanh toán trước đó!" in decoded

def test_vnpay_payment_timeout(test_client, test_session, sample_payment, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)

    payment = sample_payment
    payment.created_date = datetime.now() - timedelta(minutes=10)
    test_session.commit()
    res = test_client.get(f"/vnpay_return?vnp_ResponseCode=24&vnp_TxnRef={payment.txn_ref}")
    decoded = unquote_plus(res.location)
    assert payment.status == PaymentStatus.FAILED
    bill = payment.bill
    tickets = bill.tickets
    assert bill.status == PaymentStatus.FAILED or PaymentStatus.PENDING
    for t in tickets:
        assert t.status == TicketStatus.CANCELLED or TicketStatus.HOLDING
    assert "Thanh toán thất bại" in decoded

def test_pay_exception(test_client, test_session, sample_payment, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1

    user = FakeUser()
    mocker.patch('flask_login.utils._get_user', return_value=user)
    bill = Bill(customer_id=user.id, total_amount=1000)
    db.session.add(bill)
    db.session.commit()

    mocker.patch("app.db.session.commit", side_effect=Exception("Database Down"))
    response = test_client.get(f"/payment/{bill.id}", follow_redirects=True)
    html = response.get_data(as_text=True)
    assert 'Hệ thống đang có lỗi, vui lòng thử lại sau ít phút!' in html
    assert bill.status == PaymentStatus.FAILED or PaymentStatus.PENDING
    tickets = bill.tickets
    for t in tickets:
        assert t.status == TicketStatus.CANCELLED or TicketStatus.HOLDING










