from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from app.test.selenium.pages.BasePage import BasePage
import time


class BookingPage(BasePage):
    ORDER = (By.CSS_SELECTOR, '#movie-grid-container .row > div:nth-child(1) .btn-group-hover a')
    ORDER2 = (By.CSS_SELECTOR, '#movie-grid-container .row > div:nth-child(2) .btn-group-hover a')
    SCREENING_TYPE = (By.CSS_SELECTOR, '.room-types div:nth-child(2)')
    SCREENING_TYPE1 = (By.CSS_SELECTOR, '.room-types div:nth-child(1)')
    SCREENING_TYPE2 = (By.CSS_SELECTOR, '.room-types div:nth-child(3)')
    SCREENING_SEAT = (By.CSS_SELECTOR,'#menu-screenings > div > div:nth-child(1)')
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
        (By.CSS_SELECTOR, '#seat-map > div:nth-child(1) > div:nth-child(9)'),
    ]
    SEAT_CANCEL=(By.CSS_SELECTOR, '#seat-map > div:nth-child(4) > div:nth-child(2)')
    BUTTON_BOOK=(By.ID,'btn-submit')
    BUTTON_LOGIN=(By.CSS_SELECTOR,'#overlay-login-btn')
    BUTTON_PAYBACK=(By.CSS_SELECTOR,'.payment-card .d-grid .btn-outline-secondary')
    LIMIT_MSG=(By.CSS_SELECTOR,'#seat-map > p')
    BUTTON_REGISTER=(By.CSS_SELECTOR,'body > div.flex-grow-1 > div.login-wrapper > div > form > div.sign-up__buttons > div > a.btn--register')

    def capture_alerts(self):
        self.driver.execute_script("""
            if (!window.__alertCaptured) {
                window.__lastAlert = null;
                window.__nativeAlert = window.alert;
                window.alert = function(message) {
                    window.__lastAlert = String(message);
                };
                window.__alertCaptured = true;
            }
        """)

    def wait_for_seat_map(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, '#seat-map .seat')
            or d.find_elements(By.CSS_SELECTOR, '#seat-map > p')
            or 'd-none' not in d.find_element(By.ID, 'login-overlay').get_attribute('class')
        )

    def wait_for_screenings(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, '#menu-screenings .screening')
            or d.find_elements(By.CSS_SELECTOR, '#menu-screenings p.text-danger')
        )

    def seat_elements(self):
        return self.driver.find_elements(By.CSS_SELECTOR, '#seat-map .seat')

    def selected_seat_count(self):
        value = self.driver.execute_script("return document.getElementById('selected-seat')?.value || '';")
        return 0 if value == "" else len(value.split(","))

    def click_seat_by_index(self, index, allow_unavailable=False):
        seats = self.seat_elements()
        if index >= len(seats):
            return False

        seat = seats[index]
        class_name = seat.get_attribute('class')
        if not allow_unavailable and ('HOLDING' in class_name or 'BOOKED' in class_name):
            return False

        before = self.selected_seat_count()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seat)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", seat)

        if 'HOLDING' in class_name or 'BOOKED' in class_name:
            return False

        WebDriverWait(self.driver, 3).until(
            lambda d: d.execute_script("return window.__lastAlert || null;")
            or self.selected_seat_count() != before
        )
        return self.selected_seat_count() > before

    def click_available_seats(self, count, start=0):
        selected = 0
        index = start
        while selected < count and index < len(self.seat_elements()):
            if self.click_seat_by_index(index):
                selected += 1
            if self.driver.execute_script("return window.__lastAlert || null;"):
                break
            index += 1
        return selected

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
        self.wait_for_screenings()

    def select_screening1(self):
        btn_screening = self.find(*self.SCREENING_TYPE1)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_screening)
        self.wait_for_screenings()

    def select_screening_seat(self):
        btn_screening_seat = self.find(*self.SCREENING_SEAT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening_seat)
        time.sleep(1)
        self.capture_alerts()
        self.driver.execute_script("arguments[0].click();", btn_screening_seat)
        self.wait_for_seat_map()

    def select_screening_seat2(self):
        btn_screening_seat = self.find(*self.SCREENING_SEAT2)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening_seat)
        time.sleep(1)
        self.capture_alerts()
        self.driver.execute_script("arguments[0].click();", btn_screening_seat)
        self.wait_for_seat_map()

    def select_screening_2(self):
        btn_screening_seat = self.find(*self.SCREENING_TYPE2)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_screening_seat)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_screening_seat)
        self.wait_for_screenings()

    def select_seat(self):
        self.click_seat_by_index(0)

    def select_seat_test_cancel(self):
        seat = self.find(*self.SEAT_CANCEL)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seat)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", seat)
        time.sleep(2)

    def book_ticket(self):
        btn_submit = self.find(*self.BUTTON_BOOK)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_submit)
        time.sleep(1)
        self.capture_alerts()
        self.driver.execute_script("arguments[0].click();", btn_submit)
        time.sleep(2)

    def select_login(self):
        btn_login = self.find(*self.BUTTON_LOGIN)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_login)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_login)
        time.sleep(2)

    def select_n_seats(self, num):
        self.click_available_seats(num)

    def select_n_seats_start_end(self, num, start):
        self.click_available_seats(num, start=start)

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
        element = self.seat_elements()[0]
        class_name = element.get_attribute('class')
        if 'HOLDING' in class_name:
            return True
        return False

    def click_register(self):
        btn_order2 = self.find(*self.BUTTON_REGISTER)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_order2)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn_order2)
        time.sleep(2)