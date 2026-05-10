import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from app.test.base_test import driver, sel_app
from app.test.selenium.pages.HomePage import HomePage
from app.test.selenium.pages.LoginPage import LoginPage
from app.test.selenium.pages.BookingPage import BookingPage

def test_booking_success(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_seat()
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'

def test_booking_not_login(driver):
    home=HomePage(driver=driver)
    home.open_page()
    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.select_login()
    assert driver.current_url == 'http://127.0.0.1:5005/login?next=/booking/13'
    wait = WebDriverWait(driver, 10)

def test_booking_8_seat(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(8)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'

def test_booking_9_seat(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
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

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(5)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats_start_end(3,5)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'


def test_booking_sum_9_seat(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(5)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book()
    book.select_screening()
    book.select_screening_seat()
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

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(8)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
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

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening_2()
    book.select_screening_seat()
    book.select_n_seats(3)
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

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(5)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
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

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(8)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book2()
    book.select_screening_2()
    book.select_screening_seat()
    book.select_n_seats(8)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/12'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    assert driver.current_url == 'http://127.0.0.1:5005/'

def test_booking_movie_2_screening(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat()
    book.select_n_seats(8)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    assert driver.current_url == 'http://127.0.0.1:5005/'

    book.book()
    book.select_screening()
    book.select_screening_seat2()
    book.select_n_seats(8)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
    book.book_ticket()
    wait = WebDriverWait(driver, 10)
    assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
    book.select_pay_back()
    assert driver.current_url == 'http://127.0.0.1:5005/'


