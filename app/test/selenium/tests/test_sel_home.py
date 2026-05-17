import time
from app.test.selenium.pages.LoginPage import LoginPage
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from app.test.selenium.pages.HomePage import HomePage
from app.test.selenium.tests.conftest import driver, sel_app


def test_all_movie(driver):
    home = HomePage(driver=driver)
    home.open_page()
    count = 0

    e = home.find(By.CLASS_NAME, 'pagination')
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", e)
    time.sleep(1)

    for i in range(1, 5):
        p = home.find(By.CSS_SELECTOR, f'#movie-grid-container > nav > ul > li:nth-child({i}) > a')
        p.click()
        time.sleep(1)
        els = home.finds(By.CSS_SELECTOR, '#movie-grid-container .movie-card-minimal')
        count += len(els)
    assert count == 13

def test_pagination_enough(driver):
    home = HomePage(driver=driver)
    home.open_page()

    home.click(By.CSS_SELECTOR, '#movie-grid-container > nav > ul > li:nth-child(2) > a')
    time.sleep(1)
    els = home.finds(By.CSS_SELECTOR, '#movie-grid-container .movie-card-minimal')
    assert len(els) == 4

def test_pagination_not_enough(driver):
    home = HomePage(driver=driver)
    home.open_page()

    home.click(By.CSS_SELECTOR, '.pagination > li.page-item:last-child a.page-link')
    time.sleep(1)
    els = home.finds(By.CSS_SELECTOR, '#movie-grid-container .movie-card-minimal')
    assert len(els) == 1

def test_search(driver):
    home = HomePage(driver=driver)
    home.open_page()
    kw = 'hẹn em'
    home.search(kw=kw)
    time.sleep(1)
    es = home.finds(By.CLASS_NAME, 'movie-title-hover')
    assert all(kw in e.text for e in es if e.is_displayed())

def test_search_movie_no_result(driver):
    home = HomePage(driver=driver)
    home.open_page()

    kw = "absbhjdfasjtd"
    home.search(kw=kw)
    time.sleep(1)
    assert home.find(By.CSS_SELECTOR, '.container.mt-4 > div > p').text == 'Tìm thấy 0 phim phù hợp'
    assert home.find(By.CSS_SELECTOR, '.container.mt-4 h4').text == 'Không tìm thấy phim nào khớp với yêu cầu'

