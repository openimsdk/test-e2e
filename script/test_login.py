import os
import sys
from config import DIR_PATH, HOST

#Login test script (scripts/test_login.py)
import time
import yaml
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pytest

from pages.login_page import LoginPage

from utils.headless_browser import create_driver
from utils.read_accounts import read_registered_accounts


@pytest.fixture
def browser_driver():
    driver = create_driver()
    time.sleep(3)
    yield driver
    driver.quit()


@pytest.fixture
def driver(browser_driver):  # The fixture approach is more recommended.
    return browser_driver


@pytest.mark.run(order=2)
def test_loginss(driver):
    registered_accounts = read_registered_accounts(0)
    print("Registration account:", registered_accounts)

    # Instantiate the LoginPage class.
    login_page = LoginPage(driver)
    login_page.go_to() # Access the login page using the `go_to` method from the `LoginPage` class.
    # Select one account from the registered accounts for adding a friend operation.
    if registered_accounts:
        username, pwd, _ = registered_accounts
        print('phone：', username, pwd)
        login_page.login(username, pwd)
        time.sleep(10)
    else:
        assert False, "There are no available registered accounts for login testing."



