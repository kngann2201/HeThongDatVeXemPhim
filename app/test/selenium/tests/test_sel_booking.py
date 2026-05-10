import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from app.test.base_test import driver, sel_app
from app.test.selenium.pages.LoginPage import LoginPage
from app.test.selenium.pages.BookingPage import BookingPage

def test_booking(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)

    book=BookingPage(driver=driver)
    book.book()
    book.select_screening()
    assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
