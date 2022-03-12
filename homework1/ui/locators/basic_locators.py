from selenium.webdriver.common.by import By

# for log in
LOG_IN_BUTTON_LOCATOR = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
LOG_IN_FORM_LOGIN_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm-module-input')][@name='email']")
LOG_IN_FORM_PASSWORD_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm-module-input')][@name='password']")
LOG_IN_FORM_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'authForm-module-button')]")

# for log out
HEADER_RIGHT_MENU_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
HEADER_LIST_ITEM_LOGOUT_LOCATOR = (By.XPATH, "//li[contains(@class, 'rightMenu-module-rightMenuItem')][2]/a")

# for_change_info
CONTACT_INFO_NAME_FIELD_LOCATOR = (By.XPATH, "//div[@data-name='fio']//input")
CONTACT_INFO_PHONE_FIELD_LOCATOR = (By.XPATH, "//div[@data-name='phone']//input")
# CONTACT_INFO_ADD_MAIL_BUTTON_LOCATOR = (By.XPATH, "//*[contains(text(), 'Добавить ещё')]")
CONTACT_INFO_ADD_MAIL_BUTTON_LOCATOR = (By.CSS_SELECTOR, ".js-add-row .clickable-button__spinner")
CONTACT_INFO_ADD_MAIL_FIELD_LOCATOR = (By.XPATH, "//*[@data-email-index='1']//input")
CONTACT_INFO_ADD_MAIL2_FIELD_LOCATOR = (By.XPATH, "//*[@data-email-index='0']//input")
CONTACT_INFO_SUBMIT_CHANGES_BUTTON_LOCATOR = (By.XPATH, "//button[contains(@class, 'button_submit')]")
CONTACT_INFO_SUCCESS_CHANGES_NOTIFY_LOCATOR = (By.XPATH, "//*[@data-class-name='SuccessView']")
CONTACT_INFO_DELETE_EMAIL_BUTTON_LOCATOR = (By.CSS_SELECTOR, '.clickable-button_email_remove')

# for_switching_nav_tabs
BILLING_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-billing')]")
TOOLS_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-tools')]")
PROFILE_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-profile')]")

header_tabs = {'tools': TOOLS_LOCATOR, 'billing': BILLING_LOCATOR, 'profile': PROFILE_LOCATOR}
