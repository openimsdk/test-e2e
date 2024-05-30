from selenium.common import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base.base_page import BasePage
from config import HOST
from loc import Locators
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.wait import WebDriverWait


class SendMsgPage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.url = HOST

    def go_to(self):
        self.driver.get(self.url)

    def scroll_to_top_of_chat(self):
        chat_window = self.driver.find_element(By.ID, 'chat-list')
        self.driver.execute_script("arguments[0].scrollTop = 0;", chat_window)
        time.sleep(3)
        print('页面已经滚动到了顶部')

    def scroll_to_bottom(self):
        chat_window = self.driver.find_element(By.ID, 'chat-list')
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", chat_window)
        print('页面已经滚动到了底部')
        time.sleep(2)

    def scroll_to_element(self, element):
        # chat_window = self.driver.find_element(By.CSS_SELECTOR, 'div.chat-window-selector')  # 更新选择器为聊天窗口的实际选择器
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print('页面已经滚动到了', element, '元素的位置上', element.text)
        time.sleep(1)

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
        self.scroll_to_bottom()
        print('发送3条消息后滚到底部以便发送图片等')

    def upload_file(self, file_path, file_type):
        locator = Locators.file_type_to_loc[file_type]
        # Find th file input element and upload th file
        # Make sure "locator" is a tuple
        if not isinstance(locator, tuple):
            raise ValueError(f"Locator for {file_type} must be a tuple.")
        file_input = self.driver.find_element(*locator)
        file_input.send_keys(file_path)  # Use "send_keys" to upload files
        self.scroll_to_bottom()
        time.sleep(2)

    def check_msg_send(self, msg):
        # Wait for the message to appear in the history
        print('Testing the list of messages that are passed in', msg)
        time.sleep(3)
        self.scroll_to_top_of_chat()
        message_elements = self.wait.until(lambda driver: driver.find_elements(*Locators.msg_panel_loc))
        self.scroll_to_top_of_chat()
        messages_texts = []

        for element in message_elements:
            self.scroll_to_element(element)
            print('捕捉到滚动到消息元素：', element.text)
            messages_texts.append(element.text)

        message_text = ' '.join(messages_texts)
        print('检查验证消息有：', message_text)
        # Check if each message appears in the chat history

        all_messages_present = all(message in message_text for message in msg)
        print('所有消息-------:', all_messages_present)

        return all_messages_present

    # def check_file_sent_successfully(self, file_type):
    #     print('检查图片视频文件')
    #     locator = Locators.file_sent_success_loc[file_type]
    #     if not isinstance(locator, tuple):
    #         raise ValueError(f'"Locator for {file_type} must be a tuple.')
    #
    #     self.scroll_to_bottom()
    #     # self.wait.until(EC.presence_of_element_located(locator))
    #     self.base_find(locator)


    def check_received_messages(self):
        messages = []
        self.scroll_to_top_of_chat()
        message_element = self.wait.until(lambda driver: driver.find_elements(*Locators.received_panel_loc))
        for element in message_element:
            self.scroll_to_element(element)
            messages.append(element.text)
        print('接收的内容有：', messages)
        return messages

    def check_received_files(self,file_type):
        locator = Locators.file_sent_success_loc[file_type]
        if not isinstance(locator, tuple):
            raise ValueError(f'Locator for {file_type} must be a tuple.')

        try:
            wait = WebDriverWait(self.driver, 30, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
            elements = wait.until(EC.presence_of_element_located(locator))
            print('看看是什么：', elements)
            self.scroll_to_element(elements)
            time.sleep(3)
            if file_type == 'image':
                print(f'接收到的图片文件: {elements.get_attribute("src")}')
            elif file_type == 'video':
                print(f'接收到的视频文件: {elements.get_attribute("src")}')
            elif file_type == 'file':
                print(f'接收到的普通文件: {elements.text}')
            return True
        except TimeoutException:
            self.driver.save_screenshot(f'file_receiving_failed_{file_type}.png')
            print(f"超时：在检查接收到的文件类型时遇到 TimeoutException: {file_type}")
            return False
        except StaleElementReferenceException:
            self.driver.save_screenshot(f'file_stale_element_error_{file_type}.png')
            print(f"StaleElementReferenceException：在检查接收到的文件类型时遇到 StaleElementReferenceException: {file_type}")
            return False



