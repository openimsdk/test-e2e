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

    def check_received_files(self, file_type):
        locator = Locators.file_sent_success_loc[file_type]
        if not isinstance(locator, tuple):
            raise ValueError(f'Locator for {file_type} must be a tuple.')

        try:
            WebDriverWait(self.driver, 20).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete')

            print('查看接收类型：',file_type)
            elements = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            # elements = wait.until(EC.visibility_of_element_located(locator))
            print('等待元素可见看看是什么：', elements)
            self.scroll_to_element(elements)
            time.sleep(3)

            # 对图片和视频缩略图使用相同的加载验证逻辑
            if file_type == 'image' or file_type == 'video':
                is_valid = self.driver.execute_script(
                    "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0",
                    elements)
                if not is_valid:
                    raise ValueError(f"{file_type.capitalize()}未正确加载。")
                print(f'接收到的{file_type.capitalize()}文件: {elements.get_attribute("src")}')

            # 额外对视频检查播放按钮的存在
            if file_type == 'video':
                play_button = self.base_find(Locators.video_svg)
                if not play_button:
                    raise ValueError("播放按钮未找到。")
                print("播放按钮存在，视频应可播放。")

            elif file_type == 'file':
                # 对文件的特殊处理，这里依赖于元素的显示状态和可能的文本内容
                if not elements.is_displayed():
                    raise ValueError("文件链接未显示。")
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
        except ValueError as e:
            self.driver.save_screenshot(f'file_invalid_{file_type}.png')
            print(f"无效元素：{e}")
            return False



