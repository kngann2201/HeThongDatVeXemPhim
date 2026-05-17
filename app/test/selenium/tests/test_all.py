import os
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.test.selenium.pages.BookingPage import BookingPage
from app.test.selenium.pages.HistoryBookingPage import HistoryBookingPage
from app.test.selenium.pages.PaymentPage import PaymentPage
from app.test.selenium.tests.conftest import driver, sel_app
from app.test.selenium.pages.HomePage import HomePage
from app.test.selenium.pages.LoginPage import LoginPage
from app.test.selenium.pages.RegisterPage import RegisterPage


def test_login_flow(driver):
    home = HomePage(driver=driver)
    home.open_page()

    e = home.find(By.CLASS_NAME, 'btn-danger')
    e.click()
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/register'

    re = RegisterPage(driver=driver)
    avatar_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../assets/avatar-cute-3.jpg")
    )
    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788392',
                'abc@gmail.com', 'abc123', 'Pass@123', 'Pass@123', avatar_path)

    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/login'

    login = LoginPage(driver=driver)
    login.login('abc123', 'Pass@123')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/'

def test_system_booking_flow_without_login(driver):
    home = HomePage(driver=driver)
    home.open_page()

    book = BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_login()

    login = LoginPage(driver=driver)
    login.login("user123", "Pass@123")
    time.sleep(1)

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.5)
    book.select_n_seats(4)
    book.book_ticket()
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'

def test_system_booking_flow_with_login(driver):
    home = HomePage(driver=driver)
    home.open_page()

    e = home.find(By.CLASS_NAME, 'btn-outline-light')
    e.click()
    time.sleep(0.5)
    login = LoginPage(driver=driver)
    login.login("user123", "Pass@123")
    time.sleep(1)

    book = BookingPage(driver=driver)
    book.book()
    selected_date = driver.execute_script("return selected_info.date;")
    print("Ngày đang chọn:", selected_date)
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(4)
    book.book_ticket()
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'

def test_system_booking_cancel_flow(driver):
    home = HomePage(driver=driver)
    home.open_page()

    book = BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat2()
    book.select_login()

    login = LoginPage(driver=driver)
    login.login("user123", "Pass@123")
    time.sleep(1)

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.5)
    book.select_n_seats(4)
    book.book_ticket()
    book.select_pay_back()

    hb = HistoryBookingPage(driver=driver)
    hb.open_page(login=True)

    hb.click(By.CSS_SELECTOR, '#accordionBooking > div:last-child .bg-white')
    hb.click(By.CSS_SELECTOR, '#collapse5 tr:nth-child(1) > td:nth-child(6) .btn-danger')
    hb.accept_alert(expect='Hủy vé thành công!')

@pytest.mark.skipif(os.getenv('GITHUB_ACTIONS'))
def test_booking_payment_flow(driver):
    home = HomePage(driver=driver)
    home.open_page()

    book = BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat2()
    book.select_login()

    login = LoginPage(driver=driver)
    login.login("user123", "Pass@123")
    time.sleep(1)

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.5)
    book.select_n_seats(4)
    book.book_ticket()
    time.sleep(0.5)

    payment = PaymentPage(driver=driver)
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.card_number('9704198526191432198')
    payment.card_holder('NGUYEN VAN A')
    payment.card_date('07/15')
    payment.select_btn_continue()
    payment.select_btn_agree()
    payment.otp_value('123456')
    payment.select_btn_confirm()
    wait = WebDriverWait(driver, 10)
    success_msg_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-card h2.text-info"))
    )
    assert "Thanh toán thành công!" in success_msg_element.text