def test_filter(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.filter_by_type()
    time.sleep(1)
    es = home.finds(By.CLASS_NAME, 'movie-type-hover')
    for e in es:
        print(e.text)
    assert all('Gia đình' in e.text for e in es if e.is_displayed())

def test_filter_no_result(driver):
    home = HomePage(driver=driver)
    home.open_page()

    home.filter_by_type_no_movie()
    time.sleep(1.2)
    assert home.find(By.CSS_SELECTOR, '.container.mt-4 > div > p').text == 'Tìm thấy 0 phim phù hợp'
    assert home.find(By.CSS_SELECTOR, '.container.mt-4 h4').text == 'Không tìm thấy phim nào khớp với yêu cầu'


def test_filter_and_search(driver):
    home = HomePage(driver=driver)
    home.open_page()
    kw = 'PHÍ PHÔNG'
    home.search_filter(kw=kw)
    time.sleep(1)
    types = home.finds(By.CLASS_NAME, 'movie-type-hover')
    names = home.finds(By.CLASS_NAME, 'movie-title-hover')
    assert all(kw in e.text for e in names if e.is_displayed())
    assert all('Kinh dị' in e.text for e in types if e.is_displayed())

def test_filter_and_search_no_result(driver):
    home = HomePage(driver=driver)
    home.open_page()
    kw = 'bsdfkyja'
    home.search_filter(kw=kw)
    time.sleep(1)
    m_type = home.find(By.CSS_SELECTOR, '.fs-5.text-secondary.text-uppercase span')
    name = home.find(By.CSS_SELECTOR, '.container.mt-4 .mb-2 span')
    assert m_type.text.lower() == 'Kinh dị'.lower()
    assert name.text == kw
    assert home.find(By.CSS_SELECTOR, '.container.mt-4 > div > p').text == 'Tìm thấy 0 phim phù hợp'
    assert home.find(By.CSS_SELECTOR, '.container.mt-4 h4').text == 'Không tìm thấy phim nào khớp với yêu cầu'

def test_scroll_to_bxh(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.go_to_ranking()
    time.sleep(1)

    e = home.find(By.ID, 'ranking_list')
    is_visible = driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            return (
                rect.top < window.innerHeight &&
                rect.bottom > 0
            );
        """, e)
    assert is_visible

def test_click_booking(driver):
    home = HomePage(driver=driver)
    home.open_page()

    e = home.find(By.CSS_SELECTOR, '.movie-slider .slick-slide.slick-active .movie-card-minimal')
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", e)
    ActionChains(driver).move_to_element(e).perform()
    name = home.find(By.CSS_SELECTOR, '.movie-slider .slick-slide.slick-active h6.movie-title-hover').text
    btn = home.find(By.CSS_SELECTOR, '.movie-slider .slick-slide.slick-active .btn-red')
    href = btn.get_attribute('href')
    btn.click()
    time.sleep(1)
    assert driver.current_url == href
    movie_name = driver.find_element(By.CLASS_NAME, 'movie-title')
    assert movie_name.text == name

def test_click_booking_from_bxh(driver):
    home = HomePage(driver=driver)
    home.open_page()

    home.go_to_ranking()
    time.sleep(1)
    name = home.find(By.CSS_SELECTOR, '#ranking_list  tr:nth-child(1) > td:nth-child(2) h6').text
    btn = home.find(By.CSS_SELECTOR, '#ranking_list tr:nth-child(1) > td:nth-child(5) > a')
    href = btn.get_attribute('href')
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)
    assert driver.current_url == href
    movie_name = driver.find_element(By.CLASS_NAME, 'movie-title')
    assert movie_name.text == name

def test_click_login(driver):
    home = HomePage(driver=driver)
    home.open_page()

    e = home.find(By.CLASS_NAME, 'btn-outline-light')
    href = e.get_attribute('href')
    e.click()
    time.sleep(1)
    assert driver.current_url == href

def test_click_register(driver):
    home = HomePage(driver=driver)
    home.open_page()

    e = home.find(By.CLASS_NAME, 'btn-danger')
    href = e.get_attribute('href')
    e.click()
    time.sleep(1)
    assert driver.current_url == href

def test_click_profile(driver):
    home = HomePage(driver=driver)
    home.open_page()

    try:
        e = home.find(By.CLASS_NAME, 'btn-outline-light')
        e.click()
        time.sleep(1)

        login = LoginPage(driver=driver)
        login.login('user123', 'Pass@123')
        time.sleep(1)
    finally:
        home.click_user_menu_item('#mynavbar > div > div > ul > li:nth-child(1) > a')
        time.sleep(1)
        assert driver.current_url == 'http://127.0.0.1:5005/user/profile'

def test_click_history_ticket(driver):
    home = HomePage(driver=driver)
    home.open_page()

    try:
        e = home.find(By.CLASS_NAME, 'btn-outline-light')
        e.click()
        time.sleep(1)

        login = LoginPage(driver=driver)
        login.login('user123', 'Pass@123')
        time.sleep(1)
    finally:
        home.click_user_menu_item('#mynavbar > div > div > ul > li:nth-child(2) > a')
        time.sleep(1)
        assert driver.current_url == 'http://127.0.0.1:5005/user/history_booking'

def test_click_history_watched(driver):
    home = HomePage(driver=driver)
    home.open_page()

    try:
        e = home.find(By.CLASS_NAME, 'btn-outline-light')
        e.click()
        time.sleep(1)

        login = LoginPage(driver=driver)
        login.login('user123', 'Pass@123')
        time.sleep(1)
    finally:
        home.click_user_menu_item('#mynavbar > div > div > ul > li:nth-child(3) > a')
        time.sleep(1)
        assert driver.current_url == 'http://127.0.0.1:5005/user/history_watched'

def test_click_log_out(driver):
    home = HomePage(driver=driver)
    home.open_page()

    try:
        e = home.find(By.CLASS_NAME, 'btn-outline-light')
        e.click()
        time.sleep(1)

        login = LoginPage(driver=driver)
        login.login('user123', 'Pass@123')
        time.sleep(1)
    finally:
        home.click_user_menu_item('#mynavbar > div > div > ul > li:last-child > a')
        time.sleep(1)
        assert driver.current_url == 'http://127.0.0.1:5005/login'

def test_back_to_top(driver):
    home = HomePage(driver=driver)
    home.open_page()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    e = home.find(By.ID, 'backToTopBtn')
    e.click()
    time.sleep(1)
    top = home.find(By.CSS_SELECTOR, 'div.flex-grow-1 > div.container.mt-4 > div:nth-child(1)')
    is_visible = driver.execute_script("""
                const rect = arguments[0].getBoundingClientRect();
                return (
                    rect.top >= 0 &&
                    rect.bottom <= window.innerHeight
                );
            """, top)
    assert is_visible








