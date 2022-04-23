import time
import allure
from ui.pages.base_page import BasePage
from ui.locators.basic_locators import CampaignPageLocators


class CampaignPage(BasePage):
    locators = CampaignPageLocators()

    base_element = locators.CAMPAIGN_ADD_CAMPAIGN_BUTTON_LOCATOR
    url = 'https://target.my.com/dashboard'

    @allure.step('Creating new campaign')
    def create_new_campaign(self, path):
        random_name = self.rand_gen()

        self.click(self.locators.CAMPAIGN_ADD_CAMPAIGN_BUTTON_LOCATOR)
        self.click(self.locators.CAMPAIGN_NEW_CAMPAIGN_TARGET_TYPE_LOCATOR)
        with allure.step('Send url of campaign'):
            campaign_url_field = self.find(self.locators.CAMPAIGN_NEW_CAMPAIGN_URL_FIELD_LOCATOR)
            campaign_url_field.click()
            campaign_url_field.clear()
            campaign_url_field.send_keys(random_name + '.com')
        with allure.step('Send name of campaign'):
            campaign_name_field = self.find(self.locators.CAMPAIGN_NEW_CAMPAIGN_NAME_TEXT_FIELD_LOCATOR)
            self.scroll_to_element(campaign_name_field)
            self.click(self.locators.CAMPAIGN_NEW_CAMPAIGN_NAME_TEXT_FIELD_LOCATOR)
            campaign_name_field.clear()
            campaign_name_field.send_keys(random_name)
        with allure.step('Choose pattern of campaign'):
            choose_pattern = self.find(self.locators.CAMPAIGN_NEW_CAMPAIGN_PATTERN_LOCATOR)
            self.scroll_to_element(choose_pattern)
            choose_pattern.click()
        with allure.step('Send picture'):
            send_pic_item = self.find(self.locators.CAMPAIGN_NEW_CAMPAIGN_SEND_PICTURE_LOCATOR)
            self.scroll_to_element(send_pic_item)
            send_pic_item.send_keys(path)
        with allure.step('Submit creating'):
            self.click(self.locators.CAMPAIGN_NEW_CAMPAIGN_SAVE_PATTERN_LOCATOR)
            self.click(self.locators.CAMPAIGN_NEW_CAMPAIGN_CREATE_CAMPAIGN_BUTTON_LOCATOR)

        return random_name == (self.find(self.locators.CAMPAIGN_EXISTENT_CAMPAIGN_NAME_LOCATOR)).text
