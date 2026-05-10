import time

from selenium.webdriver.common.by import By

from app.test.selenium.pages.BasePage import BasePage
from app.test.selenium.pages.LoginPage import LoginPage

class HistoryBookingPage(BasePage):
    def open_page(self):
        login = LoginPage(self.driver)
        login.open_page()
        login.login('user123', 'Pass@123')
        time.sleep(1)
        self.click(By.CSS_SELECTOR, '#mynavbar > div > div > a')
        self.click(By.CSS_SELECTOR, '#mynavbar > div > div > ul > li:nth-child(2) > a')
        time.sleep(1)



