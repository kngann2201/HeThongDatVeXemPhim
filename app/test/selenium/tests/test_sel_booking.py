import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from app.test.selenium.tests.conftest import driver, sel_app
from app.test.selenium.pages.HomePage import HomePage
from app.test.selenium.pages.LoginPage import LoginPage
from app.test.selenium.pages.BookingPage import BookingPage
from app.test.selenium.pages.RegisterPage import RegisterPage
from app.test.selenium.pages.HistoryBookingPage import HistoryBookingPage
import os

def test_booking_success(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_seat()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'

def test_booking_not_login(driver):
    home=HomePage(driver=driver)
    home.open_page()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.select_login()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/login?next=/booking/13'

def test_booking_8_seat(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(8)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'

def test_booking_9_seat(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.select_n_seats(9)
    alert_msg = book.get_alert_text()
    expected_msg = "Bạn đã đạt giới hạn đặt ghế ở suất chiếu này!"
    assert alert_msg == expected_msg

def test_booking_sum_8_seat(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(5)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats_start_end(3,5)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'

def test_booking_sum_9_seat(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(5)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book()
    book.select_screening()
    book.select_screening_seat()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.select_n_seats_start_end(4,5)
    alert_msg = book.get_alert_text()
    expected_msg = "Bạn đã đạt giới hạn đặt ghế ở suất chiếu này!"
    assert alert_msg == expected_msg

def test_booking_8_seat_after_booking(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(8)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book()
    book.select_screening()
    book.select_screening_seat()
    actual_msg = book.msg_text()
    expected_msg = "Bạn đã đạt giới hạn 8 ghế cho suất chiếu này"
    assert actual_msg == expected_msg


def test_booking_seat_before_10m(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening_2()
    book.select_screening_seat()
    book.select_n_seats(3)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    alert_msg = book.get_alert_text()
    expected_msg = "Không thể đặt vé trong vòng 10 phút trước giờ chiếu!"
    assert alert_msg == expected_msg

def test_booking_after_booked(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(5)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book()
    book.select_screening()
    book.select_screening_seat()
    assert book.is_seat_holding()==True
    book.select_n_seats(1)
    assert book.is_seat_holding() == True

def test_booking_2_movie(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(8)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book2()
    book.select_screening_2()
    book.select_screening_seat()
    book.select_n_seats(8)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/12'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

def test_booking_movie_2_screening(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(8)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book()
    book.select_screening()
    book.select_screening_seat2()
    book.select_n_seats(8)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

def test_booking_after_movie_shown(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book = BookingPage(driver=driver)
    book.book()
    time.sleep(1)
    book.select_screening1()
    book.select_screening_seat()
    book.select_seat()
    time.sleep(65)

    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    alert_msg = book.get_alert_text()
    expected_msg = "Suất chiếu đã bắt đầu!"
    assert alert_msg == expected_msg

def test_booking_not_login_after_login(driver):
    home=HomePage(driver=driver)
    home.open_page()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.select_login()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/login?next=/booking/13'

    login = LoginPage(driver=driver)
    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'


def test_booking_not_login_after_register(driver):
    home=HomePage(driver=driver)
    home.open_page()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.select_login()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/login?next=/booking/13'

    book.click_register()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/register?next=/booking/13'

    avatar_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../assets/avatar-cute-3.jpg")
    )
    re = RegisterPage(driver=driver)
    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788392',
                'abc@gmail.com', 'abc123', 'Pass@123', 'Pass@123', avatar_path)

    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/login?next=/booking/13'
    login = LoginPage(driver=driver)
    login.login('user123', 'Pass@123')
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    

def test_booking_success_after_cancel_book(driver):
    h = HistoryBookingPage(driver=driver)
    h.open_page()

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
    login = LoginPage(driver=driver)
    login.open_page()
    book=BookingPage(driver=driver)
    book.book2()
    book.select_screening_2()
    book.select_screening_seat()
    time.sleep(1)
    book.select_seat_test_cancel()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/12'
    time.sleep(1)
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/'
