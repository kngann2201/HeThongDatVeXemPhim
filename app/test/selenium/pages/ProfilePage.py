import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
        WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url == 'http://127.0.0.1:5005/'
        )
        self.open('http://127.0.0.1:5005/user/profile')
        WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url == 'http://127.0.0.1:5005/user/profile'
        )

    def open_change_profile(self):
        self.open('http://127.0.0.1:5005/user/change_profile')
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*self.NAME)
        )

    def open_change_password(self):
        self.open('http://127.0.0.1:5005/user/change_password')
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*self.PASSWORD)
        )

    def submit_form(self):
        button = self.find(*self.UPDATE_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)

    def set_value(self, locator, value):
        element = self.find(*locator)
        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, element, value)

    def change_name(self, name):
        self.open_change_profile()
        self.set_value(self.NAME, name)
        time.sleep(1)
        self.submit_form()

    def change_birthday(self, birthday):
        self.open_change_profile()
        if birthday:
            birthday = f"{birthday[4:8]}-{birthday[2:4]}-{birthday[0:2]}"
        self.set_value(self.BIRTHDAY, birthday)
        self.submit_form()

    def change_phone(self, phone):
        self.open_change_profile()
        self.set_value(self.PHONE, phone)
        self.submit_form()

    def change_email(self, email):
        self.open_change_profile()
        self.set_value(self.EMAIL, email)
        self.submit_form()

    def change_avatar(self, avatar):
        self.open_change_profile()
        self.upload_file(*self.AVATAR, avatar)
        self.submit_form()

    def change_password(self, new, confirm):
        self.open_change_password()
        self.set_value(self.PASSWORD, new)
        self.set_value(self.CONFIRM, confirm)
        self.submit_form()




