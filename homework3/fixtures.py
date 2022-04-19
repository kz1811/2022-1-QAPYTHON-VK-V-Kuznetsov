import os
import shutil
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from api.client import ApiClient


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)


@pytest.fixture(scope='session')
def credentials():

    abs_path = os.path.abspath(r'homework3/files/log1n_data')

    with open(abs_path, 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
        return user, password


@pytest.fixture(scope='function')
def api_client(config, credentials) -> ApiClient:
    api_client = ApiClient(config['url'], *credentials)
    return api_client
