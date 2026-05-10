from selenium.webdriver.common.by import By
from app.test.selenium.pages.BasePage import BasePage
import time


class BookingPage(BasePage):
    ORDER = (By.CSS_SELECTOR, '#movie-grid-container .row div:nth-child(1) .btn-group-hover a')
    SCREENING_TYPE = (By.CSS_SELECTOR, '.room-types div:nth-child(1)')
    ROOM_TYPE = (By.CSS_SELECTOR, '#menu-rooms > div > div:nth-child(2)')
    SCREENING_SEAT=(By.CSS_SELECTOR,'#menu-screenings > div > div')
    def book(self):
        btn_order = self.find(*self.ORDER)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_order)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_order)
        time.sleep(2)

    def select_screening(self):
        btn_screening = self.find(*self.SCREENING_TYPE)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_screening)
        time.sleep(2)

    def select_room(self):
        btn_room = self.find(*self.ROOM_TYPE)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_room)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_room)
        time.sleep(2)

    def select_screening_seat(self):
        btn_screening_seat = self.find(*self.SCREENING_SEAT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening_seat)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_screening_seat)
        time.sleep(2)