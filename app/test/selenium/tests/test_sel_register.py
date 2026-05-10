import os
import time

import pytest
from selenium.webdriver.common.by import By
from app.test.base_test import driver, sel_app
from app.test.selenium.pages.RegisterPage import RegisterPage

def test_register_success(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    avatar_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../assets/avatar-cute-3.jpg")
    )
    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788392',
                'abc@gmail.com', 'abc123', 'Pass@123', 'Pass@123', avatar_path)

    time.sleep(1)
    assert driver.current_url == 'http://127.0.0.1:5005/login'

def test_register_empty_name(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('', '130512005', 'abc',
                'abcd@gmail.com', 'abc123', '11', '11', None)
    time.sleep(1)
    e = re.find(By.NAME, 'full_name')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

def test_register_invalid_birthday(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13051922', '0926788391',
                'abcd@gmail.com', 'abc123', '11', '11', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Ngày sinh không hợp lệ' in e.text

def test_register_empty_birthday(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '', '0926788391',
                'abcd@gmail.com', 'abc123', '11', '11', None)
    time.sleep(1)
    e = re.find(By.NAME, 'birthday')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

def test_register_invalid_phone(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '130512005', 'abc',
                'abcd@gmail.com', 'abc123', '11', '11', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Số điện thoại không hợp lệ' in e.text

def test_register_empty_phone(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '130512005', '',
                'abcd@gmail.com', 'abc123', '11', '11', None)
    time.sleep(1)
    e = re.find(By.NAME, 'phone')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

def test_register_invalid_email(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail', 'abc123', '11', '11', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Không đúng định dạng hoặc email đã tồn tại' in e.text

def test_register_empty_email(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                '', 'abc123', '11', '11', None)
    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Tất cả các trường thông tin đều là bắt buộc.' in e.text

def test_register_invalid_username(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail.com', 'abc', '11', '11', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Username phải từ 6 kí tự trở lên' in e.text

def test_register_empty_username(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail.com', '', '11', '11', None)
    time.sleep(1)
    e = re.find(By.NAME, 'username')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

@pytest.mark.parametrize('password', [
    'A1@' * 3, 'Aa1' * 3, 'a1@' * 3, 'aA@' * 3
])
def test_register_invalid_format_password(driver, password):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail.com', 'abc1234', password, password, None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Mật khẩu phải có chữ hoa, chữ thường, kí tự đặc biệt và số' in e.text

def test_register_invalid_length_password(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail.com', 'abc1234', '11', '11', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Mật khẩu phải có ít nhất 8 ký tự' in e.text

def test_register_confirm_not_match(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail.com', 'abc1234', '11111111', '20052005', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Mật khẩu không khớp!!' in e.text

def test_register_empty_password(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail.com', 'abc1234', '', '', None)
    time.sleep(1)
    e = re.find(By.NAME, 'password')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

def test_register_empty_confirm(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail.com', 'abc1234', '11111111', '', None)
    time.sleep(1)
    e = re.find(By.NAME, 'confirm_password')
    assert "Please fill out this field." in e.get_attribute("validationMessage")

def test_register_duplicate_phone(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788392',
                'abcd@gmail.com', 'abc1234', '11', '11', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Số điện thoại đã được sử dụng' in e.text

def test_register_duplicate_email(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abc@gmail.com', 'abc1234', '11111111', '11111111', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Không đúng định dạng hoặc email đã tồn tại' in e.text

def test_register_duplicate_username(driver):
    re = RegisterPage(driver=driver)
    re.open_page()

    re.register('Bùi Nguyễn Thuý Ngân', '13052005', '0926788391',
                'abcd@gmail.com', 'abc123', '11', '11', None)

    time.sleep(1)
    e = re.find(By.CSS_SELECTOR, 'body > div.flex-grow-1 > div.container.mt-3 > div')
    assert 'Tên đăng nhập đã tồn tại' in e.text





