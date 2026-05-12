from app.test.selenium.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
import time

class PaymentPage(BasePage):
    BUTTON_VNPAY_NOW=(By.CSS_SELECTOR,'.payment-card .d-grid .btn-vnpay')
    BUTTON_PAYMENT_TYPE=(By.CSS_SELECTOR,'#accordionList div:nth-child(2) .list-method-button')
    SEARCH=(By.ID,'searchPayMethod2')
    BUTTON_NCB=(By.CSS_SELECTOR,'#NCB > div')
    CARD_NUMBER=(By.ID,'card_number_mask')
    CARD_HOLDER=(By.ID,'cardHolder')
    CARD_DATE=(By.ID,'cardDate')
    BUTTON_CONTINUE=(By.ID,'btnContinue')
    BUTTON_AGREE=(By.ID,'btnAgree')
    OTP=(By.ID,'otpvalue')
    BUTTON_CONFIRM=(By.ID,'btnConfirm')
    def select_payment_now(self):
        btn_vnpay_now = self.find(*self.BUTTON_VNPAY_NOW)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_vnpay_now)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_vnpay_now)
        time.sleep(2)
    def select_payment_type(self):
        btn_vnpay_type = self.find(*self.BUTTON_PAYMENT_TYPE)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_vnpay_type)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_vnpay_type)
        time.sleep(2)
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