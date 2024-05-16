import time

from selenium.common import TimeoutException

from utils.headless_browser import create_headless_driver
from utils.read_accounts import read_registered_accounts
import pytest
from selenium import webdriver

from config import HOST
from pages.login_page import LoginPage
from pages.send_msg_page import SendMsgPage



@pytest.fixture
def headless_driver():
    driver = create_headless_driver()
    yield driver
    driver.quit()


@pytest.fixture
def driver(headless_driver):  # The fixture approach is more recommended.
    return headless_driver


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


@pytest.fixture
def shared_phone():
    registered_accounts = read_registered_accounts(1)
    if registered_accounts:
        phone, pwd = registered_accounts
        return phone, pwd

    pytest.fail("There are no registered accounts available to test the sending of messages")


@pytest.fixture
def send_msg_page(driver, login):  # Encapsulate the login page Because text, video and pictures need to be used
    send_msg_page = SendMsgPage(driver)
    send_msg_page.go_to()
    return send_msg_page


@pytest.mark.run(order=4)
def test_send_text_msgs(send_msg_page, shared_phone, login):
    test_login = read_registered_accounts(0)
    if test_login:
        phone, pwd = test_login
        login(phone, pwd)
        strange_phone, strange_password = shared_phone
        msgs = ['Hello! This is the first message。', 'This is the second test message。', 'The last message！']
        send_msg_page.send_msg(strange_phone, msgs)
        assert send_msg_page.check_msg_send(msgs), 'Message sending failed'
    else:
        pytest.fail("There are no available registered accounts for testing message sending")


@pytest.mark.run(order=5)
def test_receive_message(driver, login, send_msg_page, shared_phone):
    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[1])

    receiver_phone, receiver_password = shared_phone
    print('新建窗口后的', receiver_phone)
    login(receiver_phone, receiver_password)

    send_phone = read_registered_accounts(0)
    if send_phone:
        phone, pwd = send_phone
        send_msg_page.navigate_to_add_friend(phone)
        time.sleep(3)
        received_msgs = send_msg_page.check_received_messages()
        expected_msgs = ['Hello! This is the first message。', 'This is the second test message。', 'The last message！']  # 这应该是之前发送的消息列表
        assert all(msg in received_msgs for msg in expected_msgs), "有消息未正确接收"

        print("所有消息都已成功接收。")
        time.sleep(10)


