import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base.base_page import BasePage
from config import HOST
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from utils.save_register import save_registered_account


class RegisterPage(BasePage):

    register_link_loc = (By.XPATH,'//*[@id="root"]/div/div/div[2]/div[2]/form/div[5]/span[2]')
    user_count =(By.ID,'phoneNumber')
    code = (By.ID,'invitationCode')  # The invitation code can be left empty.
    register_button = (By.XPATH,'//*[@id="root"]/div/div/div[2]/div[2]/div/form/div[4]/div/div/div/div/button')
    # The assumed location of the captcha input box.
    verification_code_input_loc = (
        By.CSS_SELECTOR, 'div.flex.flex-row.items-center.justify-center > input[type="text"][maxlength]'
    )
    nickname_loc = (By.XPATH, '//*[@id="nickname"]')
    password_loc = (By.XPATH, '//*[@id="password"]')
    password2_loc = (By.XPATH, '//*[@id="password2"]')
    confirm_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.ant-btn-block')

    def __init__(self,driver):
        super().__init__(driver)
        self.url = HOST
    def go_to(self):
        self.driver.get(self.url)

    """Navigate from the login page to the registration page."""
    def navigate_to_register(self):
        self.base_click(self.register_link_loc)

    def register(self, phoneNumber,invitation_code=None,nickname='',password='',password2='' ,verification_code='666666'  ):
        expected_url = "{}#/chat".format(HOST)
        """Fill out the registration information and submit, simulate the verification code step"""
        """Fill out the registration information and submit,"""
        """skipping the verification code input depending on the situation."""

        self.enter_text(self.user_count,phoneNumber)
        if invitation_code:
            self.enter_text(self.code,invitation_code)
        self.base_click(self.register_button)


        try:
            error_message_locator = (By.XPATH, '/html/body/div[2]/div/div/div/div/span[2]')
            error_message_element = self.wait.until(EC.visibility_of_element_located(error_message_locator))
            error_message_text = error_message_element.text

            if "手机号已注册" in error_message_text:
                print("手机号已注册，请换号码")
                return "手机号已注册"

        except TimeoutException:
            # No error message found, continue trying to fill in the captcha.
            pass

        try:
            # Wait for the verification code input box to appear and fill in the verification code.
            verification_code_locator = (
            By.CSS_SELECTOR, 'div.flex.flex-row.items-center.justify-center > input[type="text"][maxlength]')
            verification_code_elements = self.wait.until(
                EC.visibility_of_all_elements_located(verification_code_locator))
            for index, element in enumerate(verification_code_elements):
                element.send_keys(verification_code[index])
        except TimeoutException:
            return "验证码输入框未出现"
         # Check if the error message "Incorrect verification code" appears.
        try:
            error_message_locator = (By.XPATH, '/html/body/div[2]/div/div/div/div/span[2]')
            error_message_element = self.wait.until(EC.visibility_of_element_located(error_message_locator))
            error_message_text = error_message_element.text
            if "验证码错误" in error_message_text:
                return "验证码错误"
        except TimeoutException:
            pass

            # Unable to find error message, continue trying to fill in the verification code.
            self.enter_text(self.nickname_loc,nickname)
            self.enter_text(self.password_loc, password)
            self.enter_text(self.password2_loc, password2)

            self.base_click(self.confirm_loc)

            # Check if the URL has been redirected to the expected one.
            try:
                WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
                save_registered_account(phoneNumber, password)
                return "注册成功"

            except  TimeoutException:
                return f"Expecting redirection to. {expected_url}，But failed to redirect. Current URL: {self.driver.current_url}"

