import os
import time
from selenium.webdriver.common.by import By
from app.test.selenium.pages.ProfilePage import ProfilePage
from app.test.base_test import driver, sel_app


def test_change_name_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_name(name="Đào Nguyên Sơn")
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = driver.find_element(By.CSS_SELECTOR, '.card-body.p-4 > div.row.g-3 > div:nth-child(1) > input')
    assert 'Đào Nguyên Sơn' in e.get_attribute('value')

def test_change_birthday_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_birthday(birthday='15022004')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = driver.find_element(By.CSS_SELECTOR, '.card-body.p-4 > div.row.g-3 > div:nth-child(4) > input')
    assert '15/02/2004' in e.get_attribute('value')

def test_change_invalid_birthday(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_birthday(birthday='11111111')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Ngày sinh không hợp lệ.' in e.text
    e = driver.find_element(By.NAME, 'birthday')
    assert '2004-02-15' in e.get_attribute('value')

def test_change_phone_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_phone(phone='0365900019')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = driver.find_element(By.CSS_SELECTOR, '.card-body.p-4 > div.row.g-3 > div:nth-child(3) > input')
    assert '0365900019' in e.get_attribute('value')

def test_change_invalid_phone(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_phone(phone='abc')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Số điện thoại không hợp lệ.' in e.text
    e = driver.find_element(By.NAME, 'phone')
    assert '0365900019' in e.get_attribute('value')

def test_change_duplicate_phone(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_phone(phone='0357899304')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Số điện thoại đã được sử dụng bởi tài khoản khác.' in e.text
    e = driver.find_element(By.NAME, 'phone')
    assert '0365900019' in e.get_attribute('value')

def test_change_email_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_email(email='abcd@gmail.vn')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = driver.find_element(By.CSS_SELECTOR, '.card-body.p-4 > div.row.g-3 > div:nth-child(2) > input')
    assert 'abcd@gmail.vn' in e.get_attribute('value')

def test_change_invalid_email(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_email(email='abc')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = driver.find_element(By.NAME, 'email')
    assert e.get_attribute("validationMessage") != ""

def test_change_duplicate_email(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_email(email='admin@gmail.com')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Email này đã được sử dụng bởi tài khoản khác.' in e.text
    e = driver.find_element(By.NAME, 'email')
    assert 'abcd@gmail.vn' in e.get_attribute('value')

def test_change_avatar_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    avatar_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../assets/avatar-cute-3.jpg")
    )
    profile.change_avatar(avatar=avatar_path)
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = driver.find_element(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = driver.find_element(By.CSS_SELECTOR, '.rounded-circle')
    assert 'res.cloudinary.com' in e.get_attribute('src')

