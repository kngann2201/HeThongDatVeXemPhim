import time
from selenium.webdriver.common.by import By
from app import db
from app.models import Ticket, TicketStatus
from app.test.selenium.tests.conftest import driver, sel_app
from app.test.selenium.pages.HistoryBookingPage import HistoryBookingPage

def test_cancel_ticket_success(driver):
    h = HistoryBookingPage(driver=driver)
    h.open_page()

    time.sleep(10)

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .text-end .text-danger')
    assert price_b.text == '200,000đ'

    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .bg-white')
    time.sleep(1)
    h.click(By.CSS_SELECTOR, '#collapse1 tr:nth-child(2) > td:nth-child(6) .btn-danger')
    h.accept_alert(expect='Hủy vé thành công!')

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .text-end .text-danger')
    assert price_b.text == '100,000đ'
    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .bg-white')
    time.sleep(1)
    e = h.find(By.CSS_SELECTOR, '#collapse1 tr:nth-child(2) > td:nth-child(5) > span')
    assert 'Đã hủy' in e.text

def test_cancel_ticket_in_2h_left(driver):
    h = HistoryBookingPage(driver=driver)
    h.open_page()

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(2) .text-end .text-danger')
    assert price_b.text == '100,000đ'

    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(2) .bg-white')
    time.sleep(1)
    h.click(By.CSS_SELECTOR, '#collapse2 tr:nth-child(1) > td:nth-child(6) .btn-danger')
    h.accept_alert(expect='Hủy vé thành công!')

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(2) .text-end .text-danger')
    assert price_b.text == '0đ'
    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(2) .bg-white')
    time.sleep(1)
    e = h.find(By.CSS_SELECTOR, '#collapse2 tr:nth-child(1) > td:nth-child(5) > span')
    assert 'Đã hủy' in e.text

def test_cancel_ticket_less_than_2h_left(driver):
    h = HistoryBookingPage(driver=driver)
    h.open_page()

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(3) .text-end .text-danger')
    assert price_b.text == '100,000đ'

    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(3) .bg-white')
    time.sleep(1)
    h.click(By.CSS_SELECTOR, '#collapse3 tr:nth-child(1) > td:nth-child(6) .btn-danger')
    h.accept_alert(expect='Quá hạn hủy vé! Bạn chỉ có thể hủy trước giờ chiếu ít nhất 2 tiếng.')

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(3) .text-end .text-danger')
    assert price_b.text == '100,000đ'
    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(3) .bg-white')
    time.sleep(1)
    e = h.find(By.CSS_SELECTOR, '#collapse3 tr:nth-child(1) > td:nth-child(5) > span')
    assert 'Đã thanh toán' in e.text

def test_cancel_checkin_ticket(driver, sel_app):
    h = HistoryBookingPage(driver=driver)
    h.open_page()

    with sel_app.app_context():
        ticket = Ticket.query.filter_by(id=4).first()
        ticket.status = TicketStatus.USED
        db.session.commit()

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .text-end .text-danger')
    assert price_b.text == '200,000đ'

    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .bg-white')
    time.sleep(1)
    h.click(By.CSS_SELECTOR, '#collapse1 tr:nth-child(2) > td:nth-child(6) .btn-danger')
    h.accept_alert(expect='Vé đã check-in và sử dụng, không thể hủy!')

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .text-end .text-danger')
    assert price_b.text == '200,000đ'
    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .bg-white')
    time.sleep(1)
    e = h.find(By.CSS_SELECTOR, '#collapse1 tr:nth-child(2) > td:nth-child(5) > span')
    assert 'Đã sử dụng' in e.text



