import pytest
from selenium.common import TimeoutException

from config import HOST
from pages.login_page import LoginPage


@pytest.fixture
def login(driver):
    def perform_login(username, password):
        login_page = LoginPage(driver)
        login_page.go_to()
        login_page.login(username,password)
        expected_url = "{}#/chat".format(HOST)
        try:
            login_page.wait_for_login_success(expected_url)
        except TimeoutException:
            login_page.reload_page_if_stuck()
            login_page.wait_for_login_success(expected_url)
    return perform_login
