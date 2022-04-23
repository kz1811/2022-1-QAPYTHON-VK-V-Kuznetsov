import time
import allure
import random
import string
from ui.exceptions.page_exceptions import PageNotOpenedException
from ui.locators.basic_locators import BasePageLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException


class BasePage:
    locators = BasePageLocators()
    url = None

    def __init__(self, driver):
        self.driver = driver
        self.is_opened()

    def is_opened(self, timeout=45):
        started = time.time()
        while time.time() - started < timeout:
            if self.url in self.driver.current_url:
                return True
        raise PageNotOpenedException(f"Page is not opened: url was not valid or base element did not loaded; "
                                     f"current url: {self.driver.current_url}")

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 45
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Waiting for object visibility')
    def wait_visibility(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_full_loading_page(self, timeout=None):
        return self.wait(timeout).until(
            lambda driver: self.driver.execute_script('return document.readyState') == 'complete'
        )

    @allure.step('Search')
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Click')
    def click(self, locator, timeout=None):
        self.find(locator)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()

    def click_repeat(self, locator):
        CLICK_RETRY = 4
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator)
                self.click(locator)
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
            except ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise

    @allure.step('Scroll to element')
    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def rand_gen(self, num=20):
        name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(num))
        return name
