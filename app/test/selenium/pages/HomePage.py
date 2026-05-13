from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from app.test.selenium.pages.BasePage import BasePage


class HomePage(BasePage):
    URL = 'http://127.0.0.1:5005/'
    SEARCH = (By.NAME, 'kw')
    TYPE_LIST = (By.ID, 'navbarDropdown')
    MOVIE_TYPE_1 = (By.CSS_SELECTOR, '#mynavbar > ul > li.nav-item.dropdown > ul > li:first-child > a')
    MOVIE_TYPE_2 = (By.CSS_SELECTOR, '#mynavbar > ul > li.nav-item.dropdown > ul > li:last-child > a')

    def open_page(self, url=URL):
        self.open(url)

    def filter_by_type(self):
        self.find(*self.TYPE_LIST).click()
        self.find(*self.MOVIE_TYPE_1).click()

    def filter_by_type_no_movie(self):
        self.find(*self.TYPE_LIST).click()
        self.find(*self.MOVIE_TYPE_2).click()

    def search(self, kw):
        e = self.find(*self.SEARCH)
        e.send_keys(kw)
        e.send_keys(Keys.RETURN)

    def search_filter(self, kw):
        self.filter_by_type()
        self.search(kw)

    def go_to_ranking(self):
        self.click(By.CSS_SELECTOR, '#mynavbar > ul > li:nth-child(3) > a')
        ranking = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.ID, 'ranking_list')
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ranking)
        return ranking

    def click_user_menu_item(self, item_selector):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(By.ID, 'username')
        )
        toggle = self.find(By.CSS_SELECTOR, '#mynavbar > div > div > a')
        self.driver.execute_script("arguments[0].click();", toggle)

        item = self.find(By.CSS_SELECTOR, item_selector)
        href = item.get_attribute('href')
        current_url = self.driver.current_url


        WebDriverWait(self.driver, 3).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '#mynavbar > div > div > ul').is_displayed()
        )
        self.driver.execute_script("arguments[0].click();", item)
        WebDriverWait(self.driver, 3).until(lambda d: d.current_url != current_url)

