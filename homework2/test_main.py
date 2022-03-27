import time
import allure
from ui.pages.login_page import LoginPage
from base import BaseCase
import pytest
import os


class TestHomework2WrongAutentification(BaseCase):
    autorize = False

    @pytest.mark.UI
    def test_negative_login_1(self, credentials):
        login_page = LoginPage(self.driver)
        assert login_page.wrong_pass(*credentials)

    @pytest.mark.UI
    def test_negative_login_2(self, credentials):
        login_page = LoginPage(self.driver)
        assert login_page.wrong_form_login(*credentials)


class TestHomework2(BaseCase):

    @pytest.fixture()
    def file_path(self, repo_root):
        return os.path.join(repo_root, 'files', 'picture.jpg')

    @pytest.mark.UI
    def test_create_ad_company(self, file_path):
        with allure.step('Going to campaign page'):
            self.main_page.go_to_campaign_page()
        assert self.campaign_page.create_new_campaign(file_path)

    @pytest.mark.UI
    def test_create_segment(self):
        with allure.step('Going to segments page'):
            self.main_page.go_to_segments_page()
        assert self.segments_page.create_segment()

    @pytest.mark.UI
    def test_delete_segment(self):
        with allure.step('Going to segments page'):
            self.main_page.go_to_segments_page()
        assert self.segments_page.delete_segment()
