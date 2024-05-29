import csv
import os.path
import time
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base.base_page import BasePage
from config import HOST, DIR_PATH
from  selenium.webdriver.support import  expected_conditions as EC

from loc import Locators
from utils.read_accounts import read_registered_accounts
from utils.test_visibility import test_visibility_of_element_located


# from utils.test_invisibility import test_invisibility_of_element_located
# from utils.test_visibility import test_visibility_of_element_located

class AddFriendPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = HOST

    def go_to(self):
        self.driver.get(self.url)

    def add_friend(self,friend_phone,greeting_message='Hello'):
        self.wait_masks_invisible()
        time.sleep(2)
        self.javascript_click(Locators.add_menu_loc)

        self.base_click(Locators.add_friend_loc)
        # Enter your friend's account number
        self.enter_text(Locators.add_input_account_loc, friend_phone)
        # Click Confirm
        self.base_click(Locators.add_input_confirm_loc)
        # In your profile, click Add Friend
        self.base_click(Locators.add_friend_info_loc)
        # Enter the verification information
        self.enter_text(Locators.send_info_loc, greeting_message)
        # Click Confirm sending
        self.base_click(Locators.end_confirm_loc)

        # Pop-up window adds successful and failed element positioning
        msg_loc = (By.CSS_SELECTOR,'.ant-message-custom-content.ant-message-success > span:nth-child(2)')
        message_check = test_visibility_of_element_located(msg_loc,'发送好友请求成功！')
        if message_check(self.driver):
            print("发送好友请求成功。")
        else:
            # Here we need to check the failure situation
            message_fail_check = test_visibility_of_element_located(msg_loc, "发送请求失败！")
            if message_fail_check(self.driver):
                print("发送好友请求失败。")
            else:
                # If it is neither a success nor a failure message, an unknown result is printed
                # You need to get the message text for printing
                try:
                    message_element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(msg_loc)
                    )
                    message_text = message_element.text
                    print("未知的结果，弹窗文本为：", message_text)
                except TimeoutException:
                    print("没有找到预期的反馈消息。")
