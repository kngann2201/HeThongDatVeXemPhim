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
    payment.click_back_cancel()
    wait = WebDriverWait(driver, 15)
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
    assert ("OTP không đúng") in cancel_msg_element.text

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
    assert ("OTP không hợp lệ") in cancel_msg_element.text
