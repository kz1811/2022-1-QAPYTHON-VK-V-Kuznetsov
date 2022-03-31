import allure
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.locators.basic_locators import LoginPageLocators


class LoginPage(BasePage):
    locators = LoginPageLocators()

    @allure.step('Login')
    def login(self, user, password):
        self.click(self.locators.LOG_IN_BUTTON_LOCATOR)
        with allure.step('Send login'):
            login = self.find(self.locators.LOG_IN_FORM_LOGIN_LOCATOR)
            login.clear()
            login.send_keys(user)
        with allure.step('Send password'):
            passw = self.find(self.locators.LOG_IN_FORM_PASSWORD_LOCATOR)
            passw.clear()
            passw.send_keys(password)
        self.click(self.locators.LOG_IN_FORM_BUTTON_LOCATOR)
        assert 'target.my.com/dashboard' in self.driver.current_url
        return MainPage(self.driver)

    @allure.step('Test: input wrong password')
    def wrong_pass(self, user, password):
        self.click(self.locators.LOG_IN_BUTTON_LOCATOR)
        with allure.step('Send login'):
            login = self.find(self.locators.LOG_IN_FORM_LOGIN_LOCATOR)
            login.clear()
            login.send_keys(user)
        with allure.step('Send wrong password'):
            passw = self.find(self.locators.LOG_IN_FORM_PASSWORD_LOCATOR)
            passw.clear()
            passw.send_keys(password + self.rand_gen())
        self.click(self.locators.LOG_IN_FORM_BUTTON_LOCATOR)
        return 'account.my.com/login/?error_code=1' in self.driver.current_url

    @allure.step('Test: input wrong form of login')
    def wrong_form_login(self, login, password):
        self.click(self.locators.LOG_IN_BUTTON_LOCATOR)
        with allure.step('Send wrong login'):
            login = self.find(self.locators.LOG_IN_FORM_LOGIN_LOCATOR)
            login.clear()
            login.send_keys(self.rand_gen())
        with allure.step('Send password'):
            passw = self.find(self.locators.LOG_IN_FORM_PASSWORD_LOCATOR)
            passw.clear()
            passw.send_keys(password)
        self.click(self.locators.LOG_IN_FORM_BUTTON_LOCATOR)
        with allure.step('Waiting for error message'):
            error_sign = self.wait_visibility(self.locators.LOG_IN_FORM_ERROR_MESSAGE_LOCATOR)
        return error_sign.is_displayed()
