from base import BaseCase
import pytest


class TestHomework1(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        self.log_in()
        assert "dashboard" in self.driver.current_url

    @pytest.mark.UI
    def test_logout(self):
        self.log_in()
        self.log_out()
        url_logout_page = self.driver.current_url
        assert (url_logout_page == "https://target.my.com/")

    @pytest.mark.UI
    @pytest.mark.parametrize(
        'tab',
        [
            pytest.param('billing'),
            pytest.param('profile'),
        ]
    )
    def test_switch_category(self, tab):
        self.log_in()
        self.switch_str(tab)
        assert tab in self.driver.current_url

    @pytest.mark.UI
    def test_change_contact_info(self):
        self.log_in()
        assert self.fill_contact_info()
