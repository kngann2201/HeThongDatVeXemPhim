import time

from selenium.webdriver.common.by import By

from app.test.base_test import driver, sel_app
from app.test.selenium.pages.HistoryBookingPage import HistoryBookingPage

def test_cancel_ticket_success(driver):
    h = HistoryBookingPage(driver=driver)
    h.open_page()

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .text-end .text-danger')
    assert price_b.text == '200,000đ'

    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(1) .bg-white')
    time.sleep(1)
    h.click(By.CSS_SELECTOR, '#collapse1 tr:nth-child(2) > td:nth-child(6) .btn-danger')
    alert = driver.switch_to.alert

    assert 'Hủy vé' in alert.text
    alert.accept()
    e = h.find(By.CLASS_NAME, 'alert')
    assert 'Hủy vé thành công!' in e.text

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
    alert = driver.switch_to.alert

    assert 'Hủy vé' in alert.text
    alert.accept()
    e = h.find(By.CLASS_NAME, 'alert')
    assert 'Quá hạn hủy vé! Bạn chỉ có thể hủy trước giờ chiếu ít nhất 2 tiếng.' in e.text

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(2) .text-end .text-danger')
    assert price_b.text == '100,000đ'
    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(2) .bg-white')
    time.sleep(1)
    e = h.find(By.CSS_SELECTOR, '#collapse2 tr:nth-child(1) > td:nth-child(5) > span')
    assert 'Đã thanh toán' in e.text

def test_cancel_ticket_less_than_2h_left(driver):
    h = HistoryBookingPage(driver=driver)
    h.open_page()

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(3) .text-end .text-danger')
    assert price_b.text == '100,000đ'

    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(3) .bg-white')
    time.sleep(1)
    h.click(By.CSS_SELECTOR, '#collapse3 tr:nth-child(1) > td:nth-child(6) .btn-danger')
    alert = driver.switch_to.alert

    assert 'Hủy vé' in alert.text
    alert.accept()
    e = h.find(By.CLASS_NAME, 'alert')
    assert 'Quá hạn hủy vé! Bạn chỉ có thể hủy trước giờ chiếu ít nhất 2 tiếng.' in e.text

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(3) .text-end .text-danger')
    assert price_b.text == '100,000đ'
    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(3) .bg-white')
    time.sleep(1)
    e = h.find(By.CSS_SELECTOR, '#collapse3 tr:nth-child(1) > td:nth-child(5) > span')
    assert 'Đã thanh toán' in e.text




