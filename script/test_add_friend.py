import time
import webbrowser

import pytest

from pages.add_friend_page import AddFriendPage

from utils.headless_browser import create_headless_driver
from utils.read_accounts import read_registered_accounts
from utils.token import login


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
def test_add_friends(driver, login):
    phone_number, pwd = read_first_registered_account()
    login(phone_number, pwd)
    add_friend_page = AddFriendPage(driver)
    add_friend_page.go_to()

    registered_accounts = read_registered_accounts(1)
    print("注册 账号:", registered_accounts)

    if registered_accounts:
        friend_phone, friend_pwd = registered_accounts
        add_friend_page.add_friend(friend_phone, "你好，加个好友把！")
    else:
        assert False, "没有可用的注册账号来进行添加好友的测试"

    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[1])
    # time.sleep(10)


