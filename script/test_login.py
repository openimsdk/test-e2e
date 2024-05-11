import os
import sys

from config import DIR_PATH, HOST



#登录测试脚本 (scripts/test_login.py)
import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
import yaml
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

# from data.login_data import LOGIN_DATA
from pages.login_page import LoginPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.read_accounts import read_registered_accounts




#The fixture approach is more recommended.
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield  driver
    time.sleep(5)

    driver.quit()




def test_loginss(driver):
    registered_accounts = read_registered_accounts()
    print("Registration account:", registered_accounts)

    # Instantiate the LoginPage class.
    login_page = LoginPage(driver)
    login_page.go_to() # Access the login page using the `go_to` method from the `LoginPage` class.
    # Select one account from the registered accounts for adding a friend operation.
    if registered_accounts:
        account_pwd = registered_accounts[0]
        username, pwd = account_pwd
        print('phone：', username, pwd)
        login_page.login(username, pwd)
        time.sleep(10)
    else:
        assert False, "There are no available registered accounts for login testing."



