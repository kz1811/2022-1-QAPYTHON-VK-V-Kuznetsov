from ui.pages.base_page import BasePage
from ui.locators.basic_locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()

    def go_to_segments_page(self):
        self.click_repeat(self.locators.HEADER_SEGMENTS_LOCATOR)
        assert 'target.my.com/segments' in self.driver.current_url

    def go_to_campaign_page(self):
        self.click_repeat(self.locators.HEADER_CAMPAIGN_LOCATOR)
        assert 'target.my.com/dashboard' in self.driver.current_url
