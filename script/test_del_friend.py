import time
from unittest import result

import pytest
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from loc import Locators
from pages.del_friend import DeleteFriedn
from utils.headless_browser import create_driver
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
def driver(browser_driver):
    return browser_driver

@pytest.mark.run(order=8)
def test_del_friend(driver, login):
    has_accounts = read_registered_accounts(0)
    phone_number, pwd, _ = has_accounts
    login(phone_number, pwd)
    del_friend_page = DeleteFriedn(driver)
    del_friend_page.go_to()
    del_friend_page.del_friend()

    try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(Locators.del_loc)
            )
            print("Delete button disappeared, friend deletion successful.")
    except TimeoutException:
            pytest.fail("Friend deletion failed, delete button still visible after timeout.")
