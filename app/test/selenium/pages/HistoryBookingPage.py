import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from app.test.selenium.pages.BasePage import BasePage
from app.test.selenium.pages.LoginPage import LoginPage

class HistoryBookingPage(BasePage):
    def open_page(self, login=False):
        if not login:
            login = LoginPage(self.driver)
            login.open_page()
            login.login('user123', 'Pass@123')
            time.sleep(1)
        self.click(By.CSS_SELECTOR, '#mynavbar > div > div > a')
        self.click(By.CSS_SELECTOR, '#mynavbar > div > div > ul > li:nth-child(2) > a')
        time.sleep(1)

    def accept_alert(self, expect):
        alert = self.driver.switch_to.alert
        assert 'Hủy vé' in alert.text
        alert.accept()
        wait = WebDriverWait(self.driver, 5)
        e = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alert')))
        assert expect in e.text



