from selenium.webdriver.common.by import By

from app.test.base_test import driver
from app.test.selenium.pages.BasePage import BasePage
import time


class BookingPage(BasePage):
    ORDER = (By.CSS_SELECTOR, '#movie-grid-container .row > div:nth-child(1) .btn-group-hover a')
    ORDER2 = (By.CSS_SELECTOR, '#movie-grid-container .row > div:nth-child(2) .btn-group-hover a')
    SCREENING_TYPE = (By.CSS_SELECTOR, '.room-types div:nth-child(2)')
    SCREENING_TYPE2 = (By.CSS_SELECTOR, '.room-types div:nth-child(3)')
    SCREENING_SEAT=(By.CSS_SELECTOR,'#menu-screenings > div > div:nth-child(1)')
    SCREENING_SEAT2 = (By.CSS_SELECTOR, '#menu-screenings > div > div:nth-child(2)')

    SEATS = [
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(1)'),
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(2)'),
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(3)'),
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(4)'),
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(5)'),
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(6)'),
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(7)'),
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(8)'),
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(9)')
    ]
    BUTTON_BOOK=(By.ID,'btn-submit')
    BUTTON_LOGIN=(By.CSS_SELECTOR,'#overlay-login-btn')
    BUTTON_PAYBACK=(By.CSS_SELECTOR,'.payment-card .d-grid .btn-outline-secondary')
    LIMIT_MSG=(By.CSS_SELECTOR,'#seat-map > p')

    def book(self):
        btn_order = self.find(*self.ORDER)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_order)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_order)
        time.sleep(2)

    def book2(self):
        btn_order2 = self.find(*self.ORDER2)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_order2)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_order2)
        time.sleep(2)

    def select_screening(self):
        btn_screening = self.find(*self.SCREENING_TYPE)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_screening)
        time.sleep(2)

    def select_screening_seat(self):
        btn_screening_seat = self.find(*self.SCREENING_SEAT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening_seat)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_screening_seat)
        time.sleep(2)

    def select_screening_seat2(self):
        btn_screening_seat = self.find(*self.SCREENING_SEAT2)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening_seat)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_screening_seat)
        time.sleep(2)

    def select_screening_2(self):
        btn_screening_seat = self.find(*self.SCREENING_TYPE2)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening_seat)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_screening_seat)
        time.sleep(2)

    def select_seat(self):
        btn_seat = self.find(*self.SEATS[0])
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_seat)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_seat)
        time.sleep(2)

    def book_ticket(self):
        btn_submit = self.find(*self.BUTTON_BOOK)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_submit)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_submit)
        time.sleep(2)

    def select_login(self):
        btn_login = self.find(*self.BUTTON_LOGIN)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_login)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_login)
        time.sleep(2)

    def select_n_seats(self, num):
        for i in range(num):
            seat_selector = self.SEATS[i]
            btn_seat = self.find(*seat_selector)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_seat)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", btn_seat)

    def select_n_seats_start_end(self, num, start):
        for i in range(start,start + num):
            seat_selector = self.SEATS[i]
            btn_seat = self.find(*seat_selector)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_seat)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", btn_seat)

    def select_pay_back(self):
        btn_login = self.find(*self.BUTTON_PAYBACK)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_login)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_login)
        time.sleep(2)

    def msg_text(self):
        element = self.find(*self.LIMIT_MSG)
        return element.text.strip()

    def is_seat_holding(self):
        element = self.find(*self.SEATS[0])
        class_name = element.get_attribute('class')
        if 'HOLDING' in class_name:
            return True
        return False
