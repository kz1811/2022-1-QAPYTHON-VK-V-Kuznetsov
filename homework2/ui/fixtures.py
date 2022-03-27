import os
import shutil
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ui.pages.base_page import BasePage
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentsPage
from ui.pages.login_page import LoginPage


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture()
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']

    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})

    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '98.0',
        }
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities,
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError('Unsupported browser: "{browser}"')
    driver.maximize_window()
    driver.get(url)
    yield driver
    driver.quit()


def get_driver(browser_name):
    if browser_name == 'chrome':
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser_name == 'firefox':
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.maximize_window()
    return browser


@pytest.fixture(scope='session', params=['chrome', 'firefox'])
def all_drivers(config, request):
    url = config['url']
    browser = get_driver(request.param)
    browser.get(url)
    yield browser
    browser.quit()


@pytest.fixture(scope='session')
def credentials():
    with open('files/log1n_data', 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
        return user, password


@pytest.fixture(scope='session')
def cookies(credentials, config):
    driver = get_driver(config['browser'])
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.login(*credentials)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture()
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture()
def main_page(driver):
    return SegmentsPage(driver=driver)


@pytest.fixture()
def campaign_page(driver):
    return CampaignPage(driver=driver)


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture()
def segments_page(driver):
    return SegmentsPage(driver=driver)
