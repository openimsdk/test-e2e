import time
import webbrowser

import pytest
from selenium.webdriver.common.by import By

from pages.add_friend_page import AddFriendPage
from selenium.webdriver.support.wait import WebDriverWait
from utils.headless_browser import  create_driver
from utils.read_accounts import read_registered_accounts
from utils.token import login
from  selenium.webdriver.support import  expected_conditions as EC

@pytest.fixture
def browser_driver():
    driver = create_driver()
    time.sleep(3)
    yield driver
    driver.quit()


@pytest.fixture
def driver(browser_driver):  # The fixture approach is more recommended.
    return browser_driver


def read_first_registered_account():
    has_accounts = read_registered_accounts(0)
    if has_accounts:
        phone_number, password, add_nickname = has_accounts

        return phone_number, password,add_nickname
    else:
        assert False, "There are no available registered accounts for registered testing."


@pytest.mark.run(order=3)
def test_add_friends(driver, login):
    phone_number, pwd, _ = read_first_registered_account()
    login(phone_number, pwd)
    add_friend_page = AddFriendPage(driver)
    add_friend_page.go_to()

    registered_accounts = read_registered_accounts(1)
    print("Register an account:", registered_accounts)

    if registered_accounts:
        friend_phone, friend_pwd, _ = registered_accounts
        add_friend_page.add_friend(friend_phone, "你好，加个好友把！")
    else:
        assert False, "There is no available registered account to test adding friends"
    #
    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[1])


@pytest.mark.run(order=7)
def test_agree_friends(driver, login):
    add_friend_page = AddFriendPage(driver)
    add_friend_page.go_to()

    handle_agree = read_registered_accounts(1)
    if handle_agree:
        phone, pwd, _ = handle_agree
        login(phone, pwd)
        add_account = read_first_registered_account()
        phone, pwd, add_name = add_account
        add_friend_page.agree_friend(add_name)

        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[@class='text-sm text-[var(--sub-text)]']"))
        )

        text = element.text
        print('Verify successful consent：', text)
        assert text == "已同意", "Assertion failed: The text content is not '已同意'"
    else:
        assert False, "There is no available registered account to test the friend request approval"

