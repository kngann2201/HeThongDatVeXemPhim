import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from app.test.selenium.pages.HomePage import HomePage
from app.test.selenium.pages.LoginPage import LoginPage
from app.test.selenium.pages.BookingPage import BookingPage
from app.test.selenium.pages.PaymentPage import PaymentPage
from app.test.selenium.pages.HistoryBookingPage import HistoryBookingPage
from selenium.webdriver.support import expected_conditions as EC
import os


def test_payment_success(driver):

    payment = PaymentPage(driver=driver)
    payment.open_payment()
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

def test_payment_success_my_ticket(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.click_pay_back()
    wait = WebDriverWait(driver, 10)
    payment.open_history()
    wait = WebDriverWait(driver, 10)
    payment.click_pay_my_ticket()

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

def test_cancel_payment_type(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    wait = WebDriverWait(driver, 10)
    payment.click_back_cancel()
    wait = WebDriverWait(driver, 10)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-card h2.text-danger"))
    )
    assert "Thanh toán thất bại!" in cancel_msg_element.text

def test_cancel_payment(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.click_cancel()
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-card h2.text-danger"))
    )
    assert "Thanh toán thất bại!" in cancel_msg_element.text

def test_cancel_payment_otp(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.card_number('9704198526191432198')
    payment.card_holder('NGUYEN VAN A')
    payment.card_date('07/15')
    payment.select_btn_continue()
    payment.select_btn_agree()
    payment.click_cancel_otp()
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-card h2.text-danger"))
    )
    assert "Thanh toán thất bại!" in cancel_msg_element.text

def test_invalid_card_number(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.card_number('970419852619143219')
    payment.card_holder('NGUYEN VAN A')
    payment.card_date('07/15')
    payment.select_btn_continue()
    payment.select_btn_agree()
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.ID, "lb_message_error"))
    )
    assert "Số thẻ không hợp lệ" in cancel_msg_element.text

def test_invalid_card_holder(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.card_number('9704198526191432198')
    payment.card_holder('NGUYEN VAN')
    payment.card_date('07/15')
    payment.select_btn_continue()
    payment.select_btn_agree()
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.ID, "lb_message_error"))
    )
    assert "Thông tin thẻ không đúng" in cancel_msg_element.text

def test_invalid_card_date(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.card_number('9704198526191432198')
    payment.card_holder('NGUYEN VAN A')
    payment.card_date('07/10')
    payment.select_btn_continue()
    payment.select_btn_agree()
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.ID, "lb_message_error"))
    )
    assert "Thông tin thẻ không đúng" in cancel_msg_element.text

def test_invalid_3(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.card_number('9704198526191432198')
    payment.card_holder('NGUYEN VAN A')
    payment.card_date('07/10')
    payment.select_btn_continue()
    payment.select_btn_agree()
    payment.select_btn_continue()
    payment.select_btn_continue()
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.ID, "lb_message_error"))
    )
    assert ("Quý khách đã bị sai thông tin thanh toán quá số lần cho phép (3 lần). "
            "Quý khách vui lòng thực hiện lại giao dịch khác") in cancel_msg_element.text

def test_invalid_otp_fail(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.card_number('9704198526191432198')
    payment.card_holder('NGUYEN VAN A')
    payment.card_date('07/15')
    payment.select_btn_continue()
    payment.select_btn_agree()
    payment.otp_value('123459')
    payment.select_btn_confirm()
    assert driver.current_url == 'https://sandbox.vnpayment.vn/paymentv2/Ncb/Transaction/Confirm.html'
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.ID, "lb_message_error"))
    )
    assert "OTP không đúng" in cancel_msg_element.text

def test_invalid_otp(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.select_payment_now()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    payment.card_number('9704198526191432198')
    payment.card_holder('NGUYEN VAN A')
    payment.card_date('07/15')
    payment.select_btn_continue()
    payment.select_btn_agree()
    payment.otp_value('12345')
    assert driver.current_url == 'https://sandbox.vnpayment.vn/paymentv2/Ncb/Transaction/Confirm.html'
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#parsley-id-5 > li"))
    )
    assert "OTP không hợp lệ" in cancel_msg_element.text

def test_payment_1_movie_2_bill(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.click_pay_back()
    wait = WebDriverWait(driver, 10)

    book = BookingPage(driver=driver)
    book.book()
    book.select_screening()
    book.select_screening_seat2()
    book.select_n_seats_start_end(3,4)
    book.book_ticket()
    wait = WebDriverWait(driver, 10)

    payment.click_pay_back()
    wait = WebDriverWait(driver, 10)
    payment.open_history()
    wait = WebDriverWait(driver, 10)
    payment.click_pay_my_ticket()
    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.ID, "totalAmountDt"))
    )
    assert "300.000" in cancel_msg_element.text

def test_payment_after_cancel(driver):
    payment = PaymentPage(driver=driver)
    payment.open_payment()
    payment.click_pay_back()
    wait = WebDriverWait(driver, 10)

    payment.open_history()
    wait = WebDriverWait(driver, 10)
    h = HistoryBookingPage(driver=driver)

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(5) .text-end .text-danger')
    assert price_b.text == '300,000đ'

    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(5) .bg-white')
    time.sleep(1)
    h.click(By.CSS_SELECTOR, '#collapse5 tr:nth-child(2) > td:nth-child(6) .btn-danger')
    h.accept_alert(expect='Hủy vé thành công!')

    price_b = h.find(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(5) .text-end .text-danger')
    assert price_b.text == '200,000đ'
    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(5) .bg-white')
    time.sleep(1)
    e = h.find(By.CSS_SELECTOR, '#collapse5 .ticket-cancelled > td:nth-child(5) > span')
    assert 'Đã hủy' in e.text
    payment.click_pay_my_ticket()

    payment.select_payment_type()
    payment.search_payment_type('NCB')
    payment.select_NCB()
    wait = WebDriverWait(driver, 15)
    cancel_msg_element = wait.until(
        EC.visibility_of_element_located((By.ID, "totalAmountDt"))
    )
    assert "200.000" in cancel_msg_element.text

def test_payment_my_ticket(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/'

    payment = PaymentPage(driver=driver)
    payment.open_history()
    h = HistoryBookingPage(driver=driver)
    h.click(By.CSS_SELECTOR, '#accordionBooking > div:nth-child(4) .bg-white')
    time.sleep(1)
    payment.click_pay_my_ticket_cancel()

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
    assert "Ghế đã bị huỷ trong khi thanh toán!" in success_msg_element.text
