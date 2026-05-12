import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.test.selenium.tests.conftest import driver, sel_app
from app.test.selenium.pages.LoginPage import LoginPage

def test_login_success(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', 'Pass@123')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/'
    wait = WebDriverWait(driver, 10)
    el = wait.until(ec.presence_of_element_located((By.ID, 'username')))
    wait.until(lambda d: "user123" in el.get_attribute("textContent"))
    assert "user123" in el.get_attribute("textContent")

def test_login_wrong_password(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user123', '1')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/login'
    e = login.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Tên đăng nhập hoặc mật khẩu không đúng' in e.text

def test_login_wrong_username(driver):
    login = LoginPage(driver=driver)
    login.open_page()

    login.login('user1', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/login'
    e = login.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Tên đăng nhập hoặc mật khẩu không đúng' in e.text

def test_login_from_booking(driver):
    login = LoginPage(driver)
    login.open_page(url='http://127.0.0.1:5005/login?next=/booking/12')

    login.login('user123', 'Pass@123')
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/booking/12'
