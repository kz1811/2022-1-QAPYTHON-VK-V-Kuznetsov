from selenium.webdriver.common.by import By


class BasePageLocators:
    pass


class LoginPageLocators(BasePageLocators):
    LOG_IN_BUTTON_LOCATOR = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
    LOG_IN_FORM_LOGIN_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm-module-input')][@name='email']")
    LOG_IN_FORM_PASSWORD_LOCATOR = (By.XPATH, "//input[contains(@class, 'authForm-module-input')][@name='password']")
    LOG_IN_FORM_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'authForm-module-button')]")
    LOG_IN_FORM_ERROR_MESSAGE_LOCATOR = (By.XPATH, "//div[contains(@class, 'notify-module-error')]")
    LOG_IN_FAILED_LOCATOR = (By.CSS_SELECTOR, ".mcPage .formMsg_text")


class MainPageLocators(BasePageLocators):
    HEADER_BILLING_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-billing')]")
    HEADER_TOOLS_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-tools')]")
    HEADER_PROFILE_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-profile')]")
    HEADER_CAMPAIGN_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-campaigns')]")
    HEADER_SEGMENTS_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-segments')]")


class CampaignPageLocators(MainPageLocators):
    CAMPAIGN_ADD_CAMPAIGN_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, "
                                                      "'dashboard-module-createButtonWrap')]//div[contains(@class, "
                                                      "'button-module-textWrapper')]")
    CAMPAIGN_NEW_CAMPAIGN_TARGET_TYPE_LOCATOR = (By.XPATH, "//div[contains(@class, '_traffic')]")
    CAMPAIGN_NEW_CAMPAIGN_URL_FIELD_LOCATOR = (By.XPATH, "//div[contains(@class, 'base-settings__main-url')]//input")
    CAMPAIGN_NEW_CAMPAIGN_NAME_TEXT_FIELD_LOCATOR = (By.XPATH, "//div[contains(@class, 'campaign-name__name-wrap')]"
                                                               "//input")

    CAMPAIGN_NEW_CAMPAIGN_PATTERN_LOCATOR = (By.CSS_SELECTOR, '.banner-settings #patterns_banner_4')
    CAMPAIGN_NEW_CAMPAIGN_SEND_PICTURE_LOCATOR = (By.XPATH, "//div[contains(@class, 'bannerEditor-module-editorForm')]"
                                                            "//input[@type='file']")
    CAMPAIGN_NEW_CAMPAIGN_SAVE_PATTERN_LOCATOR = (By.XPATH, '//div[contains(@class, '
                                                            '"bannerEditor-module-bottomControls")]/div['
                                                            '@data-test="submit_banner_button"]')

    CAMPAIGN_NEW_CAMPAIGN_CREATE_CAMPAIGN_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, "
                                                                      "'footer__controls')]//button")
    CAMPAIGN_EXISTENT_CAMPAIGN_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'dashboard-module-table')]//div["
                                                         "@data-row-id='central-1']//a[contains(@class, "
                                                         "'campaignName')]")


class SegmentsPageLocators(MainPageLocators):
    SEGMENTS_ADD_SEGMENT_BUTTON_LOCATOR = (By.CLASS_NAME, "button_submit")
    SEGMENTS_ADD_SEGMENT_FORM_LOCATOR = (By.CLASS_NAME, "adding-segments-modal")
    SEGMENTS_ADD_SEGMENT_FORM_CHECKBOX_LOCATOR = (By.XPATH, "//input[@type='checkbox'][contains(@class,"
                                                            "'adding-segments-source__checkbox')]")
    SEGMENTS_ADD_SEGMENT_FORM_SUBMIT_BUTTON_LOCATOR = (By.XPATH, "//div[@class='adding-segments-modal__btn-wrap "
                                                                 "js-add-button']/button")
    SEGMENTS_ADD_SEGMENT_NAME_FIELD_LOCATOR = (By.XPATH, "//div[contains(@class, 'input_create-segment-form')]//input")
    SEGMENTS_ADD_SEGMENT_SUBMIT_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, "
                                                            "'create-segment-form__btn-wrap')]/button")
    # for deleting segments
    SEGMENTS_EXISTENT_SEGMENT_NAME_FIELD_LOCATOR = (By.XPATH, "//div[contains(@class, 'cells-module-nameCell')]/a")
    SEGMENT_DELETE_EXISTENT_SEGMENT_ICON_LOCATOR = (By.XPATH, "//span[contains(@class, 'cells-module-removeCell')]")
    SEGMENT_DELETE_EXISTENT_SEGMENT_SUBMIT_BUTTON_LOCATOR = (By.XPATH, "//button[contains(@class, "
                                                                       "'button_confirm-remove')]")
    SEGMENTS_EXISTENT_SEGMENTS_TABLE_LOCATOR = (By.XPATH, "//div[contains(@class,'main-module-TableWrapper')]")
