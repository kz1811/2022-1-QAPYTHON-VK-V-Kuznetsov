import allure
from ui.pages.main_page import MainPage
from ui.locators.basic_locators import SegmentsPageLocators


class SegmentsPage(MainPage):
    locators = SegmentsPageLocators()

    @allure.step('Creating new segment')
    def create_segment(self):

        self.click(self.locators.SEGMENTS_ADD_SEGMENT_BUTTON_LOCATOR)
        self.find(self.locators.SEGMENTS_ADD_SEGMENT_FORM_LOCATOR)
        self.click(self.locators.SEGMENTS_ADD_SEGMENT_FORM_CHECKBOX_LOCATOR)
        self.click(self.locators.SEGMENTS_ADD_SEGMENT_FORM_SUBMIT_BUTTON_LOCATOR)

        with allure.step('Send name of segment'):
            name_segment_field = self.find(self.locators.SEGMENTS_ADD_SEGMENT_NAME_FIELD_LOCATOR)
            name_segment_field.clear()
            rand_segment_name = self.rand_gen()
            name_segment_field.send_keys(rand_segment_name)

        self.click(self.locators.SEGMENTS_ADD_SEGMENT_SUBMIT_BUTTON_LOCATOR)
        with allure.step('Save check'):
            self.find(self.locators.SEGMENTS_EXISTENT_SEGMENT_NAME_FIELD_LOCATOR)
            self.driver.refresh()
            self.find(self.locators.SEGMENTS_EXISTENT_SEGMENT_NAME_FIELD_LOCATOR)

        return rand_segment_name in self.driver.page_source

    @allure.step('Deleting segments')
    def delete_segment(self):
        with allure.step('Save name of segment'):
            created_segment_name = self.find(self.locators.SEGMENTS_EXISTENT_SEGMENT_NAME_FIELD_LOCATOR)
            curr_segment_name = created_segment_name.text

        with allure.step('Deleting segment'):
            self.click(self.locators.SEGMENT_DELETE_EXISTENT_SEGMENT_ICON_LOCATOR)
            self.click(self.locators.SEGMENT_DELETE_EXISTENT_SEGMENT_SUBMIT_BUTTON_LOCATOR)

        with allure.step('Check for deleting name in page'):
            self.driver.refresh()
            self.find(self.locators.SEGMENTS_EXISTENT_SEGMENTS_TABLE_LOCATOR)
        with allure.step('Asserting'):
            assert curr_segment_name not in self.driver.page_source
        return curr_segment_name not in self.driver.page_source
