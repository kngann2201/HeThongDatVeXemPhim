import time
from selenium.webdriver.common.by import By
from app.test.selenium.pages.BasePage import BasePage
from app.test.selenium.pages.LoginPage import LoginPage


class ProfilePage(BasePage):
    NAME = (By.NAME, 'full_name')
    BIRTHDAY = (By.NAME, 'birthday')
    PHONE = (By.NAME, 'phone')
    EMAIL = (By.NAME, 'email')
    AVATAR = (By.NAME, 'avatar')
    UPDATE_BUTTON = (By.ID, 'submit-btn')
    CHANGE_INFO = (By.ID, 'change-info')
    CHANGE_PASS = (By.ID, 'change-pass')
    PASSWORD = (By.NAME, 'password')
    CONFIRM = (By.NAME, 'confirm')
    UPDATE_PASS = (By.ID, 'submit-btn')


    def open_page(self):
        login = LoginPage(driver=self.driver)
        login.open_page()
        login.login('user123', 'Pass@123')
        time.sleep(1)
        self.click(By.CSS_SELECTOR, '#mynavbar > div > div > a')
        self.click(By.CSS_SELECTOR, '#mynavbar > div > div > ul > li:nth-child(1) > a')
        time.sleep(1)

    def change_name(self, name):
        self.click(*self.CHANGE_INFO)
        time.sleep(1)
        self.find(*self.NAME).clear()
        self.typing(*self.NAME, name)
        time.sleep(1)
        self.click(*self.UPDATE_BUTTON)

    def change_birthday(self, birthday):
        self.click(*self.CHANGE_INFO)
        time.sleep(1)
        self.find(*self.BIRTHDAY).clear()
        self.typing(*self.BIRTHDAY, birthday)
        self.click(*self.UPDATE_BUTTON)

    def change_phone(self, phone):
        self.click(*self.CHANGE_INFO)
        time.sleep(1)
        self.find(*self.PHONE).clear()
        self.typing(*self.PHONE, phone)
        self.click(*self.UPDATE_BUTTON)

    def change_email(self, email):
        self.click(*self.CHANGE_INFO)
        time.sleep(1)
        self.find(*self.EMAIL).clear()
        self.typing(*self.EMAIL, email)
        self.click(*self.UPDATE_BUTTON)

    def change_avatar(self, avatar):
        self.click(*self.CHANGE_INFO)
        time.sleep(1)
        self.upload_file(*self.AVATAR, avatar)
        self.click(*self.UPDATE_BUTTON)

    def change_password(self, new, confirm):
        self.click(*self.CHANGE_PASS)
        time.sleep(1)
        self.typing(*self.PASSWORD, new)
        self.typing(*self.CONFIRM, confirm)
        self.click(*self.UPDATE_PASS)




