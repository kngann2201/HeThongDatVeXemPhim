import time
from selenium.webdriver.common.by import By
from app.test.selenium.pages.BasePage import BasePage
from app.test.selenium.pages.LoginPage import LoginPage


class ProfilePage(BasePage):
    URL = 'http://127.0.0.1:5005/user/change_profile'
    NAME = (By.NAME, 'full_name')
    BIRTHDAY = (By.NAME, 'birthday')
    PHONE = (By.NAME, 'phone')
    EMAIL = (By.NAME, 'email')
    AVATAR = (By.NAME, 'avatar')
    UPDATE_BUTTON = (By.ID, 'submit-btn')


    def open_page(self, url=URL):
        login = LoginPage(driver=self.driver)
        login.open_page()
        login.login('user123', 'Pass@123')
        time.sleep(1)
        self.open(url)

    def change_name(self, name):
        self.find(*self.NAME).clear()
        self.typing(*self.NAME, name)
        time.sleep(1)
        self.click(*self.UPDATE_BUTTON)

    def change_birthday(self, birthday):
        self.find(*self.BIRTHDAY).clear()
        self.typing(*self.BIRTHDAY, birthday)
        self.click(*self.UPDATE_BUTTON)

    def change_phone(self, phone):
        self.find(*self.PHONE).clear()
        self.typing(*self.PHONE, phone)
        self.click(*self.UPDATE_BUTTON)

    def change_email(self, email):
        self.find(*self.EMAIL).clear()
        self.typing(*self.EMAIL, email)
        self.click(*self.UPDATE_BUTTON)

    def change_avatar(self, avatar):
        self.upload_file(*self.AVATAR, avatar)
        self.click(*self.UPDATE_BUTTON)

