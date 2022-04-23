from ui.pages.base_page import BasePage
from ui.locators.basic_locators import MainPageLocators
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentsPage


class MainPage(BasePage):
    locators = MainPageLocators()
    url = "https://target.my.com/"

    def go_to_segments_page(self):
        self.click_repeat(self.locators.HEADER_SEGMENTS_LOCATOR)
        return SegmentsPage(self.driver)

    def go_to_campaign_page(self):
        self.click_repeat(self.locators.HEADER_CAMPAIGN_LOCATOR)
        return CampaignPage(self.driver)
