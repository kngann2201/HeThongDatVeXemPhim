from selenium.webdriver.common.by import By

from app.test.selenium.pages.BasePage import BasePage


class RegisterPage(BasePage):
    URL = 'http://127.0.0.1:5000/register'

    NAME = (By.NAME, 'full_name')
    BIRTHDAY = (By.NAME, 'birthday')
    PHONE = (By.NAME, 'phone')
    EMAIL = (By.NAME, 'email')
    USERNAME = (By.NAME, 'username')
    PASSWORD = (By.NAME, 'password')
    CONFIRM = (By.NAME, 'confirm_password')
    AVATAR = (By.NAME, 'avatar')
    REGISTER_BUTTON =(By.ID, 'submit-btn')

    def open_page(self, url=URL):
        self.open(url)

    def register(self, name, birthday, phone, email, username, password, confirm, avatar=None):
        self.typing(*self.NAME, name)
        self.set_date(*self.BIRTHDAY, birthday)
        self.typing(*self.PHONE, phone)
        self.typing(*self.EMAIL, email)
        self.typing(*self.USERNAME, username)
        self.typing(*self.PASSWORD, password)
        self.typing(*self.CONFIRM, confirm)
        if avatar is not None:
            self.upload_file(*self.AVATAR, avatar)
        self.click(*self.REGISTER_BUTTON)
