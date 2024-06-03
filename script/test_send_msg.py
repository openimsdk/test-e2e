import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from loc import Locators
from utils.headless_browser import  create_driver
from utils.read_accounts import read_registered_accounts
import pytest
from selenium import webdriver

from config import HOST, IMAGE_PATH, VIDEO_PATH, FILE_PATH
from pages.login_page import LoginPage
from pages.send_msg_page import SendMsgPage
import tkinter as tk
from tkinter import simpledialog
from  utils.token import login

@pytest.fixture
def browser_driver():
    driver = create_driver()
    time.sleep(3)
    yield driver
    driver.quit()


@pytest.fixture
def driver(browser_driver):  # The fixture approach is more recommended.
    return browser_driver





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


@pytest.fixture(scope='session')
def shared_state():
    return {}


@pytest.mark.run(order=5)
def test_send_text_msgs(send_msg_page, shared_phone, login, shared_state):
    test_login = read_registered_accounts(0)
    if test_login:
        phone, pwd = test_login
        login(phone, pwd)
        strange_phone, strange_password = shared_phone
        msgs = ['Hello! This is the first message。', 'This is the second test message。', 'The last message！']
        send_msg_page.send_msg(strange_phone, msgs)
        send_msg_page.upload_file(FILE_PATH, "file")
        send_msg_page.upload_file(IMAGE_PATH, "image")
        send_msg_page.upload_file(VIDEO_PATH, "video")

        assert send_msg_page.check_msg_send(msgs), 'Message sending failed'
        assert send_msg_page.check_received_files('file'), 'File sending failed'
        time.sleep(4)
        assert send_msg_page.check_received_files('image'), 'Image sending failed'
        time.sleep(4)
        assert send_msg_page.check_received_files('video'), 'Video sending failed'
        shared_state['sent_files'] = ['file', 'image', 'video']

    else:
        pytest.fail("There are no available registered accounts for testing message sending")


@pytest.mark.run(order=6)
def test_receive_message(driver, login, send_msg_page, shared_phone, shared_state):
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
        # This should be a list of previously send message
        expected_msgs = ['Hello! This is the first message。', 'This is the second test message。', 'The last message！']
        assert all(msg in received_msgs for msg in expected_msgs), "有消息未正确接收"
        print("所有文本消息都已成功接收。")
        # assert send_msg_page.check_received_files('file'), 'File sending failed'
        # assert send_msg_page.check_received_files('image'), 'Image sending failed'
        # assert send_msg_page.check_received_files('video'), 'Video sending failed'
        for file_type in shared_state.get('sent_files', []):
            assert send_msg_page.check_received_files(file_type), f'{file_type.capitalize()} receiving failed'
    else:
        pytest.fail("There are no available registered accounts for testing message sending")




