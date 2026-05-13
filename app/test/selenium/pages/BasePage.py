import time
from selenium.webdriver.support import expected_conditions as EC
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
        e.click()

    def typing(self, by, value, text):
        e = self.find(by, value)
        e.send_keys(text)

    def upload_file(self, by, value, file_path):
        self.find(by, value).send_keys(file_path)

    def set_date(self, by, value, date_value):
        self.find(by, value).send_keys(date_value)

    def get_alert_text(self):
        text = self.driver.execute_script(
            "return window.__lastAlert || '';"
        )

        if not text:
            alert = WebDriverWait(self.driver, 10).until(
                EC.alert_is_present()
            )
            text = alert.text
            alert.accept()

        text = WebDriverWait(self.driver, 10).until(alert_text)
        self.driver.execute_script("window.__lastAlert = null;")
        return text

    def accept_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()