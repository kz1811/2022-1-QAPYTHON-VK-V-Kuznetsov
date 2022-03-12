import pytest
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from ui.locators import basic_locators


CLICK_RETRY = 3


def rand_gen():
    import random
    import string
    name = random.choice(string.ascii_uppercase) + ''.join(
        random.choice(string.ascii_lowercase) for i in range(random.randrange(9)))

    em1 = ''.join(random.choice(string.ascii_letters) for i in range(15))
    email = em1 + '@mail.ru'
    phone = ('7' + ''.join(random.choice(string.digits) for i in range(10)))
    return {'name': name, 'email': email, 'phone': phone}


random_gen = rand_gen()


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 30
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        self.wait(timeout).until(EC.visibility_of_element_located(locator))
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        self.find(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()

    def click_repeat(self, locator):
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator)
                # if i<2:
                #    self.driver.refresh()
                self.click(locator)
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
            except ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise

    def is_disp(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def log_in(self):
        self.find(basic_locators.LOG_IN_BUTTON_LOCATOR)
        self.click(basic_locators.LOG_IN_BUTTON_LOCATOR)
        self.find(basic_locators.LOG_IN_FORM_LOGIN_LOCATOR).send_keys('vlad.lavashov@yahoo.com')
        self.find(basic_locators.LOG_IN_FORM_PASSWORD_LOCATOR).send_keys('PBpMt6$mbCf83wC')
        self.find(basic_locators.LOG_IN_FORM_BUTTON_LOCATOR)
        self.click(basic_locators.LOG_IN_FORM_BUTTON_LOCATOR)

    def log_out(self):
        self.click_repeat(basic_locators.HEADER_RIGHT_MENU_BUTTON_LOCATOR)
        self.click_repeat(basic_locators.HEADER_LIST_ITEM_LOGOUT_LOCATOR)

    def switch_str(self, tab):
        self.find(basic_locators.header_tabs.get(tab))
        self.click_repeat(basic_locators.header_tabs.get(tab))

    def switch_loc(self, locator):
        self.find(locator)
        self.click_repeat(locator)

    def fill_contact_info(self) -> bool:

        self.switch_loc(basic_locators.PROFILE_LOCATOR)

        name_field = self.find(basic_locators.CONTACT_INFO_NAME_FIELD_LOCATOR)
        name_field.clear()
        phone_field = self.find(basic_locators.CONTACT_INFO_PHONE_FIELD_LOCATOR)
        phone_field.clear()

        self.find(basic_locators.CONTACT_INFO_ADD_MAIL_BUTTON_LOCATOR)
        self.click_repeat(basic_locators.CONTACT_INFO_ADD_MAIL_BUTTON_LOCATOR)

        phone_field.send_keys(random_gen.get('phone'))
        name_field.send_keys(random_gen.get('name'))
        self.find(basic_locators.CONTACT_INFO_ADD_MAIL_FIELD_LOCATOR).send_keys(random_gen.get('email'))

        self.find(basic_locators.CONTACT_INFO_SUBMIT_CHANGES_BUTTON_LOCATOR)
        self.click(basic_locators.CONTACT_INFO_SUBMIT_CHANGES_BUTTON_LOCATOR)

        success_message_is_displayed = self.is_disp(basic_locators.CONTACT_INFO_SUCCESS_CHANGES_NOTIFY_LOCATOR)

        self.driver.refresh()

        phone_was_saved = (random_gen.get('phone') == self.find(
            basic_locators.CONTACT_INFO_PHONE_FIELD_LOCATOR).get_attribute('value'))

        name_was_saved = (random_gen.get('name') == self.find(
            basic_locators.CONTACT_INFO_NAME_FIELD_LOCATOR).get_attribute('value'))

        email_was_saved = (random_gen.get('email') == self.find(
            basic_locators.CONTACT_INFO_ADD_MAIL_FIELD_LOCATOR).get_attribute('value')) or \
                          (random_gen.get('email') == self.find(
                              basic_locators.CONTACT_INFO_ADD_MAIL2_FIELD_LOCATOR).get_attribute('value'))

        self.find(basic_locators.CONTACT_INFO_SUBMIT_CHANGES_BUTTON_LOCATOR)
        self.click(basic_locators.CONTACT_INFO_SUBMIT_CHANGES_BUTTON_LOCATOR)

        self.find(basic_locators.CONTACT_INFO_DELETE_EMAIL_BUTTON_LOCATOR)
        self.click(basic_locators.CONTACT_INFO_DELETE_EMAIL_BUTTON_LOCATOR)
        self.click(basic_locators.CONTACT_INFO_DELETE_EMAIL_BUTTON_LOCATOR)
        self.click(basic_locators.CONTACT_INFO_SUBMIT_CHANGES_BUTTON_LOCATOR)

        return success_message_is_displayed and phone_was_saved and name_was_saved and email_was_saved