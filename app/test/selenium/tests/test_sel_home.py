import time
from selenium.webdriver.common.by import By
from app.test.selenium.pages.HomePage import HomePage
from app.test.base_test import driver, sel_app

def test_search(driver):
    home = HomePage(driver=driver)
    home.open_page()
    kw = 'hẹn em'
    home.search(kw=kw)
    time.sleep(1)
    es = driver.find_elements(By.CLASS_NAME, 'movie-title-hover')
    assert all(kw in e.text for e in es if e.is_displayed())

def test_filter(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.filter_by_type()
    time.sleep(1)
    es = driver.find_elements(By.CLASS_NAME, 'movie-type-hover')
    for e in es:
        print(e.text)
    assert all('Gia đình' in e.text for e in es if e.is_displayed())

def test_filter_and_search(driver):
    home = HomePage(driver=driver)
    home.open_page()
    kw = 'PHÍ PHÔNG'
    home.search_filter(kw=kw)
    time.sleep(1)
    types = driver.find_elements(By.CLASS_NAME, 'movie-type-hover')
    names = driver.find_elements(By.CLASS_NAME, 'movie-title-hover')
    assert all(kw in e.text for e in names if e.is_displayed())
    assert all('Tâm lý' in e.text for e in types if e.is_displayed())

def test_scroll_to_bxh(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.click(By.CSS_SELECTOR, '#mynavbar > ul > li:nth-child(3) > a')
    time.sleep(1)

    e = driver.find_element(By.ID, 'ranking_list')
    is_visible = driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.bottom <= window.innerHeight
            );
        """, e)
    assert is_visible



