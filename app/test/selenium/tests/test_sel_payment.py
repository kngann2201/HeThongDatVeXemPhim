import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from app.test.base_test import driver, sel_app
from app.test.selenium.pages.HomePage import HomePage
from app.test.selenium.pages.LoginPage import LoginPage
from app.test.selenium.pages.BookingPage import BookingPage
from app.test.selenium.pages.PaymentPage import PaymentPage
from app.test.selenium.pages.RegisterPage import RegisterPage
from selenium.webdriver.support import expected_conditions as EC
import os


def test_payment_success(driver):
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
    assert driver.current_url == 'https://sandbox.vnpayment.vn/paymentv2/Ncb/Transaction/Confirm.html'
    payment.select_btn_confirm()
    wait = WebDriverWait(driver, 15)
    success_msg_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-card h2.text-info"))
    )
    assert "Thanh toán thành công!" in success_msg_element.text

# def test_payment_my_ticket(driver):
#     login = LoginPage(driver=driver)
#     login.open_page()
#
#     login.login('user123', 'Pass@123')
#     time.sleep(1)
#
#     assert driver.current_url == 'http://127.0.0.1:5005/'
#     wait = WebDriverWait(driver, 10)
#
#     book=BookingPage(driver=driver)
#     book.book()
#     book.select_screening()
#     book.select_screening_seat()
#     book.select_seat()
#     assert driver.current_url == 'http://127.0.0.1:5005/booking/13'
#     book.book_ticket()
#     wait = WebDriverWait(driver, 10)
#     assert driver.current_url == 'http://127.0.0.1:5005/booking/submit'
#     book.select_pay_back()
#     assert driver.current_url == 'http://127.0.0.1:5005/'
#     wait = WebDriverWait(driver, 10)
