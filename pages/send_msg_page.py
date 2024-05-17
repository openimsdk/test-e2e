from base.base_page import BasePage
from config import HOST
from loc import Locators
from selenium.webdriver.support import expected_conditions as EC
import time


class SendMsgPage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.url = HOST

    def go_to(self):
        self.driver.get(self.url)

    def navigate_to_add_friend(self, strange_phone):
        self.wait_masks_invisible()
        time.sleep(5)
        self.javascript_click(Locators.add_menu_loc)  # Utilize an encapsulated JavaScript click function

        # Locate the element that appears after hovering,
        # such as 'Add Friend,' and click on 'Add Friend' in the dropdown menu.
        self.base_click(Locators.add_friend_loc)
        # Enter the friend's account.
        self.enter_text(Locators.add_input_account_loc, strange_phone)
        # Clicking 'Confirm'
        self.base_click(Locators.add_input_confirm_loc)
        # Clicking 'Send Message' in the profile
        self.base_click(Locators.send_strange_info_loc)
        # Ensure that the chat window has been loaded
        self.wait.until(EC.visibility_of_element_located(Locators.msg_input_loc))

    def send_msg(self, strange_phone, msg):
        self.navigate_to_add_friend(strange_phone)

        # all_msgs = ""   # Used to accumulate the text of all sent messages
        # Make sure that we are handling the list of messages here
        for messages in msg:   # Iterate through the messages
            self.enter_text(Locators.msg_input_loc, messages)
            self.base_click(Locators.send_msg_btn_loc)
            # all_msgs += messages + " "  # Assuming messages are separated by spaces
            time.sleep(1)  # A brief pause to ensure message sending

    def check_msg_send(self, msg):
        # 等待消息出现在聊天历史中
        print('Testing the list of messages that are passed in', msg)
        message_elements = self.wait.until(lambda driver:  driver.find_elements(*Locators.msg_panel_loc))
        message_text = ' '.join([element.text for element in message_elements])
        print('Chat history of sent messages：', message_text)
        # Check if each message appears in the chat history
        return all(message in message_text for message in msg)

    def check_received_messages(self):
        messages = []
        message_element = self.wait.until(lambda driver: driver.find_elements(*Locators.received_panel_loc))
        for element in message_element:
            messages.append(element.text)
        print('接收的内容有：', messages)
        return messages
