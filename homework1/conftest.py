import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='https://target.my.com/')


@pytest.fixture()
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    return {'url': url, 'browser': browser}


@pytest.fixture()
def driver(config):
    browser = config['browser']
    url = config['url']
    if browser == 'chrome':
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif browser == 'firefox':
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError('Unsupported browser: "{browser}"')
    browser.maximize_window()
    browser.get(url)
    yield browser
    browser.quit()