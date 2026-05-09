from selenium.webdriver.common.by import By

from app.test.selenium.pages.BasePage import BasePage


class LoginPage(BasePage):
    URL = 'http://127.0.0.1:5005/login'

    USERNAME = (By.NAME, 'username')
    PASSWORD = (By.NAME, 'password')
    LOGIN_BUTTON =(By.CSS_SELECTOR, '.sign-up__buttons > button')

    def open_page(self, url=URL):
        self.open(url)

    def login(self, username, password):
        self.typing(*self.USERNAME, username)
        self.typing(*self.PASSWORD, password)
        self.click(*self.LOGIN_BUTTON)
