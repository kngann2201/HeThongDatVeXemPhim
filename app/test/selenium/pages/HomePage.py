from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from app.test.selenium.pages.BasePage import BasePage


class HomePage(BasePage):
    URL = 'http://127.0.0.1:5005/'
    SEARCH = (By.NAME, 'kw')
    TYPE_LIST = (By.ID, 'navbarDropdown')
    MOVIE_TYPE_1 = (By.CSS_SELECTOR, '#mynavbar > ul > li.nav-item.dropdown > ul > li:nth-child(1) > a')

    def open_page(self, url=URL):
        self.open(url)

    def filter_by_type(self):
        self.find(*self.TYPE_LIST).click()
        self.find(*self.MOVIE_TYPE_1).click()

    def search(self, kw):
        e = self.find(*self.SEARCH)
        e.send_keys(kw)
        e.send_keys(Keys.RETURN)

    def search_filter(self, kw):
        self.filter_by_type()
        self.search(kw)