import os
import time

import pytest
from selenium.webdriver.common.by import By
from app.test.selenium.pages.ProfilePage import ProfilePage
from app.test.selenium.tests.conftest import driver, sel_app


def test_change_name_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_name(name="Đào Nguyên Sơn")
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = profile.find(By.CSS_SELECTOR, '.card-body.p-4 > div.row.g-3 > div:nth-child(1) > input')
    assert 'Đào Nguyên Sơn' in e.get_attribute('value')

def test_change_empty_name(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_name(name="")
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.NAME, 'full_name')
    assert '' in e.get_attribute('value')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

def test_change_birthday_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_birthday(birthday='15022004')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = profile.find(By.CSS_SELECTOR, '.card-body.p-4 > div.row.g-3 > div:nth-child(4) > input')
    assert '15/02/2004' in e.get_attribute('value')

def test_change_invalid_birthday_gt_100(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_birthday(birthday='11111111')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Ngày sinh không hợp lệ.' in e.text
    e = profile.find(By.NAME, 'birthday')
    assert '2004-02-15' or '2004-01-22' in e.get_attribute('value')

def test_change_invalid_birthday_lt_13(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_birthday(birthday='11112016')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Bạn phải từ 13 tuổi trở lên.' in e.text
    e = profile.find(By.NAME, 'birthday')
    assert '2004-02-15' or '2004-01-22' in e.get_attribute('value')

def test_change_empty_birthday(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_birthday(birthday="")
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.NAME, 'birthday')
    assert '' in e.get_attribute('value')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

def test_change_phone_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_phone(phone='0365900019')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = profile.find(By.CSS_SELECTOR, '.card-body.p-4 > div.row.g-3 > div:nth-child(3) > input')
    assert '0365900019' in e.get_attribute('value')

def test_change_invalid_phone(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_phone(phone='abc')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Số điện thoại không hợp lệ.' in e.text
    e = profile.find(By.NAME, 'phone')
    assert '0365900019' or '0357899305' in e.get_attribute('value')

def test_change_duplicate_phone(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_phone(phone='0357899304')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Số điện thoại đã được sử dụng bởi tài khoản khác.' in e.text
    e = profile.find(By.NAME, 'phone')
    assert '0365900019' or '0357899305' in e.get_attribute('value')

def test_change_empty_phone(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_phone(phone="")
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.NAME, 'phone')
    assert '' in e.get_attribute('value')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

def test_change_email_success(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_email(email='abcd@gmail.vn')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = profile.find(By.CSS_SELECTOR, '.card-body.p-4 > div.row.g-3 > div:nth-child(2) > input')
    assert 'abcd@gmail.vn' in e.get_attribute('value')

def test_change_invalid_email(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_email(email='abc')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.NAME, 'email')
    assert "Please include an '@' in the email address. 'abc' is missing an '@'." in e.get_attribute("validationMessage")

def test_change_duplicate_email(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_email(email='admin@gmail.com')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Email này đã được sử dụng bởi tài khoản khác.' in e.text
    e = profile.find(By.NAME, 'email')
    assert 'abcd@gmail.vn' or 'user123@gmail.com' in e.get_attribute('value')

def test_change_empty_email(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_email(email="")
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5005/user/change_profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Email không được để trống.' in e.text
    e = profile.find(By.NAME, 'email')
    assert 'abcd@gmail.vn' or 'user123@gmail.com' in e.get_attribute('value')

def test_change_avatar(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    avatar_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../assets/avatar-cute-3.jpg")
    )
    profile.change_avatar(avatar=avatar_path)
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/profile'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Cập nhật thông tin thành công!' in e.text
    e = profile.find(By.CSS_SELECTOR, '.rounded-circle')
    assert 'res.cloudinary.com' in e.get_attribute('src')

@pytest.mark.parametrize('password', [
    'A1@' * 3, 'Aa1' * 3, 'a1@' * 3, 'aA@' * 3
])
def test_change_invalid_password(driver, password):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_password(new=password, confirm=password)
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_password'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Mật khẩu phải có chữ hoa, chữ thường, kí tự đặc biệt và số' in e.text

def test_change_invalid_length_password(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_password(new='11', confirm='11')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_password'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Mật khẩu phải có ít nhất 8 ký tự' in e.text

def test_change_confirm_not_match(driver):
    profile = ProfilePage(driver=driver)
    profile.open_page()

    profile.change_password(new='11', confirm='1')
    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/user/change_password'
    e = profile.find(By.CLASS_NAME, 'alert')
    assert 'Mật khẩu xác nhận không khớp!' in e.text

