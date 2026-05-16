from app.test.selenium.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from app.test.selenium.pages.LoginPage import LoginPage
from app.test.selenium.pages.BookingPage import BookingPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PaymentPage(BasePage):
    BUTTON_VNPAY_NOW=(By.CSS_SELECTOR,'.payment-card .d-grid .btn-vnpay')
    BUTTON_PAYMENT_TYPE=(By.CSS_SELECTOR,'#accordionList > div:nth-child(2) > div.list-method-button > div')
    SEARCH=(By.ID,'searchPayMethod2')
    BUTTON_NCB=(By.CSS_SELECTOR,'#NCB > div')
    CARD_NUMBER=(By.ID,'card_number_mask')
    CARD_HOLDER=(By.ID,'cardHolder')
    CARD_DATE=(By.ID,'cardDate')
    BUTTON_CONTINUE=(By.ID,'btnContinue')
    BUTTON_AGREE=(By.ID,'btnAgree')
    OTP=(By.ID,'otpvalue')
    BUTTON_CONFIRM=(By.ID,'btnConfirm')
    BUTTON_PAY=(By.CSS_SELECTOR,'#accordionBooking > div:nth-child(5) > div.d-flex.align-items-center.bg-white > div > a')
    BUTTON_PAY_CANCEL = (By.CSS_SELECTOR, '#accordionBooking div:nth-child(4)  > div.d-flex.align-items-center.bg-white > div > a')
    BUTTON_BACK=(By.CSS_SELECTOR,'.header-desktop > div > div:nth-child(1) > a > div > span.ubtn-text')
    BUTTON_CANCEL_CONFIRM=(By.CSS_SELECTOR,'#modalCancelPayment > div > div > div.modal-footer.justify-content-center > div > div:nth-child(2) > a > div > span')
    BUTTON_CANCEL=(By.CSS_SELECTOR,'#cardVerify .hide-on-qr-show .ubtn-group div:nth-child(1) > a')
    BUTTON_CANCEL_OTP=(By.CSS_SELECTOR,'#otpConfirm div:nth-child(3) div:nth-child(1) > a > div > span')

    def open_payment(self):
        login = LoginPage(self.driver)
        login.open_page()

        login.login('user123', 'Pass@123')
        time.sleep(1)

        book = BookingPage(self.driver)
        book.book()
        book.select_screening()
        book.select_screening_seat2()
        book.select_n_seats(3)
        book.book_ticket()

    def open_payment_2(self):
        login = LoginPage(self.driver)
        login.open_page()

        login.login('user123', 'Pass@123')
        time.sleep(1)

        book = BookingPage(self.driver)
        book.book()
        book.select_screening()
        book.select_screening_seat2()
        book.select_n_seats(3)
        book.book_ticket()

    def open_history(self):
        self.click(By.CSS_SELECTOR, '#mynavbar > div > div > a')
        time.sleep(1)
        self.click(By.CSS_SELECTOR, '#mynavbar > div > div > ul > li:nth-child(2) > a')

    def select_payment_now(self):
        btn_vnpay_now = self.find(*self.BUTTON_VNPAY_NOW)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_vnpay_now)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_vnpay_now)
        time.sleep(2)

    def select_payment_type(self):
        wait = WebDriverWait(self.driver, 10)
        btn_vnpay_type = wait.until(EC.element_to_be_clickable(self.BUTTON_PAYMENT_TYPE))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_vnpay_type)
        self.driver.execute_script("arguments[0].click();", btn_vnpay_type)

    def search_payment_type(self,value):
        self.typing(*self.SEARCH,value)

    def select_NCB(self):
        btn_NCB = self.find(*self.BUTTON_NCB)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_NCB)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_NCB)
        time.sleep(2)

    def card_number(self, value):
        self.typing(*self.CARD_NUMBER,value)

    def card_holder(self, value):
        self.typing(*self.CARD_HOLDER,value)

    def card_date(self, value):
        self.typing(*self.CARD_DATE,value)

    def select_btn_continue(self):
        btn_continue = self.find(*self.BUTTON_CONTINUE)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_continue)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_continue)
        time.sleep(2)

    def select_btn_agree(self):
        btn_agree = self.find(*self.BUTTON_AGREE)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_agree)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_agree)
        time.sleep(2)

    def otp_value(self, value):
        self.typing(*self.OTP, value)

    def select_btn_confirm(self):
        btn_confirm = self.find(*self.BUTTON_CONFIRM)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_confirm)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_confirm)
        time.sleep(2)

    def click_pay_my_ticket(self):
        wait = WebDriverWait(self.driver, 10)
        btn_pay = wait.until(EC.presence_of_element_located(self.BUTTON_PAY))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_pay)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_pay)

    def click_pay_my_ticket_cancel(self):
        btn_pay = self.find(*self.BUTTON_PAY_CANCEL)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_pay)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_pay)
        time.sleep(2)

    def click_pay_back(self):
        book = BookingPage(self.driver)
        book.select_pay_back()

    def click_back_cancel(self):
        btn_back = self.find(*self.BUTTON_BACK)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_back)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_back)
        time.sleep(2)
        btn_cancel_confirm = self.find(*self.BUTTON_CANCEL_CONFIRM)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_cancel_confirm)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_cancel_confirm)
        time.sleep(2)

    def click_cancel(self):
        btn_cancel = self.find(*self.BUTTON_CANCEL)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_cancel)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_cancel)
        time.sleep(2)
        btn_cancel_confirm = self.find(*self.BUTTON_CANCEL_CONFIRM)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_cancel_confirm)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_cancel_confirm)
        time.sleep(2)

    def click_cancel_otp(self):
        btn_cancel = self.find(*self.BUTTON_CANCEL_OTP)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_cancel)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_cancel)
        time.sleep(2)
        btn_cancel_confirm = self.find(*self.BUTTON_CANCEL_CONFIRM)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_cancel_confirm)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_cancel_confirm)
        time.sleep(2)