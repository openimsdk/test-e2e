import time
import webbrowser

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from config import HOST
from pages.add_friend_page import AddFriendPage
from pages.login_page import LoginPage
from  selenium.webdriver.support import  expected_conditions as EC

from utils.headless_browser import create_headless_driver
from utils.read_accounts import read_registered_accounts

@pytest.fixture
def headless_driver():
    driver = create_headless_driver()
    time.sleep(3)
    yield driver
    driver.quit()


@pytest.fixture
def driver(headless_driver):  # The fixture approach is more recommended.
    return headless_driver



def read_first_registered_account():
    has_accounts = read_registered_accounts(0)
    if has_accounts:
        phone_number, password = has_accounts

        return phone_number, password
    else:
        assert False, "There are no available registered accounts for registered testing."


@pytest.mark.run(order=3)
def test_add_friends(driver):
    login_page = LoginPage(driver)
    login_page.go_to()
    phone_number, pwd = read_first_registered_account()
    login_page.login(phone_number, pwd)
    expected_url = "{}#/chat".format(HOST)
    login_page.wait_for_login_success(expected_url)

    add_friend_page = AddFriendPage(driver)
    add_friend_page.go_to()

    registered_accounts = read_registered_accounts(1)
    print("注册 账号:", registered_accounts)

    if registered_accounts:
        friend_phone, friend_pwd = registered_accounts
        add_friend_page.add_friend(friend_phone, "你好，加个好友把！")
    else:
        assert False, "没有可用的注册账号来进行添加好友的测试"

