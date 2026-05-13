import time
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoAlertPresentException,
)
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.driver.find_element(by, value)

    def finds(self, by, value):
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        e = self.find(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", e)
        time.sleep(1)
        try:
            e.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            self.driver.execute_script("arguments[0].click();", e)

    def typing(self, by, value, text):
        e = self.find(by, value)
        e.send_keys(text)

    def upload_file(self, by, value, file_path):
        self.find(by, value).send_keys(file_path)

    def set_date(self, by, value, date_value):
        self.find(by, value).send_keys(date_value)

    def get_alert_text(self):
        def alert_text(driver):
            text = driver.execute_script("return window.__lastAlert || '';")
            if text:
                return text
            try:
                alert = driver.switch_to.alert
                text = alert.text
                alert.accept()
                return text
            except NoAlertPresentException:
                return False

        text = WebDriverWait(self.driver, 10).until(alert_text)
        self.driver.execute_script("window.__lastAlert = null;")
        return text